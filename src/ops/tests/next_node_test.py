"""Tests the NextNode operation."""

import mock
import nose_parameterized
import unittest

from src.core import tree
from src.ops import add_node
from src.ops import next_node


@mock.patch('src.ops.add_node.AddNodeOp._update_cache')
class TestNextNodeOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  def testNextNodeEnd(self, unused_update_cache):
    """Tests that getting next node from end of a tree raises an error."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'some-data',
    })

    with self.assertRaises(StopIteration):
      next_node.NextNodeOp()(child)

  def testNextNodeSibling(self, unused_update_cache):
    """Tests getting a sibling node is implemented."""
    sibling_a = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'sibling-a')],
        'data': 'some-data',
    })
    sibling_b = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'sibling-b')],
        'data': 'some-data',
    })

    next = next_node.NextNodeOp()(sibling_a)
    self.assertEqual(next, sibling_b)
    self.assertEqual(sibling_a.metadata['next'], sibling_b)

    self.assertNotIn('next', sibling_b.metadata)

  def testNextNodeIdempotency(self, unused_update_cache):
    """Tests that the TreeNode is actually caching a NextNode call."""
    sibling_a = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'sibling-a')],
        'data': 'some-data',
    })
    sibling_b = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'sibling-b')],
        'data': 'some-data',
    })

    next = next_node.NextNodeOp()(sibling_a)
    self.assertEqual(next, sibling_b)
    self.assertEqual(next, next_node.NextNodeOp()(sibling_a))

  def testNextNodeMinSubtree(self, unused_update_cache):
    """Tests in-order tree traversal with left subtree."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'some-data',
    })
    grandchild = add_node.AddNodeOp()(child, {
        'path': [(tree.TreeNode.LEFT, 'grandchild-id')],
        'data': 'some-data',
    })

    next = next_node.NextNodeOp()(self.n)
    self.assertEqual(next, grandchild)

  def testNextNodeParent(self, unused_update_cache):
    """Tests in-order tree traversal when parent is next node."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
    })

    next = next_node.NextNodeOp()(child)
    self.assertEqual(next, self.n)
