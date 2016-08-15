from nose.tools import assert_true

from botocore import errorfactory
from botocore.exceptions import ClientError

def test_errorfactory():
    from botocore.errorfactory import Foo
    assert_true(isinstance(errorfactory.__all__, list))
    assert_true(isinstance(errorfactory.__file__, str))
    assert_true(isinstance(errorfactory.__name__, str))
    assert_true(issubclass(Foo, ClientError))
