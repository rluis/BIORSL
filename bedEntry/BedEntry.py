from typing import List, Dict, Union
import pysam


class BedEntry(object):
    """
    Represents a Bed line of Bed file, composed by 3 core column.

    """

    def __init__(self, chr: str, sCoord: int, eCoord: int, extraFields: Union[None, List] = None) -> None:
        """
        Create an instance of BedEntry object.

        :param str chr: the chromosome where region is located
        :param int sCoord: the start coordinate of the region
        :param int eCoord: the end coordinate of the region
        :param None,List extraFields: Additional fields to the standard 3 columns. (optional)

        """

        self.chr = chr
        self.sCoord = sCoord
        self.eCoord = eCoord
        self.extraFields = {}

        if extraFields is not None:
            for field in extraFields:
                self.addExtraField(field)

    ###################
    ##  Properties   ##
    ###################

    @property
    def chr(self) -> str:
        """
        Get the chromosome (*chr*) where the region is located

        :getter: Returns chromosome name
        :setter: Sets chromosome name.
        :type: string

        """
        return self._chr

    @chr.setter
    def chr(self, value: str) -> None:
        """
        Set region chromosome the new input value.
        :param str value: Chromosome Value
        """
        if type(value) != str:
            raise ValueError("Chromosome {} is not a string type.".format(value))
        self._chr = value

    @chr.deleter
    def chr(self) -> None:
        """
        Set chr property as None
        """
        self._chr = None

    @property
    def sCoord(self) -> int:
        """
        Get start coordinate (*sCoord*) where the region is located.

        :getter: Returns start coordinate
        :setter: Sets start coordinate. Can't be higher than eCoord, if latter is defined.
        :type: int
        """
        return self._sCoord

    @sCoord.setter
    def sCoord(self, value: int) -> None:
        """
        Set BedEntry start coordinate (*sCoord*) with new input value.
        It is guaranteed that *sCoord* cannot be higher than *eCoord*, if latter is defined.

        :param int value: A value to be the new *sCoord*
        """
        if type(value) != int:
            raise ValueError("Start Position {} is not a integer type.".format(value))

        if value < 0:
            raise ValueError("Start Position {} is negative.".format(value))

        if hasattr(self, 'eCoord'):
            if value >= self.eCoord:
                raise ValueError("Start Coordinate higher or equal than End Coordinate")

        self._sCoord = value

    @sCoord.deleter
    def sCoord(self) -> None:
        """
        Set sCoord property as None
        """
        self._sCoord = None

    @property
    def eCoord(self) -> int:
        """
        Get the end coordinate (*eCoord*) where the region is located.

        :getter: Returns end coordinate
        :setter: Sets end coordinate. Can't be lower than sCoord, if latter is defined.
        :type: int

        """
        return self._eCoord

    @eCoord.setter
    def eCoord(self, value: int):
        """
        Set BedEntry end coordinate (*eCoord*) with new input value.
        It is guaranteed that *eCoord* cannot be smaller than *sCoord*, if latter is defined.

        :param int value: A value to be the new *eCoord*
        """
        if not isinstance(value, int):
            raise ValueError("End Position {} is not a integer type.".format(value))

        if value < 0:
            raise ValueError("Start Position {} is negative.".format(value))

        if hasattr(self, 'sCoord'):
            if value <= self.sCoord:
                raise ValueError("End Coordinate lower or equal than Start Coordinate")

        self._eCoord = value

    @eCoord.deleter
    def eCoord(self):
        """
        Set eCoord property as None
        """
        self._eCoord = None

    @property
    def extraFields(self) -> Dict:
        """
        Get the Extra Fields (*extraFields*) in a Dict format.

        - Key1 -> Value1
        - Key2 -> Value2
        - ...

        :getter: Returns end coordinate
        :setter: In case of List as input, it restores the Dict of ExtraFields with the elements in the input List.
        :type: List,None

        """
        return self._extraFields

    @extraFields.setter
    def extraFields(self, value):
        self._extraFields = value

    @extraFields.deleter
    def extraFields(self):
        """
        Empty extraFields to an empty Dict
        """
        self._extraFields = {}

    ##################
    ##  Functions   ##
    ##################

    def addExtraField(self, extraField: List) -> None:
        """
        Adds the Extra field(s) to BedEntry objects.

        :param List extraField: List of extra Fields in the required order
        """
        n_extra_fields = self.lenExtraFields()
        self.extraFields[n_extra_fields] = extraField

    def hasExtraFields(self) -> bool:
        """
        Question the object if it has extra fields or not. True in positive case, False otherwise.

        :return bool: True / False
        """
        return self.lenExtraFields() > 0

    def lenExtraFields(self) -> int:
        """
        Get the exact number of extra fields in the BedEntry instance.

        :return int: Number of Extra fields
        """
        return len(self.extraFields.keys())

    def isOverlapping(self, other):
        """
        | Question the object if overlaps another object from *BedEntry*.
        | Considered:

        - *chr*
        - *sCoord*
        - *eCoord*

        :param BedEntry other: BedEntry object to compare with
        :return bool: *True* if both objects overlap each other, *False* otherwise.
        """
        if self.chr == other.chr:
            return self.sCoord <= other.eCoord and other.sCoord <= self.eCoord
        return False

    def addLeftClip(self, value: int) -> None:
        """
        Adds *value* number of bp to the BedEntry on the Left side.
        It means that if you gives *x* bp as input, it will set the sCoord to:

        sCoord = sCoord - value

        :param int value: Number of bp to increment on the Left side.
        """
        self.sCoord -= value

    def addRightClip(self, value: int) -> None:
        """
        Adds *value* number of bp to the BedEntry on the Right side.
        It means that if you gives *x* bp as input, it will set the eCoord to:

        eCoord = eCoord + value

        :param int value: Number of bp to increment on the Right side
        """
        self.eCoord += value

    def addClips(self, value: int) -> None:
        """
        Extends the clips on the Left and Right side by *value* bp.
        It means that if you gives *x* bp as input, it will set the sCoord and eCoord to:

        sCoord = sCoord - value
        eCoord = eCoord + value

        :param int value: Number of bp to increment on the Left and Right side.
        """
        self.addLeftClip(value)
        self.addRightClip(value)

    def shift(self, value: int) -> None:
        """
        Shifts the Region *value* bp to the right if, *value* is positive, or to the left if *value* is negative

        :param int value: Number of bp to shift the BedEntry region.
        """
        self.addLeftClip(-value)
        self.addRightClip(value)

    def binRegion(self, nBin: int) -> object:
        """
        Binning BedEntry in ``nBin`` number of *BedEntry* objects, returned in a *BedContainer*.

        :param int nBin: Number of bins to divide the *BedEntry* objects
        :return BedContainer: A *BedContainer* where are storage the *BedEntry* bins created
        """
        from bedContainer.BedContainer import BedContainer

        # Initialize BedContainer to return
        bedContainerToReturn = BedContainer(addExtras=True)
        quotient, remainder = divmod(len(self), nBin)
        number_bp_per_bin = [quotient + 1] * remainder + [quotient] * (nBin - remainder)
        int_sCoord = self.sCoord
        int_eCoord = self.sCoord
        for i in range(nBin):
            if i == 0:  # first cycle
                int_sCoord = self.sCoord
                int_eCoord += number_bp_per_bin[i]
            else:
                int_sCoord += number_bp_per_bin[i-1]
                int_eCoord += number_bp_per_bin[i]
            # Create BedEntry object
            newBin = BedEntry(self.chr, int_sCoord, int_eCoord, list(self.extraFields.values()))

            # Add to BedContainer
            bedContainerToReturn.addFrom_BedEntryObj(newBin)

        return bedContainerToReturn

    def extractLeftSide(self) -> None:
        """
        Reduce the feature to the left most bp.
        """
        self.eCoord = self.sCoord + 1

    def extractRightSide(self) -> None:
        """
        Reduce the feature to the right most bp.
        """
        self.sCoord = self.eCoord - 1

    def getReadsOverlapping(self, pysamObj: pysam.AlignmentFile) -> List[pysam.AlignedSegment]:
        """
        Returns the overlapping reads in a BAM file over the BedEntry region. Strandness is not taken into account.

        :param pysam.AlignmentFile pysamObj: A pysam AlignmentFile object with the BAM file to search the overlapping.
        :return List[pysam.AlignedSegment]: List with all the overlapping reads in pysam.AlignedSegment objects
        """
        readList = []
        for read in pysamObj.fetch(self.chr, self.sCoord, self.eCoord):
            readList.append(read)
        return readList

    ###########################
    ##  Build-in Functions   ##
    ###########################

    def __eq__(self, other):
        return self.chr == other.chr and \
               self.sCoord == other.sCoord and \
               self.eCoord == other.eCoord

    def __ge__(self, other):
        if self.chr != other.chr:
            return None
        return self.sCoord >= other.sCoord

    def __gt__(self, other):
        if self.chr != other.chr:
            return None
        return self.sCoord > other.sCoord

    def __lt__(self, other):
        if self.chr != other.chr:
            return None
        return self.sCoord < other.sCoord

    def __le__(self, other: object):
        if not isinstance(other, BedEntry):
            return NotImplemented
        if self.chr != other.chr:
            return None
        return self.sCoord <= other.sCoord

    def __len__(self):
        """
        Returns the size of BedEntry object region

        :return int: size of BedEntry object region
        """
        return self.eCoord - self.sCoord

    def __str__(self):
        """
        | Returns a string version of BedEntry 3 Col, like:
        | *chromosome* *<tab>* *start* *coordinate* *<tab>* *end* *coordinate*

        :return str: String representation of BedEntry 3 Col.
        """
        return "{}\t{}\t{}".format(self.chr, self.sCoord, self.eCoord)
