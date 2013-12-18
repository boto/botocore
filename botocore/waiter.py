import jmespath
import logging
import time


#from .botocore.exceptions import WaiterError


logger = logging.getLogger(__name__)


class Waiter(object):
    def __init__(self, name, operation, config):
        self.name = name
        self.operation = operation
        self.sleep_time = config['interval']
        self.max_attempts = config['max_attempts']
        self.success_type = config.get('success_type')
        self.success_value = config.get('success_value')
        self.success_path = config.get('success_path')
        if self.success_type == 'output' and \
                self.success_path is not None:
            self.success_path = jmespath.compile(
                self.success_path)
        self.failure_type = config.get('failure_type')
        self.failure_value = config.get('failure_value')
        self.failure_path = config.get('failure_path')
        if self.failure_type == 'output' and \
                self.failure_path is not None:
            self.failure_path = jmespath.compile(
                self.config['failure_path'])

    def wait(self, endpoint, **kwargs):
        logger.debug("Waiter %s waiting.")
        num_attempts = 0
        while num_attempts < self.max_attempts:
            http_response, parsed = self.operation.call(endpoint, **kwargs)
            if self.success_type == 'output':
                if self.success_path is not None:
                    match = self.success_path.search(parsed)
                    if self.success_value == match:
                        logger.debug("Success value acceptor matched "
                                     "success_path, terminal state reached.")
                        break
            elif self.success_type == 'error':
                if http_response.status_code >= 400 and 'Errors' in parsed:
                    error_codes = self._get_error_codes_from_response(
                        parsed)
                    if self.success_value in error_codes:
                        logger.debug("Success value acceptor matched "
                                     "error code, terminal state reached.")
                        break
            if self.failure_type == 'output':
                if self.failure_path is not None:
                    match = self.failure_path.search(parsed)
                    if self.failure_value == match:
                        error_msg = ("Failure value acceptor matched "
                                     "failure path, fail fast triggered.")
                        logger.debug(error_msg)
                        raise WaiterError(name=self.name, reason=error_msg)
            elif self.failure_type == 'error':
                if http_response.status_code >= 400 and 'Errors' in parsed:
                    error_codes = self._get_error_codes_from_response(
                        parsed)
                    if self.failure_value in error_codes:
                        error_msg = ("Failure value acceptor matched "
                                     "error code (%s), fail fast triggered, "
                                     "terminal state reached."
                                     % self.failure_value)
                        logger.debug(error_msg)
                        raise WaiterError(name=self.name, reason=error_msg)
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

    def _get_error_codes_from_response(self, parsed):
        errors = set()
        for error in parsed.get('Errors', []):
            if 'Code' in error:
                errors.add(error['Code'])
        return errors
