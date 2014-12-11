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

from itertools import tee

import jmespath
from botocore.exceptions import PaginationError
from botocore.compat import zip
from botocore.utils import set_value_from_jmespath, merge_dicts


class PageIterator(object):
    def __init__(self, method, input_token, output_token, more_results,
                 result_keys, non_aggregate_keys, limit_key, max_items,
                 starting_token, page_size, op_kwargs):
        self._method = method
        self._op_kwargs = op_kwargs
        self._input_token = input_token
        self._output_token = output_token
        self._more_results = more_results
        self._result_keys = result_keys
        self._max_items = max_items
        self._limit_key = limit_key
        self._starting_token = starting_token
        self._page_size = page_size
        self._op_kwargs = op_kwargs
        self._resume_token = None
        self._non_aggregate_key_exprs = non_aggregate_keys
        self._non_aggregate_part = {}

    @property
    def result_keys(self):
        return self._result_keys

    @property
    def resume_token(self):
        """Token to specify to resume pagination."""
        return self._resume_token

    @resume_token.setter
    def resume_token(self, value):
        if isinstance(value, list):
            self._resume_token = '___'.join([str(v) for v in value])

    @property
    def non_aggregate_part(self):
        return self._non_aggregate_part

    def __iter__(self):
        current_kwargs = self._op_kwargs
        previous_next_token = None
        next_token = [None for _ in range(len(self._input_token))]
        # The number of items from result_key we've seen so far.
        total_items = 0
        first_request = True
        primary_result_key = self.result_keys[0]
        starting_truncation = 0
        self._inject_starting_params(current_kwargs)
        while True:
            response = self._make_request(current_kwargs)
            parsed = self._extract_parsed_response(response)
            if first_request:
                # The first request is handled differently.  We could
                # possibly have a resume/starting token that tells us where
                # to index into the retrieved page.
                if self._starting_token is not None:
                    starting_truncation = self._handle_first_request(
                        parsed, primary_result_key, starting_truncation)
                first_request = False
                self._record_non_aggregate_key_values(parsed)
            current_response = primary_result_key.search(parsed)
            if current_response is None:
                current_response = []
            num_current_response = len(current_response)
            truncate_amount = 0
            if self._max_items is not None:
                truncate_amount = (total_items + num_current_response) \
                    - self._max_items
            if truncate_amount > 0:
                self._truncate_response(parsed, primary_result_key,
                                        truncate_amount, starting_truncation,
                                        next_token)
                yield response
                break
            else:
                yield response
                total_items += num_current_response
                next_token = self._get_next_token(parsed)
                if all(t is None for t in next_token):
                    break
                if self._max_items is not None and \
                        total_items == self._max_items:
                    # We're on a page boundary so we can set the current
                    # next token to be the resume token.
                    self.resume_token = next_token
                    break
                if previous_next_token is not None and \
                        previous_next_token == next_token:
                    message = ("The same next token was received "
                               "twice: %s" % next_token)
                    raise PaginationError(message=message)
                self._inject_token_into_kwargs(current_kwargs, next_token)
                previous_next_token = next_token

    def _make_request(self, current_kwargs):
        return self._method(**current_kwargs)

    def _extract_parsed_response(self, response):
        return response

    def _record_non_aggregate_key_values(self, response):
        non_aggregate_keys = {}
        for expression in self._non_aggregate_key_exprs:
            result = expression.search(response)
            set_value_from_jmespath(non_aggregate_keys,
                                    expression.expression,
                                    result)
        self._non_aggregate_part = non_aggregate_keys

    def _inject_starting_params(self, op_kwargs):
        # If the user has specified a starting token we need to
        # inject that into the operation's kwargs.
        if self._starting_token is not None:
            # Don't need to do anything special if there is no starting
            # token specified.
            next_token = self._parse_starting_token()[0]
            self._inject_token_into_kwargs(op_kwargs, next_token)
        if self._page_size is not None:
            # Pass the page size as the parameter name for limiting
            # page size, also known as the limit_key.
            op_kwargs[self._limit_key] = self._page_size

    def _inject_token_into_kwargs(self, op_kwargs, next_token):
        for name, token in zip(self._input_token, next_token):
            if token is None or token == 'None':
                continue
            op_kwargs[name] = token

    def _handle_first_request(self, parsed, primary_result_key,
                              starting_truncation):
        # First we need to slice into the array and only return
        # the truncated amount.
        starting_truncation = self._parse_starting_token()[1]
        all_data = primary_result_key.search(parsed)
        set_value_from_jmespath(
            parsed,
            primary_result_key.expression,
            all_data[starting_truncation:]
        )
        # We also need to truncate any secondary result keys
        # because they were not truncated in the previous last
        # response.
        for token in self.result_keys:
            if token == primary_result_key:
                continue
            set_value_from_jmespath(parsed, token.expression, [])
        return starting_truncation

    def _truncate_response(self, parsed, primary_result_key, truncate_amount,
                           starting_truncation, next_token):
        original = primary_result_key.search(parsed)
        if original is None:
            original = []
        amount_to_keep = len(original) - truncate_amount
        truncated = original[:amount_to_keep]
        set_value_from_jmespath(
            parsed,
            primary_result_key.expression,
            truncated
        )
        # The issue here is that even though we know how much we've truncated
        # we need to account for this globally including any starting
        # left truncation. For example:
        # Raw response: [0,1,2,3]
        # Starting index: 1
        # Max items: 1
        # Starting left truncation: [1, 2, 3]
        # End right truncation for max items: [1]
        # However, even though we only kept 1, this is post
        # left truncation so the next starting index should be 2, not 1
        # (left_truncation + amount_to_keep).
        next_token.append(str(amount_to_keep + starting_truncation))
        self.resume_token = next_token

    def _get_next_token(self, parsed):
        if self._more_results is not None:
            if not self._more_results.search(parsed):
                return [None]
        next_tokens = []
        for token in self._output_token:
            next_tokens.append(token.search(parsed))
        return next_tokens

    def result_key_iters(self):
        teed_results = tee(self, len(self.result_keys))
        return [ResultKeyIterator(i, result_key) for i, result_key
                in zip(teed_results, self.result_keys)]

    def build_full_result(self):
        complete_result = {}
        # Prepopulate the result keys with an empty list.
        for result_expression in self.result_keys:
            set_value_from_jmespath(complete_result,
                                    result_expression.expression, [])
        for _, page in self:
            # We're incrementally building the full response page
            # by page.  For each page in the response we need to
            # inject the necessary components from the page
            # into the complete_result.
            for result_expression in self.result_keys:
                # In order to incrementally update a result key
                # we need to search the existing value from complete_result,
                # then we need to search the _current_ page for the
                # current result key value.  Then we append the current
                # value onto the existing value, and re-set that value
                # as the new value.
                existing_value = result_expression.search(complete_result)
                result_value = result_expression.search(page)
                if result_value is not None:
                    existing_value.extend(result_value)
        merge_dicts(complete_result, self.non_aggregate_part)
        if self.resume_token is not None:
            complete_result['NextToken'] = self.resume_token
        return complete_result

    def _parse_starting_token(self):
        if self._starting_token is None:
            return None
        parts = self._starting_token.split('___')
        next_token = []
        index = 0
        if len(parts) == len(self._input_token) + 1:
            try:
                index = int(parts.pop())
            except ValueError:
                raise ValueError("Bad starting token: %s" %
                                 self._starting_token)
        for part in parts:
            if part == 'None':
                next_token.append(None)
            else:
                next_token.append(part)
        return next_token, index



