"""Tests the ReadData operation."""

import nose_parameterized
import unittest

from src.core import tree
from src.ops import add_node
from src.ops import read_data


class TestReadDataOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'root')

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testReadNullBytes(self, is_iterative):
    """Tests reading 0 bytes return the empty string."""
    data = read_data.ReadDataOp()(self.n, {
        'n_bytes': 0,
        'is_iterative': is_iterative,
    })

    self.assertEqual('', data)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testReadLongBytes(self, is_iterative):
    """Tests reading bytes longer than input returns max length possible."""
    data = read_data.ReadDataOp()(self.n, {
        'n_bytes': 1000,
        'is_iterative': is_iterative,
    })

    self.assertEqual('root', data)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testReadBorderBytes(self, is_iterative):
    """Tests reading exactly one node's worth of data."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'child',
    })

    data = read_data.ReadDataOp()(self.n, {
        'n_bytes': 4,
        'is_iterative': is_iterative,
    })

    self.assertEqual('root', data)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testReadShortBytes(self, is_iterative):
    """Tests reading bytes shorter returns smallest number of whole nodes."""
    data = read_data.ReadDataOp()(self.n, {
        'n_bytes': 1,
        'is_iterative': is_iterative,
    })

    self.assertEqual('root', data)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testReadMultipleNodes(self, is_iterative):
    """Tests reading bytes from multiple nodes behaves as expected."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'child',
    })

    data = read_data.ReadDataOp()(self.n, {
        'n_bytes': 1000,
        'is_iterative': is_iterative,
    })

    self.assertEqual(data, 'rootchild')
