from .BedEntry6 import BedEntry6


class BedEntry12(BedEntry6):

    def __init__(self, chr, sCoord, eCoord, name, score, strand, thickStart, thickEnd, itemRgb, blockCount, blockSizes,
                 blockStarts, extraFields=None):
        super().__init__(chr, sCoord, eCoord, name, score, strand, extraFields)
        self.__thickStart = thickStart
        self.__thickEnd = thickEnd
        self.__itemRgb = itemRgb
        self.__blockCount = blockCount
        self.__blockSizes = blockSizes
        self.__blockStarts = blockStarts

    ###################
    ##  Properties   ##
    ###################

    # To develop later ...
