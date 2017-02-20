import sortedcontainers

class IterableDict(sortedcontainers.SortedDict):
  """A dictionary with keys in sorted order."""

  def prev(self, key):
    """Returns previous key from sorted order.

    Args:
      key: Existing dictionary key.

    Returns:
      Previous dictionary key.

    Raises:
      KeyError: Given key does not exist in dictionary.
      StopIteration: Previous key does not exist.
    """
    if key not in self:
      raise KeyError(key)

    if (self.bisect_left(key) - 1) < 0:
      raise StopIteration

    return self.iloc[self.bisect_left(key) - 1]

  def next(self, key):
    """Returns next key from sorted order.

    Args:
      key: Existing dictionary key.

    Returns:
      Previous dictionary key.

    Raises:
      ValueError: Given key does not exist in dictionary.
      StopIteration: Next key does not exist.
    """
    if key not in self:
      raise KeyError(key)

    try:
      return self.iloc[self.bisect_right(key)]
    except IndexError:
      raise StopIteration
