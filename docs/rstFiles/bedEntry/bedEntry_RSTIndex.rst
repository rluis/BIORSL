BedEntry Module
===============

Module Description
^^^^^^^^^^^^^^^^^^

The BedEntry Module is composed by 2 Classes.

* :py:class:`~bedEntry.BedEntry.BedEntry`
* :py:class:`~bedEntry.BedEntry6.BedEntry6`

:py:class:`~bedEntry.BedEntry.BedEntry` is the parent class of :py:class:`~bedEntry.BedEntry6.BedEntry6`, and so all
methods and attributes presented in :py:class:`~bedEntry.BedEntry.BedEntry` will be also present in
:py:class:`~bedEntry.BedEntry6.BedEntry6`. It was necessary overwriting some of them, so the way of working of some
methods can vary from one class to the other. But will share the same key features.

BedEntry 3 Columns
^^^^^^^^^^^^^^^^^^

:py:class:`~bedEntry.BedEntry.BedEntry` represents rows of BED files (`BED description <https://en.wikipedia.org/wiki/BED_(file_format)>`_),
composed by 3 columns, like the ones below:

.. code-block:: text

    Chr     sCoord eCoord
    chr1    100    200
    chr4    700    1000
    chr20   5000   10000
    ...

It is possible to add extra Fields to :py:class:`~bedEntry.BedEntry.BedEntry` objects, which should be given in a List
following the order you want to have them stored:

.. code-block:: text

    Chr     sCoord eCoord ExtraFields
    chr1    100    200    "A"   "B"   65432
    chr4    700    1000   1234  21    45
    chr20   5000   10000  "I"   "U"   "R"
    ...

BedEntry 6 Columns
^^^^^^^^^^^^^^^^^^

Like :py:class:`~bedEntry.BedEntry.BedEntry`, :py:class:`~bedEntry.BedEntry6.BedEntry6` represents rows of BED files
(`BED description`_). However, the rows are composed by 6 key columns, where it is also possible to add an additional column
with extraFields.

.. code-block:: text

    Chr     sCoord eCoord  Name     Score  Strand
    chr1    100    200     "Gene2"  .      "+"
    chr4    700    1000    "Gene2"  .      "-"
    chr20   5000   10000   "Gene3"  .      "+"
    ...


BedEntry 12 Columns
^^^^^^^^^^^^^^^^^^^

:py:class:`~bedEntry.BedEntry12.BedEntry12` is projected to be developed in the future,
representing BED files of 12 columns (`BED12 description <https://genome.ucsc.edu/FAQ/FAQformat.html#format1>`_).


Classes Description and Methods Sum-up Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
    :maxdepth: 5

    bedEntry_SumUpTable
    bedEntry_Class

Module Usage
^^^^^^^^^^^^

.. code-block:: python

    from bedEntry.BedEntry import BedEntry
    from bedEntry.BedEntry6 import BedEntry6
    # from bedEntry.BedEntry12 import BedEntry12 ## not available for now

    if __name__ == '__main__':
        """
        Create Instance of BedEntry
        """
        a = BedEntry6("chr1", 20, 50, 'GeneName',0, "+")
        b = BedEntry6("chr1", 20, 50, 'GeneName',0, "+", ["A", "B" , "C","D"])


        """
        Access to BedEntry6 object properties.
        """
        chr = a.chr
        start_coordinate = a.sCoord
        end_coordinate = a.eCoord
        name = a.name
        score = a.score
        strand = a.strand
        extraFields = a.extraFields


        """
        Playing around with BedEntry objects
        """

        #print BedEntry in a string
        print(a)

        #Get size of genomic region
        sizeRegion = len(a)

        #Change Genomic Region
        a.shift(10); print(a)        # Shift Region
        a.addClips(10); print(a)     # Add clips on both sides
        a.addLeftClip(10); print(a)  # Add clip on left side
        a.addRightClip(10); print(a) # Add clip on right side

        #Binning a BedEntry
        out_BedContainer = b.binRegion(10) # Binning in 10 bins

        #Get Edges bp
        b.extractLeftSide()                         # Return Left Most bp
        b.extractRightSide()                        # Return Right Most bp
        b.extractLeftSide(considerStrand=True)      # Return TSS bp
        b.extractRightSide(considerStrand=True)     # Return TES bp

