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

  These operations do (Shapiro 2011, section 2.3.2):
    1. execute atomically,
    2. support nested calls,

  These operations do not:
    1. check Op preconditions,
    2. execute downstream (i.e. network support),
    3. store causual history (see section 4.1, Stability Problems),

  We will need a wrapper around these operation calls to fulfill the full
  CRDT specification.
  """

  __metaclass__ = abc.ABCMeta

  def _execute(self, f, *args, **kwargs):
    with tree.LOCK:
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
