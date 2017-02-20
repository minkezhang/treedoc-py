"""TreeNode operation to add a new node."""

import nose_parameterized
import unittest

from src.core import tree

from src.ops import abstract


class _TrivialReadOp(abstract.AbstractOp):
  is_read = True

  def do(self, root, args):
    root.metadata['is_read'] = self.__class__.is_read
    return root


class _TrivialWriteOp(_TrivialReadOp):
  is_read = False


class _TrivialDualImplementOp(abstract.AbstractOp):
  def do(self, root, args):
    root.metadata['is_iterative'] = True
    return root

  def do_recursive(self, root, args):
    root.metadata['is_iterative'] = False
    return root


class TestReadOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  def testReadAttr(self):
    root = _TrivialReadOp()(self.n, {})
    self.assertEqual(self.n.metadata['is_read'], True)


class TestWriteOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  def testWriteAttr(self):
    root = _TrivialWriteOp()(self.n, {})
    self.assertEqual(self.n.metadata['is_read'], False)


class TestDualImplementOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testOpExecutor(self, is_iterative):
    """Tests the op executor routes iterative and recursive calls correctly."""
    root = _TrivialDualImplementOp()(self.n, {
        'is_iterative': is_iterative,
    })
    self.assertEqual(self.n.metadata['is_iterative'], is_iterative)
