# =============================================================================
# @file   utils.py
# @author Juanwu Lu
# @date   Dec-21-22
# =============================================================================
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Iterable, Tuple


class AverageTracker(object):
    """Average value tracker.

    Attributes:
        name: The name of the data.
        val: The latest value stored.
        sum: The current total value.
        count: The current total update counts.
        avg: The current average value.
    """

    def __init__(self, name: str) -> None:
        """Initialize average metric tracker."""
        self.name = name
        self.reset()

    def __call__(self) -> float:
        return self.item()

    def __str__(self) -> str:
        fmtstr = '{name} {val:.4f} ({avg:.4f})'
        return fmtstr.format(**self.__dict__)

    def reset(self) -> None:
        self.val = 0.
        self.sum = 0.
        self.count = 0.
        self.avg = 0.

    def update(self, value: float, n: int = 1) -> None:
        """Update average metric tracker.

        Args:
            value: current new value to input.
            n: number of times to update.
        """
        self.val = value
        self.sum += value * n
        self.count += n
        self.avg = self.sum / self.count

    def item(self) -> float:
        return self.avg


class AverageTrackerGroup(object):
    """A collection of average value trackers.

    Attributes:
        _storage: A dictionary of `AverageTracker` object trackers.
    """

    def __init__(self) -> None:
        self.reset()

    def __getattr__(self, item: str) -> Any:
        return self._storage[item].item()

    def __getitem__(self, item: str) -> Any:
        return self._storage[item].item()

    def __repr__(self) -> str:
        return 'Metric Group: ' +\
               ' '.join(str(v) for v in self._storage.values())

    def __str__(self) -> str:
        return ' '.join(str(v) for v in self._storage.values())

    def update(self, data: Dict[str, Any]) -> None:
        '''Update the meter group with a Dict of values.

        Args:
            data: A dictionary mapping data names to their current values.
        '''
        for name, value in data.items():
            if name not in self._storage:
                self._storage[name] = AverageTracker(name)
            if isinstance(value, Iterable):
                self._storage[name].update(*value)
            else:
                self._storage[name].update(value)

    def reset(self) -> None:
        '''Reset the group metric tracker.'''
        self._storage: Dict[str, AverageTracker] = OrderedDict()

    def items(self) -> Tuple[str, Any]:
        for (key, val) in self._storage.items():
            yield (key, val.item())
