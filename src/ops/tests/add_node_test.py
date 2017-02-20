"""Tests AddNodeOp TreeNode operation."""

import nose_parameterized
import unittest

from src.core import tree
from src.ops import add_node


class TestAddNodeOp(unittest.TestCase):

  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeInvalidNullPath(self, is_iterative):
    """Tests correct operation behavior when no path is provided."""
    with self.assertRaises(ValueError):
      add_node.AddNodeOp()(self.n, {
          'path': [],
          'data': 'some-data',
          'is_iterative': is_iterative,
      })

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeInvalidDuplicatePath(self, is_iterative):
    """Tests correct operation behavior for duplicated node path."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })
    with self.assertRaises(ValueError):
      add_node.AddNodeOp()(self.n, {
          'path': [(tree.TreeNode.LEFT, 'child-id')],
          'data': 'some-data',
          'is_iterative': is_iterative,
    })

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeValid(self, is_iterative):
    """Tests expected behavior of general AddNodeOp case."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })

    self.assertEqual(len(self.n.children[tree.TreeNode.LEFT]), 1)
    self.assertIn('child-id', self.n.children[tree.TreeNode.LEFT])
    self.assertEqual(self.n.children[tree.TreeNode.LEFT]['child-id'], child)
    self.assertEqual(child.data, 'some-data')
    self.assertEqual(child.id, 'child-id')