class Paginator(object):

    PAGE_ITERATOR_CLS = PageIterator

    def __init__(self, method, pagination_config):
        self._method = method
        self._pagination_cfg = pagination_config
        self._output_token = self._get_output_tokens(self._pagination_cfg)
        self._input_token = self._get_input_tokens(self._pagination_cfg)
        self._more_results = self._get_more_results_token(self._pagination_cfg)
        self._non_aggregate_keys = self._get_non_aggregate_keys(
            self._pagination_cfg)
        self._result_keys = self._get_result_keys(self._pagination_cfg)
        self._limit_key = self._get_limit_key(self._pagination_cfg)

    @property
    def result_keys(self):
        return self._result_keys

    def _get_non_aggregate_keys(self, config):
        keys = []
        for key in config.get('non_aggregate_keys', []):
            keys.append(jmespath.compile(key))
        return keys

    def _get_output_tokens(self, config):
        output = []
        output_token = config['output_token']
        if not isinstance(output_token, list):
            output_token = [output_token]
        for config in output_token:
            output.append(jmespath.compile(config))
        return output

    def _get_input_tokens(self, config):
        input_token = self._pagination_cfg['input_token']
        if not isinstance(input_token, list):
            input_token = [input_token]
        return input_token

    def _get_more_results_token(self, config):
        more_results = config.get('more_results')
        if more_results is not None:
            return jmespath.compile(more_results)

    def _get_result_keys(self, config):
        result_key = config.get('result_key')
        if result_key is not None:
            if not isinstance(result_key, list):
                result_key = [result_key]
            result_key = [jmespath.compile(rk) for rk in result_key]
            return result_key

    def _get_limit_key(self, config):
        return config.get('limit_key')

    def paginate(self, **kwargs):
        """Create paginator object for an operation.

        This returns an iterable object.  Iterating over
        this object will yield a single page of a response
        at a time.

        """
        page_params = self._extract_paging_params(kwargs)
        return self.PAGE_ITERATOR_CLS(
            self._method, self._input_token,
            self._output_token, self._more_results,
            self._result_keys, self._non_aggregate_keys,
            self._limit_key,
            page_params['max_items'],
            page_params['starting_token'],
            page_params['page_size'],
            kwargs)

    def _extract_paging_params(self, kwargs):
        max_items = kwargs.pop('max_items', None)
        if max_items is not None:
            max_items = int(max_items)
        page_size = kwargs.pop('page_size', None)
        if page_size is not None:
            page_size = int(page_size)
        return {
            'max_items': max_items,
            'starting_token': kwargs.pop('starting_token', None),
            'page_size': page_size,
        }



