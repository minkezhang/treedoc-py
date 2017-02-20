"""Tests GetPath operation."""

import nose_parameterized
import unittest

from src.core import tree

from src.ops import get_path
from src.ops import add_node


class TestGetPathOp(unittest.TestCase):
  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testGetSingleton(self, is_iterative):
    root = tree.TreeNode((None, 'root-id'), 'some-data')

    self.assertEqual(get_path.GetPathOp()(root, {
        is_iterative: is_iterative,
    }), [(None, 'root-id')])

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testGetNestedPath(self, is_iterative):
    root = tree.TreeNode((None, 'root-id'), 'some-data')
    child = add_node.AddNodeOp()(root, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
    })

    self.assertEqual(get_path.GetPathOp()(child, {
        'is_iterative': is_iterative,
    }), [(None, 'root-id'), (tree.TreeNode.LEFT, 'child-id')])
