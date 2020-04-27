
from bedEntry.BedEntry6 import BedEntry6

from bedContainer.BedContainer import BedContainer
from typing import Iterator, TypeVar, Generator, Generic, List, Dict, Union

class BedContainer6(BedContainer):
    '''

    Represents a Python Container for BedEntry6 objects (bed file format rows with 6 columns, plus possibly Extra Fields).


    '''
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

    def addFrom_List(self, listBedEntry: List[Union[str, List, int]]) -> None:
        """
        | Add one BedEntry object based in input list (*listBedEntry*), composed by strings / List, following the rules below:

        | ["*chr*", "*sCoord*", "*eCoord*", "*name*", "*score*","*strand*", [*extraField1*, *extraField2*, ...]]  (extraFields List is optional)

        This function is also responsible for adding a unite to *entryCounts* Counter and to reset the sort property of
        *BedContainer* to *False*, since the new added *BedEntry* is added at the end of the correspondent chromosome list.
        Besides that, it also ensured that the chromosome key of the new *BedEntry* is added to the *BedContainer* if not
        already there.

        :param List listBedEntry: A list of strings with the required properties to be initialized by *BedEntry* constructor.
        """

        if listBedEntry[0] not in self.chrList:
            self._addChr(listBedEntry[0])

        tmpBedEntry = BedEntry6(listBedEntry[0], int(listBedEntry[1]), int(listBedEntry[2]),
                                listBedEntry[3], listBedEntry[4], listBedEntry[5])
        if self.addExtras:
            for field in listBedEntry[6:]:
                tmpBedEntry.addExtraField(field)

        self.bedContainer[listBedEntry[0]].append(tmpBedEntry)

        self.entryCounts += 1

    ######################
    ##  IO Management   ##
    ######################

    def readFromBedFile(self, BedFilePath: str) -> None:
        """
        Read a Bed File with 6 Columns (is possible to add more in extraFields) and store in the *BedContainer6* object.

        :param str BedFilePath: Path to Bed File Format
        """
        with open(BedFilePath) as readFile:
            for line in readFile:
                self.addFrom_List(line.strip().split("\t"))
        self.isSorted = False

    def writeToBedFile(self, BedFilePath: str) -> None:
        """
        Writes in a Bed File Format all *BedEntry6* objects inside *BedContainer6*.
        If the BedContainer6 has defined having the flag *addExtras* as *True*, the extra fields will also be write in the
        Bed File, in the same order as they are registered in *BedContainer* object.

        :param str BedFilePath: The path where the bed file will be writen.
        """
        with open(BedFilePath, 'w') as writeFile:
            for chromosome in self.select_Chromosomes():
                for entry in self.bedContainer[chromosome]:
                    if self.addExtras:
                        tmpList = []
                        for key in entry.extraFields.keys():
                            tmpList.append(entry.extraFields[key])
                        tmpList = "\t".join(tmpList)
                        writeFile.write("{}\t{}\n".format(str(entry), str(tmpList)))
                    else:
                        writeFile.write("{}\n".format(str(entry)))


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
