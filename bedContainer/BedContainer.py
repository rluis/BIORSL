from bedEntry.BedEntry import BedEntry
from typing import Generator, List, Dict, Union


class BedContainer(object):
    '''
    Represents a Python Container for BedEntry objects (bed file format rows with 3 columns, plus possibly Extra Fields).

    '''

    def __init__(self, addExtras: bool = False) -> None:
        """
        Creates an instance of BedEntry object.

        :param bool addExtras: *True* if the Bed Entries have extra fields, *False* otherwise.
        """
        self.addExtras: bool = addExtras

        self.bedContainer: Dict[str, List[BedEntry]] = {}
        self.entryCounts: int = 0
        self.chrCounts: int = 0
        self.chrList: List[str] = []
        self.isSorted: bool = False

    ###################
    ##  Properties   ##
    ###################

    def empty(self) -> None:
        """
        Remove all BedEntries in the BedContainer. Also, reset all Counters.
        Final result similar to a new BedContainer instance.
        """
        self.chrCounts = 0
        self.entryCounts = 0
        self.isSorted = False
        self.bedContainer = {}
        self.chrList = []

    def _addChr(self, chrom: str) -> None:
        """
        Adds a Key in Internal Dictionary (*bedContainer*) with the input *chrom* name associated to an empty list.
        Then, appends *chrom* name to the List of chromosomes (*chrList*) and increments 1 unite to the chromosome counter (*chrCounts*).

        | Because of its internal function inside the class, it remains private.

        :param str chrom: The Chromosome name to add
        """
        self.bedContainer[chrom] = []
        self.chrList.append(chrom)
        self.chrCounts += 1

    def select_Chromosomes(self) -> List[str]:
        """
        Returns all chromosome names present in the BedContainer

        :return List: Return a List of strings representing chromosome names.
        """
        return self.chrList

    def findEntriesWith(self, chr="Any", sCoord="Any", eCoord="Any") -> List[BedEntry]:
        """
        Return all BedEntry objects having chr or sCoord or eCoord equal to the given ones.

        :param str chr: the chromosome where region is located
        :param int sCoord: the start coordinate of the region
        :param int eCoord: the end coordinate of the region
        :return List: Return a list of BedEntry objects having the given features
        """
        tmpList = []
        if chr != "Any":
            if chr not in self.chrList:
                raise ValueError("{} not in Chromosome List!".format(chr))

            else:
                tmpList = list(filter(lambda x: x.chr == chr, self.bedContainer[chr]))

        elif chr == "Any":
            for chr in self.chrList:
                tmpList = tmpList + self.bedContainer[chr]

        if sCoord != "Any":
            tmpList = list(filter(lambda x: x.sCoord == int(sCoord), tmpList))

        if eCoord != "Any":
            tmpList = list(filter(lambda x: x.eCoord == int(eCoord), tmpList))

        return tmpList

    def select_EntriesInChr(self, chrom: str) -> List[BedEntry]:
        """
        Returns all *BedEntry* objects inside the *BedContainer*, in the specified chromosome.

        If none, an empty list is returned.

        :param str chrom: Chromosome name (*chr*) of *BedEntry* objects to return
        :return List: A List of all *BedEntry* located in *chrom*
        """
        if chrom in self.select_Chromosomes():
            return self.bedContainer[chrom]
        else:
            return []


    def number_EntriesInChr(self, chrom: str) -> int:
        """
        Number of *BedEntry* with input chromosome name.

        If none, 0 (zero) ir returned.

        :param str chrom: Chromosome name (*chr*) of *BedEntry* objects to count
        :return: Number of *BedEntry* with input chromosome name.
        """
        if chrom in self.select_Chromosomes():
            return len(self.bedContainer[chrom])
        else:
            return 0

    def addFrom_List(self, listBedEntry: List[Union[str, List]]) -> None:
        """
        | Add one BedEntry object based in input list (*listBedEntry*), composed by strings / List, following the rules below:

        | ["*chr*", "*sCoord*", "*eCoord*", [*extraField1*, *extraField2*, ...]]  (extraFields List is optional)

        This function is also responsible for adding a unite to *entryCounts* Counter and to reset the sort property of
        *BedContainer* to *False*, since the new added *BedEntry* is added at the end of the correspondent chromosome list.
        Besides that, it also ensured that the chromosome key of the new *BedEntry* is added to the *BedContainer* if not
        already there.

        :param List listBedEntry: A list of strings with the required properties to be initialized by *BedEntry* constructor.
        """
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
        """
        Add *BedEntry* object directly in the container.

        This function is also responsible for adding a unite to *entryCounts* Counter and to reset the sort property of
        *BedContainer* to *False*, since the new added *BedEntry* is added at the end of the correspondent chromosome list.
        Besides that, it also ensured that the chromosome key is added to the *BedContainer* if not already there.

        :param BedEntry obj: BedEntry object to add.
        """
        input_chr = obj.chr
        if input_chr not in self.select_Chromosomes():
            self._addChr(input_chr)
        self.bedContainer[input_chr].append(obj)
        self.entryCounts += 1
        self.isSorted = False

    def removeEntryBed(self, entryBedObj: BedEntry) -> None:
        """
        Remove *BedEntry* object from *BedContainer*.

        This function is also responsible for decrease one unite to *entryCounts* Counter and ensured that the chromosome
        key is removed from *BedContainer* if not there is no BedEntry in that chromosome.

        :param BedEntry entryBedObj: BedEntry object to remove
        """
        inputChr = entryBedObj.chr
        self.bedContainer[inputChr].remove(entryBedObj)
        self.entryCounts -= 1

        # update chrList and chrCounts, if necessary
        for chr in self.chrList:
            if self.number_EntriesInChr(chr) == 0:
                self.chrList.remove(chr)
                self.chrCounts -= 1

    @staticmethod
    def merge(other1: object, other2: object) -> object:
        """
        Returns a their *BedContainer* object, with the content of the both merged input *BedContainer*s. Having as great
        advantage the preservation of *BedEntry* objects inside the input *BedContainer* objects.

        If at least one input *BedContainer* has flagged having extraField (*addExtras*), it ensures that the final
        *BedContainer* output also has that flag as *True*.

        :param BedContainer other1: *BedContainer* to merge, 1!
        :param BedContainer other2: *BedContainer* to merge, 2!
        :return: Returns a their *BedContainer* object, with the content of both input ones.

        """
        if not isinstance(other1, BedContainer):
            return NotImplemented
        if not isinstance(other2, BedContainer):
            return NotImplemented

        addExtrasToNew = False
        if other1.addExtras or other2.addExtras:
            addExtrasToNew = True

        newObject : BedContainer = BedContainer(addExtrasToNew)

        for entryA in other1.__iter__():
            newObject.addFrom_BedEntryObj(entryA)
        for entryB in other2.__iter__():
            newObject.addFrom_BedEntryObj(entryB)

        return newObject

    def sort(self) -> None:
        """
        Sort the list of each chromosome in the *bedContainer* recursively and the Chromosome List (*chrList*).
        Ensures that set the sorted flag to *True*
        """
        def sortWorker(chrEntries: List[BedEntry]):
            return sorted(chrEntries)

        # Sort Chromosome List names
        self.chrList = sorted(self.select_Chromosomes())

        # Sort BedEntry objects inside each Chromosome.
        for chrom in self.select_Chromosomes():
            self.bedContainer[chrom] = sortWorker(self.bedContainer[chrom])

        self.isSorted = True

    ######################
    ##  IO Management   ##
    ######################

    def readFromBedFile(self, BedFilePath: str) -> None:
        """
        Read a Bed File with 3 Columns (is possible to add more in extraFields) and store in the *BedContainer* object.

        :param str BedFilePath: Path to Bed File Format
        """
        with open(BedFilePath) as readFile:
            for line in readFile:
                self.addFrom_List(line.strip().split("\t"))
        self.isSorted = False

    def writeToBedFile(self, BedFilePath: str) -> None:
        """
        Writes in a Bed File Format all *BedEntry* objects inside *BedContainer*.
        If the BedContainer has defined having the flag *addExtras* as *True*, the extra fields will also be write in the
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
        """
        Returns the number of *BedEntry* objects in the *BedContainer*

        :return: Number *BedEntry* objects
        """
        return self.entryCounts

    def __str__(self):
        """
        A meta representation of the *BedContainer*

        The following parameters are being returned:

        - Number of Entries
        - Number Chromosomes
        - isSorted (Flag)
        - Add Extra Fields (Flag)

        :return: String with the *BedContainer* meta representation.
        """
        return "BED CONTAINER:\n\nNumber of Entries: {}\nNumber Chromosomes: {}\nisSorted: {}\nAdd Extra Fields: {}" \
            .format(self.entryCounts, self.chrCounts, self.isSorted, self.addExtras)
