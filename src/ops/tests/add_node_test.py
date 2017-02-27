"""Tests AddNodeOp TreeNode operation."""

import threading
import nose_parameterized
import unittest

from src.core import tree
from src.ops import add_node


class TestAddNodeOp(unittest.TestCase):
  def setUp(self):
    self.n = tree.TreeNode((None, 'some-id'), 'some-data')
    self.assertEqual(len(self.n.children[tree.TreeNode.LEFT]), 0)
    self.assertEqual(len(self.n.children[tree.TreeNode.RIGHT]), 0)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeUpdateCacheFirstNode(self, is_iterative):
    """Tests newly added first node update neighbor nodes."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })

    self.assertEqual(child.metadata['next'], self.n)
    self.assertEqual(self.n.metadata['prev'], child)

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeUpdateCacheLastNode(self, is_iterative):
    """Tests newly added last leaf nodes update neighbor nodes."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.RIGHT, 'child-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })

    self.assertEqual(child.metadata['prev'], self.n)
    self.assertEqual(self.n.metadata['next'], child)

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

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeNested(self, is_iterative):
    """Tests adding nested node."""
    child = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })

    grandchild = add_node.AddNodeOp()(self.n, {
        'path': [(tree.TreeNode.LEFT, 'child-id'), (tree.TreeNode.LEFT, 'grandchild-id')],
        'data': 'some-data',
        'is_iterative': is_iterative,
    })

    self.assertEqual(len(child.children[tree.TreeNode.LEFT]), 1)
    self.assertIn('grandchild-id', child.children[tree.TreeNode.LEFT])
    self.assertEqual(child.children[tree.TreeNode.LEFT]['grandchild-id'], grandchild)
    self.assertEqual(grandchild.data, 'some-data')
    self.assertEqual(grandchild.id, 'grandchild-id')

  @nose_parameterized.parameterized.expand([(True,), (False,)])
  def testAddNodeValueMultithreaded(self, is_iterative):
    """Tests expected behavior of multiple messages in flight."""
    n_threads = 1000
    threads = []

    t_ids = ['child-id-%04d' % t_id for t_id in xrange(n_threads)]

    for t_id in xrange(n_threads):
      t = threading.Thread(target=add_node.AddNodeOp(), args=(self.n, {
        'path': [(tree.TreeNode.LEFT, t_ids[t_id])],
        'data': 'some-data',
        'is_iterative': is_iterative,
      }))
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

    self.assertEqual(len(self.n.children[tree.TreeNode.LEFT]), n_threads)
    self.assertEqual(len(self.n.children[tree.TreeNode.RIGHT]), 0)

    self.assertEqual(list(self.n.children[tree.TreeNode.LEFT].keys()), t_ids)
