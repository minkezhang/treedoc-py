"""Tests IterableDict functions."""

import unittest
from src.core import iterable_dict

class TestIterableDict(unittest.TestCase):

  def setUp(self):
    self.d = iterable_dict.IterableDict()
    self.d['a'] = 0
    self.d['b'] = 1

  def testPrevNodeDNE(self):
    with self.assertRaises(KeyError):
      self.assertEqual(self.d.prev('dne'))

  def testNextNodeDNE(self):
    with self.assertRaises(KeyError):
      self.assertEqual(self.d.next('dne'))

  def testPrevNode(self):
    self.assertEqual(self.d.prev('b'), 'a')

  def testPrevNodeEOF(self):
    with self.assertRaises(StopIteration):
      self.d.prev('a')

  def testNextNode(self):
    self.assertEqual(self.d.next('a'), 'b')

  def testNextNodeEOF(self):
    with self.assertRaises(StopIteration):
      self.d.next('b')
