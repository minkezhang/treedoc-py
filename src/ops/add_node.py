"""TreeNode operation to add a new node."""

from src.core import tree

from src.ops import abstract
from src.ops import prev_node
from src.ops import next_node


class AddNodeOp(abstract.AbstractOp):
  """Adds new TreeNode instance to the tree."""
  is_read = False

  def _update_cache(self, node):
    """Updates node neighbors' cache with newly inserted node."""

    try:
      prev = prev_node.PrevNodeOp()(node)
      prev.metadata['next'] = node
    except StopIteration:
      pass

    try:
      next = next_node.NextNodeOp()(node)
      next.metadata['prev'] = node
    except StopIteration:
      pass


  def do(self, root, args):
    (path, data) = (args.get('path', None), args.get('data', None))

    if not len(path):
      raise ValueError('Invalid node path provided.')

    for (node_branch, node_id) in path[:-1]:
      root = root.children[node_branch][node_id]

    (node_branch, node_id) = path[-1]

    if node_id in root.children[node_branch]:
      raise ValueError('Invalid node path provided.')

    node = tree.TreeNode((node_branch, node_id), data, root)
    root.children[node_branch][node_id] = node

    self._update_cache(node)
    return node

  def do_recursive(self, root, args):
    (path, data) = (args.get('path', None), args.get('data', None))

    if not len(path):
      raise ValueError('Invalid node path provided.')

    if len(path) == 1:  # end case
      (node_branch, node_id) = path[0]

      if node_id in root.children[node_branch]:
        raise ValueError('Invalid node path provided.')

      node = tree.TreeNode((node_branch, node_id), data, root)
      root.children[node_branch][node_id] = node

      self._update_cache(node)
      return node
    else:  # recursive case
      (node_branch, node_id) = path.pop(0)
      return self.do_recursive(root.children[node_branch][node_id], args)
