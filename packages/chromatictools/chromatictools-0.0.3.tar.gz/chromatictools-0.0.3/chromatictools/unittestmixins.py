"""Mixin classes for unittests"""
import contextlib
import io


class AssertPrintsMixin:
  """Mixin class for print assertion"""
  @contextlib.contextmanager
  def assert_prints(self, target: str):
    """Assert that contextual code prints the target string.
    Use as context manager

    Args:
      target (str): Print expectation"""
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
      yield
      printed = buf.getvalue()
    self.assertEqual(printed, target)
