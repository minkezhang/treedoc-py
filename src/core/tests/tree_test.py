import unittest

from src.core import tree


class TestTree(unittest.TestCase):

  def testTreeNormalInit(self):
    """Tests TreeNode.__init__ instantiates correctly."""

    n = tree.TreeNode((None, 'some-id'), 'some-data')
    self.assertEqual(n.parent, None)
    self.assertEqual(n.parent_branch, None)
    self.assertEqual(n.id, 'some-id')
    self.assertEqual(n.data, 'some-data')
    self.assertEqual(len(n), len('some-data'))
    self.assertEqual(n.metadata, {})

  def testTreeInitValueError(self):
    """Tests TreeNode.__init__ validates input."""

    with self.assertRaises(ValueError):
      tree.TreeNode((tree.TreeNode.LEFT, 'some-id'), 'some-data')

    r = tree.TreeNode((None, 'some-id'), 'some-data')
    with self.assertRaises(ValueError):
      tree.TreeNode((None, 'some-id'), 'some-data', r)

    with self.assertRaises(ValueError):
      tree.TreeNode(('foo', 'some-id'), 'some-data', r)
