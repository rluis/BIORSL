from bedEntry.BedEntry12 import BedEntry12

from bedContainer.BedContainer import BedContainer
from typing import Iterator, TypeVar, Generator, Generic, List, Dict


class BedContainer12(BedContainer):
    '''
    Represents a Python Container for BedEntry objects (bed file format rows with 12 Columns, plus possibly Extra Fields).

    '''

    def __init__(self, addExtras=False):
        super().__init__(addExtras)

        self.bedContainer: Dict[str, List[BedEntry12]] = {}
        self._entryCounts = 0
        self._chrCounts = 0
        self._chrList: List[str] = []
        self._isSorted = False

    # Not ready yet! Feel free to complete it!

    # ...
    # ...
    # Add method "add"
    # etc...

    ###########################
    ##  Build-in Functions   ##
    ###########################
