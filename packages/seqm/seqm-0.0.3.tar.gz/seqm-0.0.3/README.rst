
|Build status| |Code coverage| |Maintenance yes| |GitHub license| |Documentation Status|

.. |Build status| image:: https://github.com/atgtag/seqm/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/atgtag/seqm/actions/workflows/ci.yml

.. |Code coverage| image:: https://codecov.io/gh/atgtag/seqm/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/atgtag/seqm

.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/atgtag/seqm/graphs/commit-activity

.. |GitHub license| image:: https://img.shields.io/github/license/atgtag/seqm
   :target: https://github.com/atgtag/seqm/blob/master/LICENSE

.. |Documentation Status| image:: https://readthedocs.org/projects/seqm/badge/?version=latest
   :target: http://seqm.readthedocs.io/?badge=latest


====
seqm
====

Python utilities for sequence comparison, quantification, and feature extraction.


Installation
============

.. code-block:: bash

    ~$ pip install seqm


Documentation
=============

Documentation for the package can be found `here <http://github.com/atgtag/seqm/latest/index.html>`_.


Usage
-----

The `seqm <http://github.com/atgtag/seqm/latest/index.html>`_ module contains functions for calculating sequence-related distance and complexity metrics, commonly used in language processing and next-generation sequencing. It has a simple and consistent API that be used for investigating sequence characteristics:

.. code-block:: python

    >>> import seqm
    >>> seqm.hamming('ATTATT', 'ATTAGT')
    1
    >>> seqm.edit('ATTATT', 'ATAGT')
    2
    >>> seqm.polydict('AAAACCGT')
    {'A': 4, 'C': 2, 'G': 1, 'T': 1}
    >>> seqm.polylength('AAAACCGT')
    4
    >>> seqm.entropy('AGGATAAG')
    1.40
    >>> seqm.gc_percent('AGGATAAG')
    0.375
    >>> seqm.gc_skew('AGGATAAG')
    3.0
    >>> seqm.gc_shift('AGGATAAG')
    1.67
    >>> seqm.dna_weight('AGGATAAG')
    3968.59
    >>> seqm.rna_weight('AGGATAAG')
    4082.59
    >>> seqm.aa_weight('AGGATAAG')
    700.8
    >>> seqm.tm('AGGATAAGAGATAGATTT')
    39.31
    >>> seqm.zipsize('AGGATAAGAGATAGATTT')
    22


It also has a ``Sequence`` object for object-based access to these properties:

.. code-block:: python

    >>> import seqm
    >>> seq = seqm.Sequence('AAAACCGT')
    >>> seq.hamming('AAAAGCGT')
    1
    >>> seq.gc_percent
    0.375
    >>> seq.revcomplement
    ACGTACGT
    >>> seq.dna_weight
    3895.59
    >>> # ... and so on ...


All of the metrics available in the repository are listed below, and can also be found in the `API <http://github.com/atgtag/seqm/latest/api.html>`_ section of the documentation.

Finally, all functions from the ``seqm`` module can be used at the command line:

.. code-block:: bash

    ~$ # calculate distance between sequences
    ~$ seqm edit AAAACCGT AAAAGCGT
    1

    ~$ # calculate gc percent of sequence
    ~$ seqm gc_percent AAAACCGT
    0.375

    ~$ # generate random sequence and pipe to `wrap` command
    ~$ seqm random --length 10 | seqm wrap --bases 5 -
    ATGGA
    TATTA


Sequence Quantification
+++++++++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Metric                                                     |
+=================================+============================================================+
| ``seqm.polydict``               | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| ``seqm.polylength``             | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.entropy``                | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_percent``             | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_skew``                | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| ``seqm.gc_shift``               | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.dna_weight``             | Molecular weight for sequence with DNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.rna_weight``             | Molecular weight for sequence with RNA backbone.           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.aa_weight``              | Molecular weight for amino acid sequence.                  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.tm``                     | Melting temperature of sequence.                           |
+---------------------------------+------------------------------------------------------------+
| ``seqm.zipsize``                | Compressibility of sequence.                               |
+---------------------------------+------------------------------------------------------------+


Domain Conversion
+++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Conversion                                                 |
+=================================+============================================================+
| ``seqm.revcomplement``          | Length of longest homopolymer for all bases in sequence.   |
+---------------------------------+------------------------------------------------------------+
| ``seqm.complement``             | Length of longest homopolymer in sequence.                 |
+---------------------------------+------------------------------------------------------------+
| ``seqm.aa``                     | Shannon entropy for bases in sequence.                     |
+---------------------------------+------------------------------------------------------------+
| ``seqm.wrap``                   | Percentage of GC bases in sequence relative to all bases.  |
+---------------------------------+------------------------------------------------------------+
| ``seqm.likelihood``             | GC skew for sequence:  (#G - #C)/(#G + #C).                |
+---------------------------------+------------------------------------------------------------+
| ``seqm.qscore``                 | GC shift for sequence: (#A + #T)/(#G + #C)                 |
+---------------------------------+------------------------------------------------------------+


Distance Metrics
++++++++++++++++

+---------------------------------+------------------------------------------------------------+
| Function                        | Distance Metric                                            |
+=================================+============================================================+
| ``seqm.hamming``                | Hamming distance between sequences.                        |
+---------------------------------+------------------------------------------------------------+
| ``seqm.edit``                   | Edit (levenshtein) distance between sequences              |
+---------------------------------+------------------------------------------------------------+


Utilities
+++++++++

+------------------------------------+------------------------------------------------------------+
| Function                           | Utility                                                    |
+====================================+============================================================+
| ``seqm.random_sequence``           | Generate random sequence.                                  |
+------------------------------------+------------------------------------------------------------+
| ``seqm.wrap``                      | Newline-wrap sequence                                      |
+------------------------------------+------------------------------------------------------------+


Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/atgtag/seqm/issues>`_.
