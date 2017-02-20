"""Get node path given child node."""

from src.core import tree

from src.ops import abstract


class GetPathOp(abstract.AbstractOp):
  def do(self, root, args):
    path = []

    while root is not None:
      path.append((root.parent_branch, root.id))
      root = root.parent

    return path[::-1]

  def do_recursive(self, root, args):
    partial_path = (root.parent_branch, root.id)
    if root.parent is None:
      return [partial_path]
    else:
      return self.do_recursive(root.parent, args) + [partial_path]
