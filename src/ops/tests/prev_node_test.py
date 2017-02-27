"""Tests the PrevNode operation."""

import mock
import nose_parameterized
import unittest

from src.core import tree
from src.ops import add_node
from src.ops import prev_node


@mock.patch('src.ops.add_node.AddNodeOp._update_cache')
class TestPrevNodeOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  def testPrevNodeBegin(self, unused_update_cache):
    """Tests that getting prev node from start of a tree raises an error."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
    })

    with self.assertRaises(StopIteration):
      prev_node.PrevNodeOp()(child)

  def testPrevNodeSibling(self, unused_update_cache):
    """Tests getting a sibling node is implemented."""
    sibling_a = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'sibling-a')],
        'data': 'some-data',
    })
    sibling_b = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'sibling-b')],
        'data': 'some-data',
    })

    prev = prev_node.PrevNodeOp()(sibling_b)
    self.assertEqual(prev, sibling_a)
    self.assertEqual(sibling_b.metadata['prev'], sibling_a)

    self.assertNotIn('prev', sibling_a.metadata)

  def testPrevNodeIdempotency(self, unused_update_cache):
    """Tests that the TreeNode is actually caching a PrevNode call."""
    sibling_a = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'sibling-a')],
        'data': 'some-data',
    })
    sibling_b = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'sibling-b')],
        'data': 'some-data',
    })

    prev = prev_node.PrevNodeOp()(sibling_b)
    self.assertEqual(prev, sibling_a)
    self.assertEqual(prev, prev_node.PrevNodeOp()(sibling_b))

  def testPrevNodeMaxSubtree(self, unused_update_cache):
    """Tests in-order tree traversal with a right subtree."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
    })
    grandchild = add_node.AddNodeOp()(child, {
        'path': [(tree.TreeNode.RIGHT, 'grandchild-id')],
        'data': 'some-data',
    })

    prev = prev_node.PrevNodeOp()(self.n)
    self.assertEqual(prev, grandchild)

  def testPrevNodeParent(self, unused_update_cache):
    """Tests in-order tree traversal when parent is prev node."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'some-data',
    })

    prev = prev_node.PrevNodeOp()(child)
    self.assertEqual(prev, self.n)
