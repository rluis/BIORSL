
from bedEntry.BedEntry6 import BedEntry6

from bedContainer.BedContainer import BedContainer
from typing import Iterator, TypeVar, Generator, Generic, List, Dict

class BedContainer6(BedContainer):

    def __init__(self, addExtras: bool = False):
        super().__init__(addExtras)
        self.bedContainer: Dict[str, List[BedEntry6]] = {}
        self.entryCounts: int = 0
        self.chrCounts: int = 0
        self.chrList: List[str] = []
        self.isSorted: bool = False

    ##################
    ##  Functions   ##
    ##################

    def addFrom_List(self, listBedEntry: list) -> None:
        if listBedEntry[0] not in self.chrList:
            self._addChr(listBedEntry[0])

        tmpBedEntry = BedEntry6(listBedEntry[0], int(listBedEntry[1]), int(listBedEntry[2]),
                                listBedEntry[3], listBedEntry[4], listBedEntry[5])
        if self.addExtras:
            for field in listBedEntry[6:]:
                tmpBedEntry.addExtraField(field)

        self.bedContainer[listBedEntry[0]].append(tmpBedEntry)

        self.entryCounts += 1


    ###########################
    ##  Build-in Functions   ##
    ###########################

    def __getitem__(self, item: int) -> BedEntry6:
        '''
        Getter item function for BedContainer class.
        Design to return a single BedEntry per time. Slices are not accepted, by now.

        :param int item: Index of BedEntry to retrieve
        :return BedEntry: A BedEntry Object
        '''

        if item < 0:
            raise ValueError("Negative index value is not accepted.")
        total = 0
        for chromosome in self.select_Chromosomes():
            nEntries = self.number_EntriesInChr(chromosome)
            total += nEntries
            if item < total:
                return self.bedContainer[chromosome][item - (total - nEntries)]
        raise ValueError("Index out of boundaries")

    def __iter__(self) -> Generator[BedEntry6, BedEntry6, None]:
        '''
        Iterator function for BedContainer class.

        :return BedEntry:  A BedEntry Object
        '''
        for chromosome in self.select_Chromosomes():
            yield from self.bedContainer[chromosome]
