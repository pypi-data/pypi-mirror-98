from typing import Union

from treepath.path.traverser.match_traverser import MatchTraverser


class ValueTraverser(MatchTraverser):
    __slots__ = ()

    def __next__(self) -> Union[dict, list, str, int, float, bool, None]:
        return super().__next__().data
