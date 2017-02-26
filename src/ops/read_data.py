"""TreeNode operation to read data."""

from src.core import tree

from src.ops import abstract
from src.ops import next_node


class ReadDataOp(abstract.AbstractOp):
  """Reads next several bytes of data from the TreeNode."""

  def do(self, root, args):
    """Implements ReadDataOp.

    Args:
      root: TreeNode instance
      args: Instance of a dictionary object of function args.

    Returns:
      String of the data read

    Raises:
      StopIteration if given node is the last one in the tree.
    """
    n_bytes = args.get('n_bytes', 0)
    current_bytes = 0
    aggregated_data = []
    node = root

    while current_bytes < n_bytes:
      if not node.metadata.get('is_deleted', False):
        aggregated_data.append(node.data)
        current_bytes += len(node)
      try:
        node = next_node.NextNodeOp()(node)
      except StopIteration:
        break

    return ''.join(aggregated_data)

  def do_recursive(self, root, args):
    n_bytes = args.get('n_bytes', 0)
    if args.get('n_bytes', 0) <= 0:
      return ''

    data = ''
    if not root.metadata.get('is_deleted', False):
      data = root.data

    try:
      node = next_node.NextNodeOp()(root)
    except StopIteration:  # base case
      return data

    args['n_bytes'] = args.get('n_bytes', 0) - len(data)
    return data + self.do_recursive(node, args)
