"""TreeNode operation to add a new node."""

from src.core import tree

from src.ops import abstract

# TODO(minkezhang): Reset L|R cache by invoking NextNode|PrevNode on newly
# added node.


class AddNodeOp(abstract.AbstractOp):
  """Adds new TreeNode instance to the tree."""
  is_read = False

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

      return node
    else:  # recursive case
      (node_branch, node_id) = path.pop(0)
      return self.do_recursive(root.children[node_branch][node_id], args)
