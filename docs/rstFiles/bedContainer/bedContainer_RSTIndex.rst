BedContainer Module
===================

Module Description
^^^^^^^^^^^^^^^^^^

The *BedContainer* Module is composed by 2 Classes.

* :py:class:`~bedContainer.BedContainer.BedContainer`
* :py:class:`~bedContainer.BedContainer6.BedContainer6`

:py:class:`~bedContainer.BedContainer.BedContainer` is the parent class of :py:class:`~bedContainer.BedContainer6.BedContainer6`, and so all
methods and attributes presented in :py:class:`~bedContainer.BedContainer.BedContainer` will be also present in
:py:class:`~bedContainer.BedContainer6.BedContainer6`. It was necessary overwriting some of them, so the way of working of some
methods can vary from one class to the other. But will share the same key features.


The internal structure of a *BedContainer* object is a **Dictionary of Lists**, each of one corresponding to one chromosome.
For some methods is possible to parallelize activities by running them for each chromosome individually.


Different *BedContainer* classes accommodate different *BedEntry* objects:

- :py:class:`~bedContainer.BedContainer.BedContainer` -> :py:class:`~bedEntry.BedEntry.BedEntry`
- :py:class:`~bedContainer.BedContainer6.BedContainer6` -> :py:class:`~bedEntry.BedEntry6.BedEntry6`


Classes Description and Methods Sum-up Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
    :maxdepth: 5

    bedContainer_SumUpTable
    bedContainer_Class

.. code-block:: python

    from bedContainer.BedContainer import BedContainer
    from bedContainer.BedContainer6 import BedContainer6
    from bedContainer.BedContainer12 import BedContainer12


    if __name__ == '__main__':
        """
        Create Instance of BedContainer
        """
        container1 = BedContainer6(addExtras=True)  # With extraFields
        container2 = BedContainer6(addExtras=False) # WithOUT extraFields

        """
        Read From BED files
        """
        container1.readFromBedFile("file1.bed")
        container2.readFromBedFile("file2.bed")

        """
        Sorting BedEntry objects
        """
        container1.sort()
        container1.sort()

        """
        Add new Entry
        """
        #Input as List:
        container1.addFrom_List(["A", 1, 2, "NAME", ".", "+",["A", "B", "C"]])

        #Input already a BedEntry object
        bedEntryObj = BedEntry6("chr1", 20, 50, 'GeneName',0, "+", ["A", "B" , "C","D"])
        container1.addFrom_BedEntryObj(bedEntryObj)

        """
        Remove a entry from BedContainer
        """
        container1.removeEntryBed(container1[0])

        """
        Merge 2 BedContainer
        """
        containerMerge = BedContainer6.merge(container2, container1)

        """

        It's also possible to iterate over the BedContainer
        """
        for elem in containerMerge:
            #Do something
            pass

        """
        Write in File BedContainer
        """
        containerMerge.writeToBedFile("FinalOutput.bed")