class ResultKeyIterator(object):
    """Iterates over the results of paginated responses.

    Each iterator is associated with a single result key.
    Iterating over this object will give you each element in
    the result key list.

    :param pages_iterator: An iterator that will give you
        pages of results (a ``PageIterator`` class).
    :param result_key: The JMESPath expression representing
        the result key.

    """
    def __init__(self, pages_iterator, result_key):
        self._pages_iterator = pages_iterator
        self.result_key = result_key

    def __iter__(self):
        for _, page in self._pages_iterator:
            results = self.result_key.search(page)
            if results is None:
                results = []
            for result in results:
                yield result


# These two class use the Operation.call() interface that is
# being deprecated.  This is here so that both interfaces can be
# supported during a transition period.  Eventually these two
# interfaces will be removed.
class DeprecatedPageIterator(PageIterator):
    def __init__(self, operation, endpoint, input_token,
                 output_token, more_results,
                 result_keys, non_aggregate_keys, limit_key, max_items,
                 starting_token, page_size, op_kwargs):
        super(DeprecatedPageIterator, self).__init__(
            None, input_token, output_token, more_results, result_keys,
            non_aggregate_keys, limit_key, max_items,
            starting_token, page_size, op_kwargs)
        self._operation = operation
        self._endpoint = endpoint

    def _make_request(self, current_kwargs):
        return self._operation.call(self._endpoint, **current_kwargs)

    def _extract_parsed_response(self, response):
        return response[1]


class DeprecatedPaginator(Paginator):
    PAGE_ITERATOR_CLS = DeprecatedPageIterator

    def __init__(self, operation, pagination_config):
        super(DeprecatedPaginator, self).__init__(None, pagination_config)
        self._operation = operation

    def paginate(self, endpoint, **kwargs):
        """Paginate responses to an operation.

        The responses to some operations are too large for a single response.
        When this happens, the service will indicate that there are more
        results in its response.  This method handles the details of how
        to detect when this happens and how to retrieve more results.

        """
        page_params = self._extract_paging_params(kwargs)
        return self.PAGE_ITERATOR_CLS(
            self._operation, endpoint, self._input_token,
            self._output_token, self._more_results,
            self._result_keys, self._non_aggregate_keys,
            self._limit_key,
            page_params['max_items'],
            page_params['starting_token'],
            page_params['page_size'],
            kwargs)
