import threading

from src.core import iterable_dict


LOCK = threading.RLock()


class TreeNode(object):
  """TreeDoc class definition.

  Attributes:
    LEFT: Key signifying left child branch.
    RIGHT: Key signifying right child branch.
  """

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

    (self._parent_branch, self._id) = partial_path

    if (self.parent_branch is not None and parent is None) or (
        self.parent_branch is None and parent is not None):
      raise ValueError('Parent node and branch mismatch.')

    if self.parent_branch not in [None, TreeNode.LEFT, TreeNode.RIGHT]:
      raise ValueError('Invalid tree branch.')

    self.parent = parent
    self._data = data

    #          N
    #      L /   \ R
    # [C, C, C] [C, C, C]
    self._children = {
        TreeNode.LEFT: iterable_dict.IterableDict(),
        TreeNode.RIGHT: iterable_dict.IterableDict()
    }

    # User-space node metadata
    self._metadata = {}

  def __len__(self):
    return len(self.data)

  # read-only properties

  @property
  def children(self):
    return self._children

  @property
  def data(self):
    return self._data

  @property
  def id(self):
    return self._id

  @property
  def metadata(self):
    return self._metadata

  @property
  def parent_branch(self):
    return self._parent_branch
