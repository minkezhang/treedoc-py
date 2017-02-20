"""Base TreeNode operation interface."""

import abc

class AbstractOp(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def do(self, node, args):
    """Execute the operation.

    Args:
      node: An instance of a TreeNode node.
      args: Dictionary of auxiliary inputs.
    Returns:
      TreeNode instance.
    """
    pass

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

    is_iterative = args.pop('is_iterative', True)
    if is_iterative:
      return self.do(node, args)
    else:
      return self.do_recursive(node, args)