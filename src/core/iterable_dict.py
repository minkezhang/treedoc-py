import sortedcontainers

class IterableDict(sortedcontainers.SortedDict):
  """A dictionary with keys in sorted order."""

  def prev(self, key):
    """Returns previous key from sorted order."""

    if (self.bisect_left(key) - 1) < 0:
      raise StopIteration

    try:
      return self.iloc[self.bisect_left(key) - 1]
    except IndexError:
      raise StopIteration

  def next(self, key):
    """Returns next key from sorted order."""

    try:
      return self.iloc[self.bisect_right(key)]
    except IndexError:
      raise StopIteration
