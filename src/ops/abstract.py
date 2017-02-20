"""Base TreeNode operation interface."""

import abc

from src.core import tree


class AbstractOp(object):
  """Base TreeNode operation class.

  Classes can be called as:
    SomeOp()(node, {
      ...
      'is_iterative': True,
    })

  Attributes:
    is_read: Boolean expressing if the operation alters the TreeNode op.
  """

  __metaclass__ = abc.ABCMeta

  is_read = True

  def _execute(self, f, *args, **kwargs):
    if self.__class__.is_read:
      with tree.RWLOCK.reader_lock():
        return f(*args, **kwargs)
    else:
      with tree.RWLOCK.writer_lock():
        return f(*args, **kwargs)

  @abc.abstractmethod
  def do(self, node, args):
    """Execute the operation.

    Args:
      node: An instance of a TreeNode node.
      args: Dictionary of auxiliary inputs.
    Returns:
      TreeNode instance.
    """

  def do_recursive(self, node, args):
    """Executes the operaton applied recursively.

    This definition is optional -- by default this will call the iterative
    method instead (generally this is more efficient).

    Args:
      node: An instance of a TreeNode node.
      args: Dictionary of auxiliary inputs.
    Returns:
      TreeNode instance.
    """
    return self.do(node, args)

  def __call__(self, node, args=None):
    """Calls the appropriate TreeNode operation to execute.

    Args:
      node: An instance of a TreeNode node.
      args: Dictionary of auxiliary inputs.
    Returns:
      TreeNode instance.
    """
    if args is None:
      args = {}

    is_iterative = args.pop('is_iterative', True)

    if is_iterative:
      return self._execute(self.do, node, args)
    else:
      return self._execute(self.do_recursive, node, args)
