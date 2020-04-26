from bedEntry.BedEntry import BedEntry
from bedEntry.BedEntry6 import BedEntry6
from bedEntry.BedEntry12 import BedEntry12
import time

if __name__ == '__main__':
    a = BedEntry6("chr1", 20, 50, 'GeneName',0, "+")
    b = BedEntry6("chr1", 20, 50, 'GeneName',0, "-", ["A", "B" , "C","D"])

    i = 0
    start = time.time()
    x = []
    while i < 5000:
        i+=1
        x.append(BedEntry6("chr1", 5, 25, 'GeneName',0, "+", ["A"]))
        c = BedEntry6("chr1", 5, 25, 'GeneName',0, "-", ["A"])

    print(a.chr)
    print(a.sCoord)
    print(a.eCoord)
    print(a.name)
    print(a.score)
    print(a.strand)
    print(a.extraFields)

    print(b.extraFields)
    print(c.extraFields)

    print(a.isOverlapping(b))
    print(a.isOverlapping(b, considerStrand=True))

    print(a)

    a.shift(10);print(a)
    a.addClips(10);print(a)
    a.addLeftClip(10);print(a)
    a.addRightClip(10);print(a)

    print(b)
    b.shift(10);print(b)
    b.addClips(10);print(b)
    b.addLeftClip(10);print(b)
    b.addRightClip(10);print(b)

    print(b)
    b = BedEntry6("chr1", 20, 50, 'GeneName',0, "-", ["A", "B" , "C","D"])
    b.shift(-10, considerStrand=True);print(b)
    b.addClips(10);print(b)
    b.addLeftClip(100,considerStrand=True);print(b)
    b.addRightClip(10,considerStrand=True);print(b)

    b.binRegion(10)
    print("\n\nTime of execution: {}".format(time.time() - start))