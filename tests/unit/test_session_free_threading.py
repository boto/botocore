# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Reproductions for data races a Session exhibits under free-threading.

These accompany the free-threading (no-GIL) support work: a single
``botocore.session.Session`` lazily builds and caches shared state
(components, credentials, parsed config) and ``HierarchicalEmitter`` mutates a
shared handler trie. Several of these paths use check-then-act without
synchronization. The races are latent under the GIL -- the ~5ms switch
interval makes the window rare -- but reproduce under free-threading, where
threads run Python bytecode in parallel.

These tests are written to FAIL on the current code and pass once the shared
state is synchronized. They use two techniques so a single run is conclusive
rather than relying on luck:

* delay-injection -- a sleep is inserted into the lazy-init window (between the
  "is it built yet?" check and the assignment), so concurrent first-access
  overlaps if the code is not locked. The factory/loader is then expected to
  run exactly once.
* identity-invariant -- N threads fetch the same lazily-built singleton and
  every thread should observe the same object; more than one distinct object
  means it was built more than once.

They also shrink the thread-switch interval to widen the window on the GIL
build. Run them under a free-threaded interpreter (e.g. python3.13t/3.14t) to
exercise true parallelism:

    python -m pytest tests/unit/test_session_free_threading.py
"""

import sys
import threading
import time
from contextlib import contextmanager

import botocore.configloader
import botocore.hooks
import botocore.session

N_THREADS = 32


@contextmanager
def aggressive_switching(interval=1e-6):
    old = sys.getswitchinterval()
    sys.setswitchinterval(interval)
    try:
        yield
    finally:
        sys.setswitchinterval(old)


def _run_concurrently(target, n_threads):
    """Run target(idx) on n_threads, all released from a barrier together."""
    barrier = threading.Barrier(n_threads)
    results = [None] * n_threads
    errors = [None] * n_threads

    def worker(idx):
        try:
            barrier.wait()
            results[idx] = target(idx)
        except Exception as e:  # noqa: BLE001
            errors[idx] = e

    threads = [
        threading.Thread(target=worker, args=(i,)) for i in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
        assert not t.is_alive(), "thread did not finish; possible deadlock"

    assert not any(errors), f"worker errors: {[repr(e) for e in errors if e]}"
    return results


def test_get_component_builds_deferred_component_once():
    # ComponentLocator.get_component lazily builds a deferred component with a
    # check-then-act ("if name in self._deferred: ... factory()"). Concurrent
    # first-access can run the factory more than once. endpoint_resolver is a
    # lazily-registered internal component; we slow its factory to force
    # concurrent first-access to overlap and count how many times it runs.
    session = botocore.session.Session()
    locator = session._internal_components
    build_count = [0]
    count_lock = threading.Lock()
    orig_factory = locator._deferred['endpoint_resolver']

    def slow_factory():
        with count_lock:
            build_count[0] += 1
        time.sleep(0.02)
        return orig_factory()

    locator._deferred['endpoint_resolver'] = slow_factory

    with aggressive_switching():
        results = _run_concurrently(
            lambda idx: session.get_component('endpoint_resolver'), N_THREADS
        )

    assert build_count[0] == 1, (
        f"deferred component factory ran {build_count[0]} times "
        f"under concurrent first-access; expected 1"
    )
    assert len({id(r) for r in results}) == 1, (
        "threads observed different component instances"
    )


def test_get_credentials_loads_once():
    # Session.get_credentials lazily loads self._credentials with a
    # check-then-act. Concurrent first-access can invoke the credential
    # provider more than once and discard all but the last result.
    session = botocore.session.Session()
    load_count = [0]
    lock = threading.Lock()

    class CountingProvider:
        def load_credentials(self):
            with lock:
                load_count[0] += 1
            time.sleep(0.02)
            return object()

    session._components.register_component(
        'credential_provider', CountingProvider()
    )

    with aggressive_switching():
        results = _run_concurrently(
            lambda idx: session.get_credentials(), N_THREADS
        )

    assert load_count[0] == 1, (
        f"credentials loaded {load_count[0]} times under concurrent "
        f"first-access; expected 1"
    )
    assert len({id(r) for r in results}) == 1


def test_full_config_parsed_once(monkeypatch):
    # Session.full_config lazily parses the config files with a check-then-act
    # and then mutates the dict in a merge loop. Concurrent first-access can
    # parse more than once, and a reader on the unlocked fast path can observe
    # a partially merged dict.
    session = botocore.session.Session()
    parse_count = [0]
    lock = threading.Lock()

    def counting_load(path):
        with lock:
            parse_count[0] += 1
        time.sleep(0.02)
        return {'profiles': {}}

    monkeypatch.setattr(botocore.configloader, 'load_config', counting_load)

    with aggressive_switching():
        results = _run_concurrently(lambda idx: session.full_config, N_THREADS)

    assert parse_count[0] == 1, (
        f"config parsed {parse_count[0]} times under concurrent "
        f"first-access; expected 1"
    )
    assert len({id(r) for r in results}) == 1


def test_emitter_concurrent_register_keeps_all_handlers():
    # HierarchicalEmitter shares a handler trie across threads. The race is the
    # check-then-act node creation in _PrefixTrie.append_item: if N threads
    # register a handler under the same not-yet-existing event path at the same
    # instant, an unlocked trie lets one node-creation clobber another and drop
    # the loser's handler. (This survives free-threading's per-object dict
    # locking because the check and the assignment are separate operations.)
    # Each round, all threads register under a fresh shared path, released
    # together by a per-round barrier.
    emitter = botocore.hooks.HierarchicalEmitter()
    n_threads = 12
    n_rounds = 40
    handlers = [
        [(lambda r=r, t=t: lambda **kw: (t, r))() for r in range(n_rounds)]
        for t in range(n_threads)
    ]
    round_barrier = threading.Barrier(n_threads)

    def worker(idx):
        for r in range(n_rounds):
            round_barrier.wait()
            emitter.register(f'round{r}.evt', handlers[idx][r])
        return n_rounds

    with aggressive_switching():
        _run_concurrently(worker, n_threads)

    for r in range(n_rounds):
        found = set(map(id, emitter._handlers.prefix_search(f'round{r}.evt')))
        for t in range(n_threads):
            assert id(handlers[t][r]) in found, (
                f"handler for thread {t} round {r} was lost -- concurrent "
                f"trie node creation raced"
            )
