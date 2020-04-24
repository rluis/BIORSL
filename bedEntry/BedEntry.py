
class BedEntry(object):

    #extraFields needs to be a List
    def __init__(self, chr, sCoord, eCoord, extraFields=None):
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
    def chr(self):
        return self._chr

    @chr.setter
    def chr(self, value):
        if type(value) != str:
            raise ValueError("Chromosome {} is not a string type.".format(value))
        self._chr = value

    @chr.deleter
    def chr(self):
        self._chr = None

    @property
    def sCoord(self):
        return self._sCoord

    @sCoord.setter
    def sCoord(self, value):
        if type(value) != int:
            raise ValueError("Start Position {} is not a integer type.".format(value))

        if hasattr(self, 'eCoord'):
            if value >= self.eCoord:
                raise ValueError("Start Coordinate higher or equal than End Coordinate")
        self._sCoord = value

    @sCoord.deleter
    def sCoord(self):
        self._sCoord = None

    @property
    def eCoord(self):
        return self._eCoord

    @eCoord.setter
    def eCoord(self, value):
        if not isinstance(value, int):
            raise ValueError("End Position {} is not a integer type.".format(value))
        if hasattr(self, 'sCoord'):
            if value <= self.sCoord:
                raise ValueError("End Coordinate lower or equal than Start Coordinate")
        self._eCoord = value

    @eCoord.deleter
    def eCoord(self):
        self._eCoord = None

    @property
    def extraFields(self):
        return self._extraFields

    @extraFields.setter
    def extraFields(self, value):
        self._extraFields = value

    @extraFields.deleter
    def extraFields(self):
        self._extraFields = {}


    ##################
    ##  Functions   ##
    ##################

    def addExtraField(self, extraField):
        n_extra_fields = self.lenExtraFields()
        self.extraFields[n_extra_fields] = extraField

    def hasExtraFields(self) -> bool:
        return self.lenExtraFields() > 0

    def lenExtraFields(self):
        return len(self.extraFields.keys())

    def isOverlapping(self, other):
        if self.chr == other.chr:
            return self.sCoord <= other.eCoord and other.sCoord <= self.eCoord
        return False



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
        return self.eCoord - self.sCoord

    def __str__(self):
        return "{}\t{}\t{}".format(self.chr, self.sCoord, self.eCoord)



