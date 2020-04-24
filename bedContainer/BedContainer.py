from bedEntry.BedEntry import BedEntry
from typing import Generator, List, Dict


class BedContainer(object):

    def __init__(self, addExtras: bool = False):
        self.addExtras: bool = addExtras

        self.bedContainer: Dict[str, List[BedEntry]] = {}
        self.entryCounts: int = 0
        self.chrCounts: int = 0
        self.chrList: List[str] = []
        self.isSorted: bool = False

    ###################
    ##  Properties   ##
    ###################

    def empty(self):
        self.chrCounts = 0
        self.entryCounts = 0
        self.isSorted = False
        self.bedContainer = {}
        self.chrList = []

    def _addChr(self, chrom: str) -> None:
        self.bedContainer[chrom] = []
        self.chrList.append(chrom)
        self.chrCounts += 1

    def select_Chromosomes(self) -> list:
        return list(self.chrList)

    def select_EntriesInChr(self, chrom: str) -> list:
        return self.bedContainer[chrom]

    def number_EntriesInChr(self, chrom: str) -> int:
        return len(self.bedContainer[chrom])

    def addFrom_List(self, listBedEntry: list) -> None:
        if listBedEntry[0] not in self.chrList:
            self._addChr(listBedEntry[0])

        tmpBedEntry = BedEntry(listBedEntry[0], int(listBedEntry[1]), int(listBedEntry[2]))

        if self.addExtras:
            for field in listBedEntry[3:]:
                tmpBedEntry.addExtraField(field)

        self.bedContainer[listBedEntry[0]].append(tmpBedEntry)
        self.entryCounts += 1
        self.isSorted = False

    def addFrom_BedEntryObj(self, obj: BedEntry) -> None:
        input_chr = obj.chr
        if input_chr not in self.select_Chromosomes():
            self._addChr(input_chr)
        self.bedContainer[input_chr].append(obj)
        self.entryCounts += 1
        self.isSorted = False

    def removeEntryBed(self, entryBedObj: BedEntry):
        inputChr = entryBedObj.chr
        self.bedContainer[inputChr].remove(entryBedObj)
        self.entryCounts -= 1

        # update chrList and chrCounts, if necessary
        for chr in self.chrList:
            if self.number_EntriesInChr(chr) == 0:
                self.chrList.remove(chr)
                self.chrCounts -= 1

    @staticmethod
    def merge(other1: object, other2: object):
        if not isinstance(other1, BedContainer):
            return NotImplemented
        if not isinstance(other2, BedContainer):
            return NotImplemented

        addExtrasToNew = False
        if other1.addExtras or other2.addExtras:
            addExtrasToNew = True

        newObject = BedContainer(addExtrasToNew)

        for entryA in other1.__iter__():
            newObject.addFrom_BedEntryObj(entryA)
        for entryB in other2.__iter__():
            newObject.addFrom_BedEntryObj(entryB)

        return newObject

    def sort(self) -> None:
        def sortWorker(chrEntries: List[BedEntry]):
            return sorted(chrEntries)

        for chrom in self.select_Chromosomes():
            self.bedContainer[chrom] = sortWorker(self.bedContainer[chrom])

        self.isSorted = True

    ######################
    ##  IO Management   ##
    ######################

    def readFromBedFile(self, BedFilePath: str) -> None:
        with open(BedFilePath) as readFile:
            for line in readFile:
                self.addFrom_List(line.strip().split("\t"))
        self.isSorted = False

    def writeToBedFile(self, BedFilePath: str) -> None:
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

    def __getitem__(self, item: int) -> BedEntry:
        '''
        Getter item function for BedContainer class.
        Design to return a single BedEntry per time. Slices are not accepted, by now.

        :param int item: Index of BedEntry to retrieve
        :return BedEntry: A BedEntry Object(s)
        '''

        if item < 0:
            raise ValueError("Negative index value is not accepted.")

        total = 0
        for chromosome in self.select_Chromosomes():
            nEntries = self.number_EntriesInChr(chromosome)
            total += nEntries
            if item < total:
                return (self.bedContainer[chromosome][item - (total - nEntries)])
        raise ValueError("Index out of boundaries")

    def __iter__(self) -> Generator[BedEntry, None, None]:
        '''
        Iterator function for BedContainer class.

        :return BedEntry:  A BedEntry Object
        '''
        for chromosome in self.select_Chromosomes():
            yield from self.bedContainer[chromosome]

    def __len__(self):
        return self.entryCounts

    def __str__(self):
        return "BED CONTAINER:\n\nNumber of Entries: {}\nNumber Chromosomes: {}\nisSorted: {}\nAdd Extra Fields: {}" \
            .format(self.entryCounts, self.chrCounts, self.isSorted, self.addExtras)
