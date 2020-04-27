from .BedEntry import BedEntry
from typing import TypeVar

BedContainer6 = TypeVar('BedContainer6')


class BedEntry6(BedEntry):
    """
    Represents a Bed line of Bed file, composed by 6 core column.

    """

    def __init__(self, chr, sCoord, eCoord, name, score, strand, extraFields=None):
        """

        :param str chr: chromosome name where region is located
        :param int sCoord: start coordinate of region
        :param int eCoord: end coordinate of region
        :param str name: name of genomic feature
        :param int score: score of genomic feature
        :param "+","-" strand: DNA strand where the region belongs
        :param None,List extraFields: Additional fields to the standard 6 columns. (optional)
        """
        super().__init__(chr, sCoord, eCoord, extraFields)
        self.name = name
        self.score = score
        self.strand = strand

    ###################
    ##  Properties   ##
    ###################

    @property
    def name(self):
        """
        Get the name (*name*) of genomic feature.

        :getter: Returns feature name
        :setter: Sets feature name.
        :type: string

        """
        return self._name

    @name.setter
    def name(self, value):
        if type(value) != str:
            raise ValueError("Name {} is not a string type.".format(value))
        self._name = value

    @name.deleter
    def name(self):
        self._name = None

    @property
    def score(self):
        """
        Get the score (*score*) of genomic feature.

        :getter: Returns feature score
        :setter: Sets feature score.
        :type: int

        """
        return self._score

    @score.setter
    def score(self, value):
        if type(value) != int:
            value = "."
        self._score = value

    @score.deleter
    def score(self):
        self._score = None

    @property
    def strand(self):
        """
        Get the genomic feature strand (*strand*)

        :getter: Returns feature strand
        :setter: Sets feature strand.
        :type: "+","-"

        """
        return self._strand

    @strand.setter
    def strand(self, value):
        if value not in ["+", "-"]:
            raise ValueError("Strand must to be \'+\' or \'-\'".format(value))
        self._strand = value

    @strand.deleter
    def strand(self):
        self._strand = None

    ##################
    ##  Functions   ##
    ##################

    def isOverlapping(self, other, considerStrand=False):
        """
        | Question the object if overlaps another object from *BedEntry6*.
        | Considered:

        - *chr*
        - *sCoord*
        - *eCoord*
        - *strand*

        :param BedEntry6 other: *BedEntry6* object to compare with.
        :param bool considerStrand: If *True* is only considered overlap if both features share the same DNA strand. (default *False*)
        :return bool: *True* if both objects overlap each other, *False* otherwise.
        """
        if considerStrand:
            if self.strand != other.strand:
                return False
        if self.chr == other.chr:
            return self.sCoord <= other.eCoord and other.sCoord <= self.eCoord
        return False

    def addLeftClip(self, value: int, considerStrand: bool = False) -> None:
        """
        Adds *value* number of bp to the BedEntry on the Left side.
        It means that if you gives *x* bp as input, it will set the sCoord to:

        sCoord = sCoord - value

        **However, if *considerStrand* is set as *True*** it adds the *x* bp on the 5' end, regardless is the left or right
        side of the BedEntry.

        When:

        - *strand* = "+" -> 5'end = Left side
        - *strand* = "-" -> 5'end = Right side

        :param bool considerStrand: if *True* the Left side is consider the 5'End.
        :param int value: Number of bp to increment on the Left side.
        """
        if not considerStrand:
            self.sCoord -= value
        else:
            if self.strand == "+":
                self.sCoord -= value
            else:
                self.eCoord += value

    def addRightClip(self, value: int, considerStrand: bool = False) -> None:
        """
        Adds *value* number of bp to the BedEntry on the Right side.
        It means that if you gives *x* bp as input, it will set the eCoord to:

        eCoord = eCoord + value

        **However, if *considerStrand* is set as *True*** it adds the *x* bp on the 3' end, regardless is the left or right
        side of the BedEntry.

        When:

        - *strand* = "+" -> 3'end = Right side
        - *strand* = "-" -> 3'end = Left side

        :param bool considerStrand: if *True* the Left side is consider the 3'End.
        :param int value: Number of bp to increment on the Right side
        """
        if not considerStrand:
            self.eCoord += value
        else:
            if self.strand == "+":
                self.eCoord += value
            else:
                self.sCoord -= value

    def shift(self, value: int, considerStrand: bool = False) -> None:
        """
        Shifts the Region *value* bp to the right if, *value* is positive, or to the left if *value* is negative.

        **However**, if ``considerStrand`` is set as ``True`` it shifts ``input`` bp **downstream** for positive ``input`` values,
        and **upstream** for negative ``input`` values, regardless is the left or right.

        When:

        - *strand* = "+" -> Positive ``value`` -> Shifts to the Right
        - *strand* = "-" -> Positive ``value`` -> Shifts to the Left
        - *strand* = "+" -> Negative ``value`` -> Shifts to the Left
        - *strand* = "-" -> Negative ``value`` -> Shifts to the Right

        :param bool considerStrand: if ``True``, positive *values* shifts downstream and *negative* values upstream, considering the strand.
        :param int value: Number of bp to shift the BedEntry region.
        """
        if not considerStrand:
            self.addLeftClip(-value)
            self.addRightClip(value)
        else:
            if self.strand == "+":
                self.addLeftClip(-value)
                self.addRightClip(value)
            else:
                self.addLeftClip(value)
                self.addRightClip(-value)

    def binRegion(self, nBin: int) -> BedContainer6:
        """
        Binning BedEntry in ``nBin`` number of *BedEntry* objects, returned in a *BedContainer*.

        :param int nBin: Number of bins to divide the *BedEntry* objects
        :return BedContainer: A *BedContainer* where are storage the *BedEntry* bins created
        """

        # Initialize BedContainer to return
        from bedContainer.BedContainer6 import BedContainer6

        bedContainerToReturn = BedContainer6(addExtras=True)
        quotient, remainder = divmod(len(self), nBin)
        number_bp_per_bin = [quotient + 1] * remainder + [quotient] * (nBin - remainder)
        int_sCoord = self.sCoord
        int_eCoord = self.sCoord
        for i in range(nBin):
            if i == 0:  # first cycle
                int_sCoord = self.sCoord
                int_eCoord += number_bp_per_bin[i]
            else:
                int_sCoord += number_bp_per_bin[i - 1]
                int_eCoord += number_bp_per_bin[i]

            # Create BedEntry object
            newBin = BedEntry6(self.chr, int_sCoord, int_eCoord, self.name, self.score, self.strand,
                               list(self.extraFields.values()))

            # Add to BedContainer
            bedContainerToReturn.addFrom_BedEntryObj(newBin)

        return bedContainerToReturn

    def extractLeftSide(self, considerStrand: bool = False):
        """
        Reduces the feature to the left most bp.

        **However**, if ``considerStrand`` is set as *True*:

            *Reduces the feature to TSS bp*
        """
        if not considerStrand:
            self.eCoord = self.sCoord + 1
        else:
            self.sCoord = self.eCoord - 1

    def extractRightSide(self, considerStrand: bool = False):
        """
        Reduce the feature to the right most bp.

        **However**, if ``considerStrand`` is set as *True*:

            *Reduces the feature to TES bp*
        """
        if not considerStrand:
            self.sCoord = self.eCoord - 1
        else:
            self.eCoord = self.sCoord + 1

    ###########################
    ##  Build-in Functions   ##
    ###########################

    def __eq__(self, other: object):
        """
        Return a *boolean* indicating if two *BedEntry6* objects share the same properties.

        - *chr*
        - *sCoord*
        - *eCoord*
        - *name*
        - *score*
        - *strand*

        (Extra Fields Not Included)

        :param BedEntry6 other: *BedEntry6* object to compare with.
        :return: *True* if they have same properties, *False* otherwise.
        :rtype: bool
        """
        if not isinstance(other, BedEntry6):
            return NotImplemented

        return self.chr == other.chr and \
               self.sCoord == other.sCoord and \
               self.eCoord == other.eCoord and \
               self.name == other.name and \
               self.score == other.score and \
               self.strand == other.strand

    def __str__(self):
        """
        Returns a string version of *BedEntry6*, like:

        *chromosome <tab> start coordinate <tab> end coordinate <tab> name <tab> score <tab> strand*

        :return: String representation of BedEntry 6 Col.
        """
        return "{}\t{}\t{}\t{}\t{}\t{}".format(self.chr, self.sCoord, self.eCoord, self.name, self.score, self.strand)
