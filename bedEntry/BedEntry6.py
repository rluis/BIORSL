from .BedEntry import BedEntry


class BedEntry6(BedEntry):

    def __init__(self, chr, sCoord, eCoord, name, score, strand, extraFields=None):
        super().__init__(chr, sCoord, eCoord, extraFields)
        self.name = name
        self.score = score
        self.strand = strand

    ###################
    ##  Properties   ##
    ###################

    @property
    def name(self):
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
        if considerStrand:
            if self.strand != other.strand:
                return False
        if self.chr == other.chr:
            return self.sCoord <= other.eCoord and other.sCoord <= self.eCoord
        return False

    ###########################
    ##  Build-in Functions   ##
    ###########################

    def __eq__(self, other):
        return self.chr == other.chr and \
               self.sCoord == other.sCoord and \
               self.eCoord == other.eCoord and \
               self.name == other.name and \
               self.score == other.score and \
               self.strand == other.strand


    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}".format(self.chr, self.sCoord, self.eCoord, self.name, self.score, self.strand)
