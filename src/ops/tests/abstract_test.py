"""TreeNode operation to add a new node."""

import nose_parameterized
import unittest

from src.ops import abstract


class _TrivialDualImplementOp(abstract.AbstractOp):
  def do(self, root, args):
    return True  # is_iterative

  def do_recursive(self, root, args):
    return False


class _TrivialSingleImplementOp(abstract.AbstractOp):
  def do(self, root, args):
    return 'is_iterative called'


class TestSingleImplementOp(unittest.TestCase):
  """Tests default executor routing behavior."""
  def testDoRecursive(self):
    self.assertEqual(_TrivialSingleImplementOp()(None, {
        'is_iterative': False,
    }), 'is_iterative called')


class TestDualImplementOp(unittest.TestCase):
  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testOpExecutor(self, is_iterative):
    """Tests the op executor routes iterative and recursive calls correctly."""
    self.assertEqual(_TrivialDualImplementOp()(None, {
        'is_iterative': is_iterative,
    }), is_iterative)

  def testDefaultExecutorPath(self):
    """Tests the default op executor invokes the iterative solution."""
    self.assertEqual(_TrivialDualImplementOp()(None), True)
