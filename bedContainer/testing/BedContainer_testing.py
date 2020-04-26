from bedContainer.BedContainer import BedContainer
from bedContainer.BedContainer6 import BedContainer6
from bedContainer.BedContainer12 import BedContainer12

import time

if __name__ == '__main__':
    start = time.time()
    container1 = BedContainer6(addExtras=True)
    container2 = BedContainer6(addExtras=True)

    print(container1)
    container1.sort()

    container1.readFromBedFile("HeLa_ExpressedGenes_proteinCoding_500-NoOverlap-2000.bed")
    print(container1)
    container1.sort()
    print(container1)
    print(container1[0])
    container1.removeEntryBed(container1[0])
    container1.addFrom_List(["A", 1, 2, "NAME", ".", "+",["A", "B", "C"]])
    print(container1.chrList)

    print("\n\n\n\n")
    print(list(filter( lambda x: x.chr == "A", container1))[0])
    print("\n\n\n\n")

    #container1.removeEntryBed(entry)



    print(container1.number_EntriesInChr("A"))
    print(container1.chrList)
    print(container1[0])
    print(container1)

    exit()

    container2.readFromBedFile("EXONS_ALL_Homo_sapiens.GRCh38.90_Wchr.bed")
    print(container1)
    container1.sort()
    print(container1)

    container1.writeToBedFile("AAAA")

    containerMerge = BedContainer6.merge(container2, container1)

    #containerMerge.writeToBedFile("AAAA")
    print(time.time() - start)
    container1.sort()
    print(time.time())
    #print(container2[500000])
    print(time.time())
    #print(container1[:10])

    container1.writeToBedFile("AAAA")

    exit()
    print(container1)
    print(container2)
    print(containerMerge)

    i=0
    for entry in containerMerge:
        i+=1
        print(entry)
        if i > 1000:
            break

    print(i)

    exit()
    i = 0
    for x in container1:
        #print(x)
        i+=1
    print(container1)

    print(time.time() - start)