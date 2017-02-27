"""TreeNode operation to get previous node."""

from src.core import tree

from src.ops import abstract


class PrevNodeOp(abstract.AbstractOp):
  """Finds previous TreeNode instance in the tree in in-order traversal."""

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
    prev = root.metadata.get('prev', None)
    if prev is not None:
      return prev

    if root.parent is not None:  # get sibling node from parent branch
      try:
        root.metadata['prev'] = root.parent.children[root.parent_branch][
            root.parent.children[root.parent_branch].prev(root.id)]
        return root.metadata.get('prev')
      except StopIteration:  # no siblings exist
        pass

    # get maximum value from left subtree
    if len(root.children[tree.TreeNode.LEFT]):
      node = root.children[tree.TreeNode.LEFT][
          root.children[tree.TreeNode.LEFT].iloc[-1]]
      while len(node.children[tree.TreeNode.RIGHT]):
        node = node.children[tree.TreeNode.RIGHT][
            node.children[tree.TreeNode.RIGHT].iloc[-1]]
      root.metadata['prev'] = node
      return root.metadata.get('prev')

    # current node is right leaf of the tree, traverse back up
    else:
      node = root
      while node.parent is not None:
        if node.parent_branch == tree.TreeNode.RIGHT:
          root.metadata['prev'] = node.parent
          return root.metadata.get('prev')
        node = node.parent

    raise StopIteration('First node reached.')

