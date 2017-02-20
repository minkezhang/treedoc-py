from src.core import iterable_dict


class TreeNode(object):
  """TreeDoc class definition."""

  # branch constants
  LEFT = '0'
  RIGHT = '1'

  def __init__(self, partial_path, data, parent=None):
    """Initializes new TreeNode instance.

    Args:
      partial_path: (branch, id) tuple, where branch is either LEFT or RIGHT and
          id is a unique client designator.
      data: Actual text data stored in this node (probably a string)
      parent: TreeNode instance link to the parent node.

    Returns:
      None
    """

    (self.parent_branch, self.id) = partial_path

    if (self.parent_branch is not None and parent is None) or (
        self.parent_branch is None and parent is not None):
      raise ValueError('Parent node and branch mismatch.')

    if self.parent_branch not in [None, TreeNode.LEFT, TreeNode.RIGHT]:
      raise ValueError('Invalid tree branch.')

    self.parent = parent
    self.data = data

    #          N
    #      L /   \ R
    # [C, C, C] [C, C, C]
    self.children = {
        TreeNode.LEFT: iterable_dict.IterableDict(),
        TreeNode.RIGHT: iterable_dict.IterableDict()
    }

    # User-space node metadata
    self.metadata = {}

    self._next = None
    self._prev = None

  def __len__(self):
    return len(self.data)
