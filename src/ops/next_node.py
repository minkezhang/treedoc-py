"""TreeNode operation to find next node."""

import threading

from src.core import tree

from src.ops import abstract


class NextNodeOp(abstract.AbstractOp):
  """Finds next TreeNode instance in the tree in in-order traversal."""

  def do(self, root, args):
    """Implements NextNodeOp.

    See http://www.geeksforgeeks.org/inorder-successor-in-binary-search-tree.

    Args:
      root: TreeNode instance
      args: Instance of a dictionary object of function args.

    Returns:
      TreeNode instance

    Raises:
      StopIteration if given node is the last one in the tree.
    """
    # cache may have updated since lock has been acquired
    next = root.metadata.get('next', None)
    if next is not None:
      return next

    if root.parent is not None:  # get sibling node from parent branch
      try:
        root.metadata['next'] = root.parent.children[root.parent_branch][
            root.parent.children[root.parent_branch].next(root.id)]
        return root.metadata.get('next')
      except StopIteration:  # no siblings exist
        pass

    # get minimum value from right subtree
    if len(root.children[tree.TreeNode.RIGHT]):
      node = root.children[tree.TreeNode.RIGHT][
          root.children[tree.TreeNode.RIGHT].iloc[0]]
      while len(node.children[tree.TreeNode.LEFT]):
        node = node.children[tree.TreeNode.LEFT][
            node.children[tree.TreeNode.LEFT].iloc[0]]
      root.metadata['next'] = node
      return root.metadata.get('next')
    # current node is left leaf of the tree, traverse back up
    else:
      node = root
      while node.parent is not None:
        if node.parent_branch == tree.TreeNode.LEFT:
          root.metadata['next'] = node.parent
          return root.metadata.get('next')
        node = node.parent

    raise StopIteration('Last node reached.')
