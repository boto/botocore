# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import jmespath
import logging
import time


from .exceptions import WaiterError


logger = logging.getLogger(__name__)


class Waiter(object):
    """Wait for a resource to reach a certain state.

    In addition to creating this class manually, you can
    also use ``botocore.service.Service.get_waiter`` to
    create an instance of ``Waiter```.

    The typical usage pattern is from a ``Service`` object::

        ec2 = session.get_service('ec2')
        p = ec2.get_operation('RunInstances').call(endpoint, **kwargs)[1]
        instance_running = ec2.get_waiter('InstanceRunning')
        instance_id = p['Reservations'][0]['Instances'][0]['InstanceId']

        # This will block until the instance reaches a 'running' state.
        instance_running.wait(instance_ids=[instance_id])

    """
    def __init__(self, name, operation, config):
        """

        :type name: str
        :param name: The name of the waiter.

        :type operation: ``botocore.operation.Operation``
        :param operation:  The operation associated with the waiter.
            This is specified in the waiter configuration as the
            ``operation`` key.

        :type config: dict
        :param config: The waiter configuration.

        """
        self.name = name
        self.operation = operation
        self.sleep_time = config['interval']
        self.max_attempts = config['max_attempts']
        self.success = self._process_config(config.get('success'))
        self.failure = self._process_config(config.get('failure'))

    def _process_config(self, acceptor_config):
        if acceptor_config is None:
            return {}
        new_config = acceptor_config.copy()
        if new_config['type'] == 'output' and \
                new_config.get('path') is not None:
            new_config['path'] = jmespath.compile(acceptor_config['path'])
        return new_config

    def wait(self, endpoint, **kwargs):
        """Wait until a resource reaches its success state.

        Calling this method will block until the waiter reaches its
        desired state. If the failure state is reached, a ``WaiterError``
        is raised.

        The ``**kwargs`` passed to this method will be forwarded to the
        operation associated with the waiter.

        :param endpoint:  An instance of ``botocore.endpoint.Endpoint``.

        """
        logger.debug("Waiter %s waiting.", self.name)
        num_attempts = 0
        while num_attempts < self.max_attempts:
            http_response, parsed = self.operation.call(endpoint, **kwargs)
            if self.success:
                if self._matches_acceptor_state(self.success,
                                                http_response, parsed):
                    # For the success state, if the acceptor matches then we
                    # break the loop.
                    break
            if self.failure:
                if self._matches_acceptor_state(self.failure,
                                                http_response, parsed):
                    # For the failure state, if the acceptor matches then we
                    # raise an exception.
                    raise WaiterError(
                        name=self.name,
                        reason='Failure state matched one of: %s' %
                        ', '.join(self.failure['value']))
            logger.debug("No acceptor state reached for waiter %s, "
                         "attempt %s/%s, sleeping for: %s",
                         self.name, num_attempts, self.max_attempts,
                         self.sleep_time)
            num_attempts += 1
            time.sleep(self.sleep_time)
        else:
            error_msg = ("Max attempts (%s) exceeded for waiter %s without "
                         "reaching a terminal state."
                         % (self.max_attempts, self.name))
            logger.debug(error_msg)
            raise WaiterError(name=self.name, reason=error_msg)

    def _matches_acceptor_state(self, acceptor, http_response, parsed):
        if acceptor['type'] == 'output':
            return self._matches_acceptor_output_type(acceptor, http_response,
                                                      parsed)
        elif acceptor['type'] == 'error':
            return self._matches_acceptor_error_type(acceptor, http_response,
                                                     parsed)

    def _matches_acceptor_output_type(self, acceptor, http_response, parsed):
        if 'path' not in acceptor and not self._get_error_codes_from_response(parsed):
            # If there's no path specified, then a successful response means
            # that we've matched the acceptor.
            return True
        match = acceptor['path'].search(parsed)
        return self._path_matches_value(match, acceptor['value'])

    def _path_matches_value(self, match, value):
        # Determine if the matched data matches the config value.
        if match is None:
            return False
        elif not isinstance(match, list):
            # If match is not a list, then we need to perform an exact match,
            # this is something like Table.TableStatus == 'CREATING'
            return self._single_value_match(match, value)
        elif isinstance(match, list):
            # If ``match`` is a list, then we need to ensure that every element
            # in ``match`` matches something in the ``value`` list.
            return all(self._single_value_match(element, value)
                       for element in match)
        else:
            return False

    def _single_value_match(self, match, value):
        for v in value:
            if match == v:
                return True
        else:
            return False

    def _matches_acceptor_error_type(self, acceptor, http_response, parsed):
        if http_response.status_code >= 400 and 'Errors' in parsed:
            error_codes = self._get_error_codes_from_response(parsed)
            for v in acceptor['value']:
                if v in error_codes:
                    return True
        return False

    def _get_error_codes_from_response(self, parsed):
        errors = set()
        for error in parsed.get('Errors', []):
            if 'Code' in error:
                errors.add(error['Code'])
        return errors
