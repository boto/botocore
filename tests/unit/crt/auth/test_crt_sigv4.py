# This will run the CRT version of the test_generator
# on import. When we're off nose, we should split this
# yield test into two and have the CRT portion here.
from tests.unit.auth.test_sigv4 import test_generator
