from .BedEntry import BedEntry


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
