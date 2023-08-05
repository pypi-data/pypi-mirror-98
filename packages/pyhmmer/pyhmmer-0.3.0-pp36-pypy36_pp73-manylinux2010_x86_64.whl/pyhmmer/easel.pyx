# coding: utf-8
# cython: language_level=3, linetrace=True
"""High-level interface to the Easel C library.

Easel is a library developed by the `Eddy/Rivas Lab <http://eddylab.org/>`_
to facilitate the development of biological software in C. It is used by
`HMMER <http://hmmer.org/>`_ and `Infernal <http://eddylab.org/infernal/>`_.

"""

# --- C imports --------------------------------------------------------------

cimport cython
from cpython.buffer cimport PyBUF_READ, PyBUF_WRITE
from cpython.memoryview cimport PyMemoryView_FromMemory
from cpython.unicode cimport PyUnicode_FromUnicode
from libc.stdint cimport int64_t, uint16_t, uint32_t
from libc.stdio cimport fclose
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy, memmove, strdup, strlen, strncpy
from posix.types cimport off_t

cimport libeasel
cimport libeasel.alphabet
cimport libeasel.bitfield
cimport libeasel.keyhash
cimport libeasel.msa
cimport libeasel.msafile
cimport libeasel.sq
cimport libeasel.sqio
cimport libeasel.sqio.ascii
cimport libeasel.ssi
from libeasel cimport ESL_DSQ, esl_pos_t
from libeasel.sq cimport ESL_SQ

DEF eslERRBUFSIZE = 128

IF UNAME_SYSNAME == "Linux":
    include "fileobj/linux.pxi"
ELIF UNAME_SYSNAME == "Darwin" or UNAME_SYSNAME.endswith("BSD"):
    include "fileobj/bsd.pxi"

# --- Python imports ---------------------------------------------------------

import os
import collections
import warnings

from .errors import AllocationError, UnexpectedError, AlphabetMismatch


# --- Cython classes ---------------------------------------------------------

cdef class Alphabet:
    """A biological alphabet, including additional marker symbols.

    This type is used to share an alphabet to several objects in the `easel`
    and `plan7` modules. Reference counting helps sharing the same instance
    everywhere, instead of reallocating memory every time an alphabet is
    needed.

    Use the factory class methods to obtain a default `Alphabet` for one of
    the three standard biological alphabets::

        >>> dna = Alphabet.dna()
        >>> rna = Alphabet.rna()
        >>> aa  = Alphabet.amino()

    """

    # --- Default constructors -----------------------------------------------

    cdef void _init_default(self, int ty):
        with nogil:
            self._abc = libeasel.alphabet.esl_alphabet_Create(ty)
        if not self._abc:
            raise AllocationError("ESL_ALPHABET")

    @classmethod
    def amino(cls):
        """amino(cls)\n--

        Create a default amino-acid alphabet.

        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslAMINO)
        return alphabet

    @classmethod
    def dna(cls):
        """dna(cls)\n--

        Create a default DNA alphabet.

        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslDNA)
        return alphabet

    @classmethod
    def rna(cls):
        """rna(cls)\n--

        Create a default RNA alphabet.

        """
        cdef Alphabet alphabet = Alphabet.__new__(Alphabet)
        alphabet._init_default(libeasel.alphabet.eslRNA)
        return alphabet

    # def __init__(self, str alphabet, int K, int Kp):
    #     buffer = alphabet.encode('ascii')
    #     self._alphabet = libeasel.alphabet.esl_alphabet_CreateCustom(<char*> buffer, K, Kp)
    #     if not self._alphabet:
    #         raise AllocationError("ESL_ALPHABET")

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._abc = NULL

    def __dealloc__(self):
        libeasel.alphabet.esl_alphabet_Destroy(self._abc)

    def __repr__(self):
        if self._abc.type == libeasel.alphabet.eslRNA:
            return "Alphabet.rna()"
        elif self._abc.type == libeasel.alphabet.eslDNA:
            return "Alphabet.dna()"
        elif self._abc.type == libeasel.alphabet.eslAMINO:
            return "Alphabet.amino()"
        else:
            return "Alphabet({!r}, K={!r}, Kp={!r})".format(
                self._abc.sym.decode('ascii'),
                self._abc.K,
                self._abc.Kp
            )

    def __eq__(self, object other):
        assert self._abc != NULL
        # TODO: Update when we implement custom alphabet creation from Python.
        if isinstance(other, Alphabet):
            return self._eq(<Alphabet> other)
        return NotImplemented

    def __getstate__(self):
        return {"type": self._abc.type}

    def __setstate__(self, state):
        self._init_default(state["type"])


    # --- Properties ---------------------------------------------------------

    @property
    def K(self):
        """`int`: The alphabet size, counting only actual alphabet symbols.

        Example:
            >>> Alphabet.dna().K
            4
            >>> Alphabet.amino().K
            20

        """
        return self._abc.K

    @property
    def Kp(self):
        """`int`: The complete alphabet size, including marker symbols.

        Example:
            >>> Alphabet.dna().Kp
            18
            >>> Alphabet.amino().Kp
            29

        """
        return self._abc.Kp

    @property
    def symbols(self):
        """`str`: The symbols composing the alphabet.

        Example:
            >>> Alphabet.dna().symbols
            'ACGT-RYMKSWHBVDN*~'
            >>> Alphabet.rna().symbols
            'ACGU-RYMKSWHBVDN*~'

        """
        cdef bytes symbols = self._abc.sym[:self._abc.Kp]
        return symbols.decode("ascii")

    # --- Utils --------------------------------------------------------------

    cdef inline bint _eq(self, Alphabet other) nogil:
        return self._abc.type == other._abc.type


cdef class Bitfield:
    """A statically sized sequence of booleans stored as a packed bitfield.

    A bitfield is instantiated with a fixed length, and all booleans are set
    to `False` by default::

        >>> bitfield = Bitfield(8)
        >>> len(bitfield)
        8
        >>> bitfield[0]
        False

    Use indexing to access and edit individual bits::

        >>> bitfield[0] = True
        >>> bitfield[0]
        True
        >>> bitfield[0] = False
        >>> bitfield[0]
        False

    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._b = NULL

    def __dealloc__(self):
        libeasel.bitfield.esl_bitfield_Destroy(self._b)

    def __init__(self, size_t length):
        """__init__(self, length)\n--

        Create a new bitfield with the given ``length``.

        """
        with nogil:
            self._b = libeasel.bitfield.esl_bitfield_Create(length)
        if not self._b:
            raise AllocationError("ESL_BITFIELD")

    def __len__(self):
        assert self._b != NULL
        return self._b.nb

    def __getitem__(self, int idx):
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(idx)
        return libeasel.bitfield.esl_bitfield_IsSet(self._b, index_)

    def __setitem__(self, index, value):
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(index)
        if value:
            libeasel.bitfield.esl_bitfield_Set(self._b, index_)
        else:
            libeasel.bitfield.esl_bitfield_Clear(self._b, index_)

    cdef size_t _wrap_index(self, int index) except -1:
        if index < 0:
            index += self._b.nb
        if index >= self._b.nb or index < 0:
            raise IndexError("bitfield index out of range")
        return <size_t> index

    cpdef size_t count(self, bint value=1):
        """count(self, value=True)\n--

        Count the number occurrences of ``value`` in the bitfield.

        If no argument is given, counts the number of `True` occurences.

        Example:
            >>> bitfield = Bitfield(8)
            >>> bitfield.count(False)
            8
            >>> bitfield[0] = bitfield[1] = True
            >>> bitfield.count()
            2

        """
        assert self._b != NULL
        cdef size_t count_
        with nogil:
            count_ = libeasel.bitfield.esl_bitfield_Count(self._b)
        return count_ if value else self._b.nb - count_

    cpdef void toggle(self, int index):
        """toggle(self, index)\n--

        Switch the value of one single bit.

        Example:
            >>> bitfield = Bitfield(8)
            >>> bitfield[0]
            False
            >>> bitfield.toggle(0)
            >>> bitfield[0]
            True
            >>> bitfield.toggle(0)
            >>> bitfield[0]
            False

        """
        assert self._b != NULL
        cdef size_t index_ = self._wrap_index(index)
        with nogil:
            libeasel.bitfield.esl_bitfield_Toggle(self._b, index_)


cdef class KeyHash:
    """A dynamically resized container to store byte keys using a hash table.

    Internally uses Bob Jenkins' *one at a time* hash, a simple and
    efficient hash function published in 1997 that exhibits
    `avalanche <https://en.wikipedia.org/wiki/Avalanche_effect>`_
    behaviour.

    Example:
        Add new keys to the key hash using the `~KeyHash.add` method
        like you would with a Python `set`::

            >>> kh = KeyHash()
            >>> kh.add(b"key")
            0

        Check if a key hash contains a given key::

            >>> b"key" in kh
            True
            >>> b"missing" in kh
            False

        Get the index associated with a key using the indexing notation::

            >>> kh[b"key"]
            0
            >>> kh[b"missing"]
            Traceback (most recent call last):
              ...
            KeyError: b'missing'

    See Also:
        The Wikipedia article for Bob Jenkins' hash functions:
        https://en.wikipedia.org/wiki/Jenkins_hash_function

    """

    def __cinit__(self):
        self._kh = NULL

    def __dealloc__(self):
        libeasel.keyhash.esl_keyhash_Destroy(self._kh)

    def __init__(self):
        """__init__(self)\n--

        Create a new empty key-hash collection.

        """
        with nogil:
            self._kh = libeasel.keyhash.esl_keyhash_Create()
        if not self._kh:
            raise AllocationError("ESL_KEYHASH")

    def __copy__(self):
        return self.copy()

    def __len__(self):
        assert self._kh != NULL
        return libeasel.keyhash.esl_keyhash_GetNumber(self._kh)

    def __contains__(self, object value):
        assert self._kh != NULL

        if not isinstance(value, bytes):
            return False

        cdef const char*  key    = value
        cdef       size_t length = len(value)

        with nogil:
            status = libeasel.keyhash.esl_keyhash_Lookup(self._kh, key, length, NULL)
        if status == libeasel.eslOK:
            return True
        elif status == libeasel.eslENOTFOUND:
            return False
        else:
            raise UnexpectedError(status, "esl_keyhash_Lookup")

    def __getitem__(self, bytes item):
        assert self._kh != NULL

        cdef const char*  key    = item
        cdef       size_t length = len(item)
        cdef       int    index

        with nogil:
            status = libeasel.keyhash.esl_keyhash_Lookup(self._kh, key, length, &index)
        if status == libeasel.eslOK:
            return index
        elif status == libeasel.eslENOTFOUND:
            raise KeyError(item)
        else:
            raise UnexpectedError(status, "esl_keyhash_Lookup")

    def __iter__(self):
        assert self._kh != NULL

        cdef int   i
        cdef int   offset
        cdef char* key

        for i in range(libeasel.keyhash.esl_keyhash_GetNumber(self._kh)):
            offset = self._kh.key_offset[i]
            key = &self._kh.smem[offset]
            yield <bytes> key

    cpdef int add(self, bytes key) except -1:
        """add(self, item)\n--

        Add a new key to the hash table, and return its index.

        If ``key`` was already in the hash table, the previous index is
        returned::

            >>> kh = KeyHash()
            >>> kh.add(b"first")
            0
            >>> kh.add(b"second")
            1
            >>> kh.add(b"first")
            0

        Arguments:
            key (`bytes`): The key to add to the hash table.

        Returns:
            `int`: The index corresponding to the added ``key``.

        .. versionadded:: 0.3.0

        """
        assert self._kh != NULL

        cdef       int    status
        cdef       int    index
        cdef const char*  k      = key
        cdef       size_t length = len(key)

        with nogil:
            status = libeasel.keyhash.esl_keyhash_Store(self._kh, k, length, &index)
        if status == libeasel.eslOK or status == libeasel.eslEDUP:
            return index
        else:
            raise UnexpectedError(status, "esl_keyhash_Store")

    cpdef void clear(self):
        """clear(self)\n--

        Remove all entries from the collection.

        """
        cdef int status
        with nogil:
            status = libeasel.keyhash.esl_keyhash_Reuse(self._kh)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_keyhash_Reuse")

    cpdef KeyHash copy(self):
        """copy(self)\n--

        Create and return an exact copy of this mapping.

        Example:
            >>> kh = KeyHash()
            >>> kh.add(b"key")
            0
            >>> copy = kh.copy()
            >>> b"key" in copy
            True

        """
        assert self._kh != NULL
        cdef KeyHash new = KeyHash.__new__(KeyHash)
        with nogil:
            new._kh = libeasel.keyhash.esl_keyhash_Clone(self._kh)
        if not new._kh:
            raise AllocationError("ESL_KEYHASH")
        return new


cdef class _MSASequences:
    """A read-only view over the individual sequences of an MSA.
    """

    def __cinit__(self):
        self.msa = None

    def __init__(self, MSA msa):
        self.msa = msa

    def __len__(self):
        assert self.msa._msa != NULL
        return self.msa._msa.nseq


@cython.freelist(8)
cdef class MSA:
    """An abstract alignment of multiple sequences.

    Hint:
        Use ``len(msa)`` to get the number of columns in the alignment,
        and ``len(msa.sequences)`` to get the number of sequences (i.e.
        the number of rows).

    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._msa = NULL

    def __dealloc__(self):
        libeasel.msa.esl_msa_Destroy(self._msa)

    def __init__(self):
        raise TypeError("Can't instantiate abstract class 'MSA'")

    def __copy__(self):
        return self.copy()

    def __eq__(self, object other):
        assert self._msa != NULL

        cdef int status
        cdef MSA other_msa

        if not isinstance(other, MSA):
            return NotImplemented

        other_msa = <MSA> other
        status = libeasel.msa.esl_msa_Compare(self._msa, other_msa._msa)

        if status == libeasel.eslOK:
            return True
        elif status == libeasel.eslFAIL:
            return False
        else:
            raise UnexpectedError(status, "esl_msa_Compare")

    def __len__(self):
        assert self._msa != NULL
        if self._msa.nseq == 0:
            return 0
        return self._msa.alen

    # --- Properties ---------------------------------------------------------

    @property
    def accession(self):
        """`bytes` or `None`: The accession of the alignment, if any.
        """
        assert self._msa != NULL
        if self._msa.acc == NULL:
            return None
        return <bytes> self._msa.acc

    @accession.setter
    def accession(self, bytes accession):
        assert self._msa != NULL

        cdef       int       status
        cdef       esl_pos_t length = len(accession)
        cdef const char*     acc    = accession

        with nogil:
            status = libeasel.msa.esl_msa_SetAccession(self._msa, acc, length)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetAccession")

    @property
    def author(self):
        """`bytes` or `None`: The author of the alignment, if any.
        """
        assert self._msa != NULL
        if self._msa.au == NULL:
            return None
        return <bytes> self._msa.au

    @author.setter
    def author(self, bytes author):
        assert self._msa != NULL

        cdef       int       status
        cdef       esl_pos_t length = len(author)
        cdef const char*     au   = author

        with nogil:
            status = libeasel.msa.esl_msa_SetAuthor(self._msa, au, length)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetAuthor")

    @property
    def name(self):
        """`bytes` or `None`: The name of the alignment, if any.
        """
        assert self._msa != NULL
        if self._msa.name == NULL:
            return None
        return <bytes> self._msa.name

    @name.setter
    def name(self, bytes name):
        assert self._msa != NULL

        cdef       int       status
        cdef       esl_pos_t length = len(name)
        cdef const char*     nm     = name

        with nogil:
            status = libeasel.msa.esl_msa_SetName(self._msa, nm, length)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetName")

    @property
    def description(self):
        """`bytes` or `None`: The description of the sequence, if any.
        """
        assert self._msa != NULL
        if self._msa.desc == NULL:
            return None
        return <bytes> self._msa.desc

    @description.setter
    def description(self, bytes description):
        assert self._msa != NULL

        cdef       int       status
        cdef       esl_pos_t length = len(description)
        cdef const char*     desc   = description

        with nogil:
            status = libeasel.msa.esl_msa_SetDesc(self._msa, desc, length)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetDesc")

    # --- Utils --------------------------------------------------------------

    cdef int _rehash(self) nogil except 1:
        """Rehash the sequence names for faster lookup.
        """
        cdef int status = libeasel.msa.esl_msa_Hash(self._msa)
        if status == libeasel.eslOK:
            return 0
        else:
            raise UnexpectedError(status, "esl_msa_Hash")

    # --- Methods ------------------------------------------------------------

    cpdef uint32_t checksum(self):
        """checksum(self)\n--

        Calculate a 32-bit checksum for the multiple sequence alignment.

        """
        cdef uint32_t checksum = 0
        cdef int status
        with nogil:
            status = libeasel.msa.esl_msa_Checksum(self._msa, &checksum)
        if status == libeasel.eslOK:
            return checksum
        else:
            raise UnexpectedError(status, "esl_msa_Checksum")

    cpdef void write(self, object fh, str format) except *:
        """write(self, fh, format)\n--

        Write the multiple sequence alignement to a file handle.

        Arguments:
            fh (`io.IOBase`): A Python file handle, opened in binary mode.
            format (`str`): The name of the multiple sequence alignment
                file format to use.

        .. versionadded:: 0.3.0

        """
        assert self._msa != NULL

        cdef int    status
        cdef int    fmt
        cdef FILE*  file

        if format not in MSAFile._formats:
            raise ValueError("Invalid MSA format: {!r}".format(format))

        fmt = MSAFile._formats[format]
        file = fopen_obj(fh, mode="w")
        status = libeasel.msafile.esl_msafile_Write(file, self._msa, fmt)
        fclose(file)

        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sqascii_WriteFasta")


cdef class _TextMSASequences(_MSASequences):
    """A read-only view over the sequences of an MSA in text mode.
    """

    def __init__(self, TextMSA msa):
        self.msa = msa

    def __getitem__(self, int idx):
        assert self.msa._msa != NULL

        cdef int          status
        cdef TextSequence seq

        if idx < 0:
            idx += self.msa._msa.nseq
        if idx >= self.msa._msa.nseq or idx < 0:
            raise IndexError("list index out of range")

        seq = TextSequence.__new__(TextSequence)
        status = libeasel.sq.esl_sq_FetchFromMSA(self.msa._msa, idx, &seq._sq)

        if status == libeasel.eslOK:
            return seq
        else:
            raise UnexpectedError(status, "esl_sq_FetchFromMSA")

    def __setitem__(self, int idx, TextSequence seq):
        assert self.msa is not None
        assert seq._sq != NULL

        cdef int status
        cdef int hash_index

        if idx < 0:
            idx += self.msa._msa.nseq
        if idx >= self.msa._msa.nseq or idx < 0:
            raise IndexError("list index out of range")

        # make sure the sequence has a name
        if seq.name is None:
            raise ValueError("cannot set an alignment sequence with an empty name")

        # make sure the sequence has the right length
        if len(seq) != len(self.msa):
            raise ValueError("sequence does not have the expected length")

        # make sure inserting the sequence will not create a name duplicate
        status = libeasel.keyhash.esl_keyhash_Lookup(
            self.msa._msa.index,
            seq._sq.name,
            -1,
            &hash_index
        )
        if status == libeasel.eslOK and hash_index != idx:
            raise ValueError("cannot set a sequence with a duplicate name")

        # set the new sequence
        with nogil:
            (<TextMSA> self.msa)._set_sequence(idx, (<TextSequence> seq)._sq)
            if hash_index != idx:
                self.msa._rehash()


cdef class TextMSA(MSA):
    """A multiple sequence alignement stored in text mode.
    """

    # --- Magic methods ------------------------------------------------------

    def __init__(
        self,
        bytes name=None,
        bytes description=None,
        bytes accession=None,
        object sequences=None,
        bytes author=None,
    ):
        """__init__(self, name=None, description=None, accession=None, sequences=None, author=None)\n--

        Create a new text-mode alignment with the given ``sequences``.

        Arguments:
            name (`bytes`, optional): The name of the alignment, if any.
            description (`bytes`, optional): The description of the
                alignment, if any.
            accession (`bytes`, optional): The accession of the alignment,
                if any.
            sequences (iterable of `TextSequence`): The sequences to store
                in the multiple sequence alignment. All sequences must have
                the same length. They also need to have distinct names.
            author (`bytes`, optional): The author of the alignment, often
                used to record the aligner it was created with.

        Raises:
            `ValueError`: When the alignment cannot be created from the
                given sequences.
            `TypeError`: When ``sequences`` is not an iterable of
                `TextSequence` objects.

        Example:
            >>> s1 = TextSequence(name=b"seq1", sequence="ATGC")
            >>> s2 = TextSequence(name=b"seq2", sequence="ATGC")
            >>> msa = TextMSA(name=b"msa", sequences=[s1, s2])
            >>> len(msa)
            4

        .. versionchanged:: 0.3.0
           Allow creating an alignment from an iterable of `TextSequence`.

        """
        cdef list    seqs  = [] if sequences is None else list(sequences)
        cdef set     names = { seq.name for seq in seqs }
        cdef int64_t alen  = len(seqs[0]) if seqs else -1
        cdef int     nseq  = len(seqs) if seqs else 1

        if len(names) != len(seqs):
            raise ValueError("duplicate names in alignment sequences")

        for seq in seqs:
            if not isinstance(seq, TextSequence):
                ty = type(seq).__name__
                raise TypeError(f"expected TextSequence, found {ty}")
            elif len(seq) != alen:
                raise ValueError("all sequences must have the same length")

        with nogil:
            self._msa = libeasel.msa.esl_msa_Create(nseq, alen)
        if self._msa == NULL:
            raise AllocationError("ESL_MSA")

        if name is not None:
            self.name = name
        if accession is not None:
            self.accession = accession
        if description is not None:
            self.description = description
        if author is not None:
            self.author = author
        for i, seq in enumerate(seqs):
            self._set_sequence(i, (<TextSequence> seq)._sq)

    # --- Properties ---------------------------------------------------------

    @property
    def sequences(self):
        """`_TextMSASequences`: A view of the sequences in the alignment.

        This property lets you access the individual sequences in the
        multiple sequence alignment as `TextSequence` instances.

        Example:
            Query the number of sequences in the alignment with `len`, or
            access individual members via indexing notation::

                >>> s1 = TextSequence(name=b"seq1", sequence="ATGC")
                >>> s2 = TextSequence(name=b"seq2", sequence="ATGC")
                >>> msa = TextMSA(name=b"msa", sequences=[s1, s2])
                >>> len(msa.sequences)
                2
                >>> msa.sequences[0].name
                b'seq1'

        Caution:
            Sequences in the list are copies, so editing their attributes
            will have no effect on the alignment::

                >>> msa.sequences[0].name
                b'seq1'
                >>> msa.sequences[0].name = b"seq1bis"
                >>> msa.sequences[0].name
                b'seq1'

            Support for this feature will be added in a future version, but
            can be circumvented for now by forcingly setting the updated
            version of the object::

                >>> seq = msa.sequences[0]
                >>> seq.name = b"seq1bis"
                >>> msa.sequences[0] = seq
                >>> msa.sequences[0].name
                b'seq1bis'

        .. versionadded:: 0.3.0

        """
        return _TextMSASequences(self)

    # --- Utils --------------------------------------------------------------

    cdef int _set_sequence(self, int idx, ESL_SQ* seq) nogil except 1:
        # assert seq.seq != NULL

        cdef int status

        status = libeasel.msa.esl_msa_SetSeqName(self._msa, idx, seq.name, -1)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetSeqName")

        if seq.acc[0] != b'\0':
            status = libeasel.msa.esl_msa_SetSeqAccession(self._msa, idx, seq.acc, -1)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_SetSeqAccession")

        if seq.desc[0] != b'\0':
            status = libeasel.msa.esl_msa_SetSeqDescription(self._msa, idx, seq.desc, -1)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_SetSeqDescription")

        # assert self._msa.aseq[idx] != NULL
        strncpy(self._msa.aseq[idx], seq.seq, self._msa.alen)
        return 0

    # --- Methods ------------------------------------------------------------

    cpdef TextMSA copy(self):
        """copy(self)\n--

        Duplicate the text sequence alignment, and return the copy.

        """
        assert self._msa != NULL
        assert not (self._msa.flags & libeasel.msa.eslMSA_DIGITAL)

        cdef int status
        cdef TextMSA new = TextMSA.__new__(TextMSA)
        with nogil:
            new._msa = libeasel.msa.esl_msa_Create(self._msa.nseq, self._msa.alen)
        if new._msa == NULL:
            raise AllocationError("ESL_MSA")

        with nogil:
            status = libeasel.msa.esl_msa_Copy(self._msa, new._msa)
        if status == libeasel.eslOK:
            return new
        else:
            raise UnexpectedError(status, "esl_msa_Copy")

    cpdef DigitalMSA digitize(self, Alphabet alphabet):
        """digitize(self, alphabet)\n--

        Convert the text alignment to a digital alignment using ``alphabet``.

        Returns:
            `DigitalMSA`: An alignment in digital mode containing the same
            sequences digitized with ``alphabet``.

        """
        assert self._msa != NULL

        cdef int status
        cdef DigitalMSA new

        new = DigitalMSA.__new__(DigitalMSA, alphabet)
        with nogil:
            new._msa = libeasel.msa.esl_msa_CreateDigital(
                alphabet._abc,
                self._msa.nseq,
                self._msa.alen
            )
            if new._msa == NULL:
                raise AllocationError("ESL_MSA")

            status = libeasel.msa.esl_msa_Copy(self._msa, new._msa)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_Copy")

        assert new._msa.flags & libeasel.msa.eslMSA_DIGITAL
        return new


cdef class _DigitalMSASequences(_MSASequences):
    """A read-only view over the sequences of an MSA in digital mode.
    """

    def __init__(self, DigitalMSA msa):
        self.msa = msa
        self.alphabet = msa.alphabet

    def __getitem__(self, int idx):
        assert self.msa._msa != NULL

        cdef int             status
        cdef DigitalSequence seq

        if idx < 0:
            idx += self.msa._msa.nseq
        if idx >= self.msa._msa.nseq:
            raise IndexError("list index out of range")

        seq = DigitalSequence.__new__(DigitalSequence, self.alphabet)
        status = libeasel.sq.esl_sq_FetchFromMSA(self.msa._msa, idx, &seq._sq)

        if status == libeasel.eslOK:
            return seq
        else:
            raise UnexpectedError(status, "esl_sq_FetchFromMSA")

    def __setitem__(self, int idx, DigitalSequence seq):
        assert self.msa is not None
        assert seq._sq != NULL

        cdef int status
        cdef int hash_index

        if idx < 0:
            idx += self.msa._msa.nseq
        if idx >= self.msa._msa.nseq or idx < 0:
            raise IndexError("list index out of range")

        # make sure the sequence has a name
        if seq.name is None:
            raise ValueError("cannot set an alignment sequence with an empty name")

        # make sure the sequence has the right length
        if len(seq) != len(self.msa):
            raise ValueError("sequence does not have the expected length")

        # make sure the sequence has the right alphabet
        if not self.msa.alphabet._eq(seq.alphabet):
            raise AlphabetMismatch(self.msa.alphabet, seq.alphabet)

        # make sure inserting the sequence will not create a name duplicate
        status = libeasel.keyhash.esl_keyhash_Lookup(
            self.msa._msa.index,
            seq._sq.name,
            -1,
            &hash_index
        )
        if status == libeasel.eslOK and hash_index != idx:
            raise ValueError("cannot set a sequence with a duplicate name")

        # set the new sequence
        with nogil:
            (<TextMSA> self.msa)._set_sequence(idx, (<TextSequence> seq)._sq)
            if hash_index != idx:
                self.msa._rehash()


cdef class DigitalMSA(MSA):
    """A multiple sequence alignment stored in digital mode.

    Attributes:
        alphabet (`Alphabet`): The biological alphabet used to encode this
            sequence alignment to digits.

    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self, Alphabet alphabet, *args, **kwargs):
        self._msa = NULL
        self.alphabet = alphabet

    def __init__(
        self,
        Alphabet alphabet,
        bytes name=None,
        bytes description=None,
        bytes accession=None,
        object sequences=None,
        bytes author=None,
    ):
        """__init__(self, alphabet, name=None, description=None, accession=None, sequences=None, author=None)\n--

        Create a new digital-mode alignment with the given ``sequences``.

        Arguments:
            alphabet (`Alphabet`): The alphabet of the alignmed sequences.
            name (`bytes`, optional): The name of the alignment, if any.
            description (`bytes`, optional): The description of the
                alignment, if any.
            accession (`bytes`, optional): The accession of the alignment,
                if any.
            sequences (iterable of `DigitalSequence`): The sequences to
                store in the multiple sequence alignment. All sequences must
                have the same length and alphabet. They also need to have
                distinct names set.
            author (`bytes`, optional): The author of the alignment, often
                used to record the aligner it was created with.

        .. versionchanged:: 0.3.0
           Allow creating an alignment from an iterable of `DigitalSequence`.

        """
        cdef list    seqs  = [] if sequences is None else list(sequences)
        cdef set     names = { seq.name for seq in seqs }
        cdef int64_t alen  = len(seqs[0]) if seqs else -1
        cdef int     nseq  = len(seqs) if seqs else 1

        if len(names) != len(seqs):
            raise ValueError("duplicate names in alignment sequences")

        for seq in seqs:
            if not isinstance(seq, DigitalSequence):
                ty = type(seq).__name__
                raise TypeError(f"expected DigitalSequence, found {ty}")
            elif len(seq) != alen:
                raise ValueError("all sequences must have the same length")
            elif not alphabet._eq(seq.alphabet):
                raise AlphabetMismatch(alphabet, seq.alphabet)

        self.alphabet = alphabet
        with nogil:
            self._msa = libeasel.msa.esl_msa_CreateDigital(alphabet._abc, nseq, alen)
        if self._msa == NULL:
            raise AllocationError("ESL_MSA")

        if name is not None:
            self.name = name
        if accession is not None:
            self.accession = accession
        if description is not None:
            self.description = description
        if author is not None:
            self.author = author
        for i, seq in enumerate(seqs):
            self._set_sequence(i, (<DigitalSequence> seq)._sq)


    # --- Properties ---------------------------------------------------------

    @property
    def sequences(self):
        """`_DigitalMSASequences`: A view of the sequences in the alignment.

        This property lets you access the individual sequences in the
        multiple sequence alignment as `DigitalSequence` instances.

        See Also:
            The documentation for the `TextMSA.sequences` property, which
            contains some additional information.

        .. versionadded:: 0.3.0

        """
        return _DigitalMSASequences(self)

    # --- Utils --------------------------------------------------------------

    cdef int _set_sequence(self, int idx, ESL_SQ* seq) nogil except 1:
        # assert seq.dsq != NULL

        cdef int status

        status = libeasel.msa.esl_msa_SetSeqName(self._msa, idx, seq.name, -1)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msa_SetSeqName")

        if seq.acc[0] != b'\0':
            status = libeasel.msa.esl_msa_SetSeqAccession(self._msa, idx, seq.acc, -1)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_SetSeqAccession")

        if seq.desc[0] != b'\0':
            status = libeasel.msa.esl_msa_SetSeqDescription(self._msa, idx, seq.desc, -1)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_SetSeqDescription")

        # assert self._msa.ax[idx] != NULL
        memcpy(self._msa.ax[idx], seq.dsq, self._msa.alen+2)
        return 0

    # --- Methods ------------------------------------------------------------

    cpdef DigitalMSA copy(self):
        """Duplicate the digital sequence alignment, and return the copy.
        """
        assert self._msa != NULL
        assert self._msa.flags & libeasel.msa.eslMSA_DIGITAL

        cdef int           status
        cdef ESL_ALPHABET* abc    = self.alphabet._abc
        cdef DigitalMSA    new    = DigitalMSA.__new__(DigitalMSA, self.alphabet)

        with nogil:
            new._msa = libeasel.msa.esl_msa_CreateDigital(
                abc,
                self._msa.nseq,
                self._msa.alen
            )
            if new._msa == NULL:
                raise AllocationError("ESL_MSA")
            status = libeasel.msa.esl_msa_Copy(self._msa, new._msa)

        if status == libeasel.eslOK:
            return new
        else:
            raise UnexpectedError(status, "esl_msa_Copy")

    cpdef TextMSA textize(self):
        """textize(self)\n--

        Convert the digital alignment to a text alignment.

        Returns:
            `TextMSA`: A copy of the alignment in text-mode.

        .. versionadded:: 0.3.0

        """
        assert self._msa != NULL

        cdef int     status
        cdef TextMSA new

        new = TextMSA.__new__(TextMSA)
        with nogil:
            new._msa = libeasel.msa.esl_msa_Create(
                self._msa.nseq,
                self._msa.alen
            )
            if new._msa == NULL:
                raise AllocationError("ESL_MSA")

            status = libeasel.msa.esl_msa_Copy(self._msa, new._msa)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_msa_Copy")

        assert not (new._msa.flags & libeasel.msa.eslMSA_DIGITAL)
        return new


cdef class MSAFile:
    """A wrapper around a multiple-alignment file.

    This class supports reading sequences stored in different formats, such
    as Stockholm, A2M, PSI-BLAST or Clustal.

    """

    _formats = {
        "stockholm": libeasel.msafile.eslMSAFILE_STOCKHOLM,
        "pfam": libeasel.msafile.eslMSAFILE_PFAM,
        "a2m": libeasel.msafile.eslMSAFILE_A2M,
        "psiblast": libeasel.msafile.eslMSAFILE_PSIBLAST,
        "selex": libeasel.msafile.eslMSAFILE_SELEX,
        "afa": libeasel.msafile.eslMSAFILE_AFA,
        "clustal": libeasel.msafile.eslMSAFILE_CLUSTAL,
        "clustallike": libeasel.msafile.eslMSAFILE_CLUSTALLIKE,
        "phylip": libeasel.msafile.eslMSAFILE_PHYLIP,
        "phylips": libeasel.msafile.eslMSAFILE_PHYLIPS,
    }


    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self.alphabet = None
        self._msaf = NULL

    def __init__(self, str file, str format = None):
        cdef int fmt = libeasel.msafile.eslMSAFILE_UNKNOWN
        if format is not None:
            format_ = format.lower()
            if format_ not in self._formats:
                raise ValueError("Invalid MSA format: {!r}".format(format))
            fmt = self._formats[format_]

        cdef bytes fspath = os.fsencode(file)
        cdef int status = libeasel.msafile.esl_msafile_Open(NULL, fspath, NULL, fmt, NULL, &self._msaf)
        if status == libeasel.eslENOTFOUND:
            raise FileNotFoundError(2, "No such file or directory: {!r}".format(file))
        elif status == libeasel.eslEMEM:
            raise AllocationError("ESL_MSAFILE")
        elif status == libeasel.eslEFORMAT:
            if format is None:
                raise ValueError("Could not determine format of file: {!r}".format(file))
            else:
                raise EOFError("Sequence file is empty")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_msafile_Open")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        seq = self.read()
        if seq is None:
            raise StopIteration()
        return seq


    # --- Read methods -------------------------------------------------------

    cpdef MSA read(self):
        """read(self)\n--

        Read the next alignment from the file.

        Returns:
            `MSA`: The next alignment in the file, or `None` if all the
            alignments were read from the file already.

        Raises:
            `ValueError`: When attempting to read an alignment from a closed
                file, or when the file could not be parsed.

        Hint:
            This method allocates a new alignment, which is not efficient in
            case the sequences are being read within a tight loop. Use
            `SequenceFile.readinto` with an already initialized `Sequence`
            if you can to recycle the internal buffers.

        """
        cdef MSA msa

        if self.alphabet is not None:
            msa = DigitalMSA.__new__(DigitalMSA, self.alphabet)
        else:
            msa = TextMSA.__new__(TextMSA)

        if self._msaf == NULL:
            raise ValueError("I/O operation on closed file.")
        else:
            status = libeasel.msafile.esl_msafile_Read(self._msaf, &msa._msa)

        if status == libeasel.eslOK:
            return msa
        elif status == libeasel.eslEOF:
            return None
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> self._msaf.errmsg
            raise ValueError("Could not parse file: {}".format(msg.decode()))
        else:
            raise UnexpectedError(status, "esl_msafile_Read")


    # --- Utils --------------------------------------------------------------

    cpdef void close(self):
        """close(self)\n--

        Close the file and free the resources used by the parser.

        """
        libeasel.msafile.esl_msafile_Close(self._msaf)
        self._msaf = NULL

    cpdef Alphabet guess_alphabet(self):
        """guess_alphabet(self)\n--

        Guess the alphabet of an open `MSAFile`.

        This method tries to guess the alphabet of a multiple-alignment file
        by inspecting the first entry in the file. It returns the alphabet,
        or `None` if the file alphabet cannot be reliably guessed.

        Raises:
            `EOFError`: if the file is empty.
            `OSError`: if a parse error occurred.
            `ValueError`: if this methods is called after the file was closed.

        """
        cdef int ty
        cdef int status
        cdef Alphabet alphabet

        if self._msaf == NULL:
            raise ValueError("I/O operation on closed file.")

        status = libeasel.msafile.esl_msafile_GuessAlphabet(self._msaf, &ty)
        if status == libeasel.eslOK:
            alphabet = Alphabet.__new__(Alphabet)
            alphabet._init_default(ty)
            return alphabet
        elif status == libeasel.eslENOALPHABET:
            return None
        elif status == libeasel.eslENODATA:
            raise EOFError("Sequence file appears to be empty.")
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> self._msaf.errmsg
            raise ValueError("Could not parse file: {}".format(msg.decode()))
        else:
            raise UnexpectedError(status, "esl_msafile_GuessAlphabet")

    cpdef void set_digital(self, Alphabet alphabet):
        """set_digital(self, alphabet)\n--

        Set the `MSAFile` to read in digital mode with ``alphabet``.

        This method can be called even after the first alignment have been
        read; it only affects subsequent sequences in the file.

        """
        if self._msaf == NULL:
            raise ValueError("I/O operation on closed file.")

        cdef int status = libeasel.msafile.esl_msafile_SetDigital(self._msaf, alphabet._abc)
        if status == libeasel.eslOK:
            self.alphabet = alphabet
        else:
            raise UnexpectedError(status, "esl_msafile_SetDigital")


@cython.freelist(8)
cdef class Sequence:
    """An abstract biological sequence with some associated metadata.

    Easel provides two different mode to store a sequence: text, or digital.
    In the HMMER code, changing from one mode to another mode is done in
    place, which allows recycling memory. However, doing so can be confusing
    since there is no way to know statically the representation of a sequence.

    To avoid this, ``pyhmmer`` provides two subclasses of the `Sequence`
    abstract class to maintain the mode contract: `TextSequence` and
    `DigitalSequence`. Functions expecting sequences in digital format, like
    `pyhmmer.hmmsearch`, can then use Python type system to make sure they
    receive sequences in the right mode. This allows type checkers such as
    ``mypy`` to detect potential contract breaches at compile-time.

    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._sq = NULL

    def __init__(self):
        raise TypeError("Can't instantiate abstract class 'Sequence'")

    def __dealloc__(self):
        libeasel.sq.esl_sq_Destroy(self._sq)

    def __eq__(self, object other):
        assert self._sq != NULL

        cdef int      status
        cdef Sequence other_sq

        if not isinstance(other, Sequence):
            return NotImplemented

        other_sq = <Sequence> other
        status = libeasel.sq.esl_sq_Compare(self._sq, other_sq._sq)

        if status == libeasel.eslOK:
            return True
        elif status == libeasel.eslFAIL:
            return False
        else:
            raise UnexpectedError(status, "esl_sq_Compare")

    def __len__(self):
        assert self._sq != NULL
        if self._sq.n == -1:
            return 0
        return <int> self._sq.n

    def __copy__(self):
        return self.copy()


    # --- Properties ---------------------------------------------------------

    @property
    def accession(self):
        """`bytes`: The accession of the sequence.
        """
        assert self._sq != NULL
        return <bytes> self._sq.acc

    @accession.setter
    def accession(self, bytes accession):
        assert self._sq != NULL

        cdef       int   status
        cdef const char* acc    = accession

        with nogil:
            status = libeasel.sq.esl_sq_SetAccession(self._sq, acc)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetAccession")

    @property
    def name(self):
        """`bytes`: The name of the sequence.
        """
        assert self._sq != NULL
        return <bytes> self._sq.name

    @name.setter
    def name(self, bytes name):
        assert self._sq != NULL

        cdef       int   status
        cdef const char* nm     = name

        with nogil:
            status = libeasel.sq.esl_sq_SetName(self._sq, nm)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetName")

    @property
    def description(self):
        """`bytes`: The description of the sequence.
        """
        assert self._sq != NULL
        return <bytes> self._sq.desc

    @description.setter
    def description(self, bytes description):
        assert self._sq != NULL

        cdef       int   status
        cdef const char* desc   = description

        with nogil:
            status = libeasel.sq.esl_sq_SetDesc(self._sq, desc)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetDesc")

    @property
    def source(self):
        """`bytes`: The source of the sequence, if any.
        """
        return <bytes> self._sq.source

    @source.setter
    def source(self, bytes source):
        assert self._sq != NULL

        cdef       int   status
        cdef const char* src    = source

        with nogil:
            status = libeasel.sq.esl_sq_SetSource(self._sq, src)
        if status == libeasel.eslEMEM:
            raise AllocationError("char*")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_SetSource")


    # --- Abstract methods ---------------------------------------------------

    def copy(self):
        """copy(self)\n--

        Duplicate the sequence, and return the copy.

        """
        raise NotImplementedError("Sequence.copy")


    # --- Methods ------------------------------------------------------------

    cpdef uint32_t checksum(self):
        """checksum(self)\n--

        Calculate a 32-bit checksum for the sequence.

        """
        assert self._sq != NULL

        cdef int      status
        cdef uint32_t checksum = 0

        with nogil:
            status = libeasel.sq.esl_sq_Checksum(self._sq, &checksum)
        if status == libeasel.eslOK:
            return checksum
        else:
            raise UnexpectedError(status, "esl_sq_Checksum")

    cpdef void clear(self):
        """clear(self)\n--

        Reinitialize the sequence for re-use.

        """
        assert self._sq != NULL

        cdef int status

        with nogil:
            status = libeasel.sq.esl_sq_Reuse(self._sq)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_Reuse")

    cpdef void write(self, object fh) except *:
        """write(self, fh)\n--

        Write the sequence alignement to a file handle, in FASTA format.

        Arguments:
            fh (`io.IOBase`): A Python file handle, opened in binary mode.

        .. versionadded:: 0.3.0

        """
        assert self._sq != NULL

        cdef int    status
        cdef FILE*  file   = fopen_obj(fh, mode="w")

        status = libeasel.sqio.ascii.esl_sqascii_WriteFasta(file, self._sq, False)
        fclose(file)
        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sqascii_WriteFasta")


cdef class TextSequence(Sequence):
    """A biological sequence stored in text mode.

    Hint:
        Use the ``sequence`` property to access the sequence letters as a
        Python string.

    """

    def __init__(
        self,
        bytes name=None,
        bytes description=None,
        bytes accession=None,
        str   sequence=None,
        bytes source=None,
    ):
        """__init__(self, name=None, description=None, accession=None, sequence=None, source=None)\n--

        Create a new text-mode sequence with the given attributes.

        """
        cdef bytes sq

        if sequence is not None:
            sq = sequence.encode("ascii")
            self._sq = libeasel.sq.esl_sq_CreateFrom(NULL, sq, NULL, NULL, NULL)
        else:
            self._sq = libeasel.sq.esl_sq_Create()
        if self._sq == NULL:
            raise AllocationError("ESL_SQ")
        self._sq.abc = NULL

        if name is not None:
            self.name = name
        if accession is not None:
            self.accession = accession
        if description is not None:
            self.description = description
        if source is not None:
            self.source = source

        assert libeasel.sq.esl_sq_IsText(self._sq)
        assert self._sq.name != NULL
        assert self._sq.desc != NULL
        assert self._sq.acc != NULL

    @property
    def sequence(self):
        """`str`: The raw sequence letters, as a Python string.
        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsText(self._sq)
        return self._sq.seq.decode("ascii")

    cpdef DigitalSequence digitize(self, Alphabet alphabet):
        """digitize(self, alphabet)\n--

        Convert the text sequence to a digital sequence using ``alphabet``.

        Returns:
            `DigitalSequence`: A copy of the sequence in digital-model,
            digitized with ``alphabet``.

        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsText(self._sq)

        cdef int             status
        cdef ESL_ALPHABET*   abc    = alphabet._abc
        cdef DigitalSequence new    = DigitalSequence.__new__(DigitalSequence, alphabet)

        with nogil:
            new._sq = libeasel.sq.esl_sq_CreateDigital(abc)
            if new._sq == NULL:
                raise AllocationError("ESL_SQ")

            status = libeasel.sq.esl_sq_Copy(self._sq, new._sq)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_sq_Copy")

        assert libeasel.sq.esl_sq_IsDigital(new._sq)
        return new

    cpdef TextSequence copy(self):
        """copy(self)\n--

        Duplicate the text sequence, and return the copy.

        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsText(self._sq)

        cdef int          status
        cdef TextSequence new    = TextSequence.__new__(TextSequence)

        with nogil:
            new._sq = libeasel.sq.esl_sq_Create()
            if new._sq == NULL:
                raise AllocationError("ESL_SQ")
            new._sq.abc = NULL

            status = libeasel.sq.esl_sq_Copy(self._sq, new._sq)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_sq_Copy")

        assert libeasel.sq.esl_sq_IsText(new._sq)
        return new

    cpdef TextSequence reverse_complement(self, bint inplace=False):
        """Build the reverse complement of the sequence.

        This method assumes that the sequence alphabet is IUPAC/DNA. If the
        sequence contains any unknown letters, they will be replaced by
        :math:`N` in the reverse-complement.

        Arguments:
            inplace (`bool`): Whether or not to copy the sequence before
                computing its reverse complement. With `False` (the default),
                the method will return a copy of the sequence that has been
                reverse-complemented. With `True`, it will reverse-complement
                inplace and return `None`.

        Raises:
            UserWarning: When the sequence contains unknown characters.

        Example:
            >>> seq = TextSequence(sequence="ATGC")
            >>> seq.reverse_complement().sequence
            'GCAT'

        Caution:
            The copy made when ``inplace`` is `False` is an exact copy, so
            the `name`, `description` and `accession` of the copy will be
            the same. This could lead to duplicates if you're not careful!

        .. versionadded:: 0.3.0

        """
        assert self._sq != NULL

        cdef TextSequence rc
        cdef int          status

        if inplace:
            status = libeasel.sq.esl_sq_ReverseComplement(self._sq)
        else:
            rc = self.copy()
            status = libeasel.sq.esl_sq_ReverseComplement(rc._sq)

        if status == libeasel.eslEINVAL:
            warnings.warn(
                "reverse-complementing a text sequence with non-DNA characters",
                UserWarning,
                stacklevel=2
            )
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_ReverseComplement")

        return None if inplace else rc


cdef class DigitalSequence(Sequence):
    """A biological sequence stored in digital mode.

    Attributes:
        alphabet (`Alphabet`, *readonly*): The biological alphabet used to
            encode this sequence to digits.

    Hint:
        Use the ``sequence`` property to access the sequence digits as a
        memory view, allowing to access the individual bytes. This can be
        combined with `numpy.asarray` to get the sequence as an array with
        zero-copy.

    """

    def __cinit__(self, Alphabet alphabet, *args, **kwargs):
        self.alphabet = alphabet

    def __init__(self,
        Alphabet alphabet,
        bytes    name=None,
        bytes    description=None,
        bytes    accession=None,
        char[:]  sequence=None,
        bytes    source=None,
    ):
        """__init__(self, alphabet, name=None, description=None, accession=None, sequence=None, source=None)\n--

        Create a new digital-mode sequence with the given attributes.

        .. versionadded:: 0.1.4

        """
        cdef int     status
        cdef int64_t n

        # create an empty digital sequence
        self._sq = libeasel.sq.esl_sq_CreateDigital(alphabet._abc)
        if self._sq == NULL:
            raise AllocationError("ESL_SQ")

        # NB: because the easel sequence has sentinel bytes that we hide from
        #     the user, we cannot just copy the sequence here or use the libeasel
        #     internals; instead, if a sequence is given, we need to emulate
        #     the `esl_sq_CreateDigitalFrom` but copy the sequence with different
        #     offsets.
        if sequence is not None:
            # we can release the GIL while copying memory
            with nogil:
                # grow the sequence buffer so it can hold `n` residues
                n = sequence.shape[0]
                status = libeasel.sq.esl_sq_GrowTo(self._sq, n)
                if status != libeasel.eslOK:
                    raise UnexpectedError(status, "esl_sq_GrowTo")
                # update the digital sequence buffer
                self._sq.dsq[0] = self._sq.dsq[n+1] = libeasel.eslDSQ_SENTINEL
                memcpy(<void*> &self._sq.dsq[1], <const void*> &sequence[0], n)
            # set the coor bookkeeping like it would happend
            self._sq.start = 1
            self._sq.C = 0
            self._sq.end = self._sq.W = self._sq.L = self._sq.n = n

        if name is not None:
            self.name = name
        if accession is not None:
            self.accession = accession
        if description is not None:
            self.description = description
        if source is not None:
            self.source = source

        assert libeasel.sq.esl_sq_IsDigital(self._sq)
        assert self._sq.name != NULL
        assert self._sq.desc != NULL
        assert self._sq.acc != NULL

    @property
    def sequence(self):
        """`memoryview`: The raw sequence digits, as a memory view.
        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsDigital(self._sq)
        return PyMemoryView_FromMemory(
            <char*> &self._sq.dsq[1],
            self._sq.n,
            PyBUF_WRITE
        )

    cpdef DigitalSequence copy(self):
        """copy(self)\n--

        Duplicate the digital sequence, and return the copy.

        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsDigital(self._sq)

        cdef int             status
        cdef ESL_ALPHABET*   abc    = self.alphabet._abc
        cdef DigitalSequence new    = DigitalSequence.__new__(DigitalSequence, self.alphabet)

        with nogil:
            new._sq = libeasel.sq.esl_sq_CreateDigital(abc)
            if new._sq == NULL:
                raise AllocationError("ESL_SQ")

            status = libeasel.sq.esl_sq_Copy(self._sq, new._sq)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_sq_Copy")

        assert libeasel.sq.esl_sq_IsDigital(new._sq)
        return new

    cpdef TextSequence textize(self):
        """textize(self)\n--

        Convert the digital sequence to a text sequence.

        Returns:
            `TextSequence`: A copy of the sequence in text-mode.

        .. versionadded:: 0.1.4

        """
        assert self._sq != NULL
        assert libeasel.sq.esl_sq_IsDigital(self._sq)

        cdef int          status
        cdef TextSequence new    = TextSequence.__new__(TextSequence)

        with nogil:
            new._sq = libeasel.sq.esl_sq_Create()
            if new._sq == NULL:
                raise AllocationError("ESL_SQ")

            status = libeasel.sq.esl_sq_Copy(self._sq, new._sq)
            if status != libeasel.eslOK:
                raise UnexpectedError(status, "esl_sq_Copy")

        assert libeasel.sq.esl_sq_IsText(new._sq)
        return new

    cpdef DigitalSequence reverse_complement(self, bint inplace=False):
        """Build the reverse complement of the sequence.

        Arguments:
            inplace (`bool`): Whether or not to copy the sequence before
                computing its reverse complement. With `False` (the default),
                the method will return a copy of the sequence that has been
                reverse-complemented. With `True`, it will reverse-complement
                inplace and return `None`.

        Raises:
            ValueError: When the alphabet of the `DigitalSequence` does
            not have a complement mapping set (e.g., `Alphabet.amino`).

        Caution:
            The copy made when ``inplace`` is `False` is an exact copy, so
            the `name`, `description` and `accession` of the copy will be
            the same. This could lead to duplicates if you're not careful!

        .. versionadded:: 0.3.0

        """
        assert self._sq != NULL
        assert self.alphabet is not None

        cdef DigitalSequence rc
        cdef int             status

        if self.alphabet._abc.complement == NULL:
            raise ValueError(f"{self.alphabet} has no defined complement")

        if inplace:
            status = libeasel.sq.esl_sq_ReverseComplement(self._sq)
        else:
            rc = self.copy()
            status = libeasel.sq.esl_sq_ReverseComplement(rc._sq)

        if status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sq_ReverseComplement")

        return None if inplace else rc


cdef class SequenceFile:
    """A wrapper around a sequence file, containing unaligned sequences.

    This class supports reading sequences stored in different formats, such
    as FASTA, GenBank or EMBL. The format of each file can be automatically
    detected, but it is also possible to pass an explicit format specifier
    when the `SequenceFile` is instantiated.

    .. versionadded:: 0.2.0
       The ``alphabet`` attribute.

    """

    _formats = {
        "fasta": libeasel.sqio.eslSQFILE_FASTA,
        "embl": libeasel.sqio.eslSQFILE_EMBL,
        "genbank": libeasel.sqio.eslSQFILE_GENBANK,
        "ddbj": libeasel.sqio.eslSQFILE_DDBJ,
        "uniprot": libeasel.sqio.eslSQFILE_UNIPROT,
        "ncbi": libeasel.sqio.eslSQFILE_NCBI,
        "daemon": libeasel.sqio.eslSQFILE_DAEMON,
        "hmmpgmd": libeasel.sqio.eslSQFILE_DAEMON,
        "fmindex": libeasel.sqio.eslSQFILE_FMINDEX,
    }


    # --- Class methods ------------------------------------------------------

    @classmethod
    def parse(cls, bytes buffer, str format):
        """parse(cls, buffer, format)\n--

        Parse a sequence from a binary ``buffer`` using the given ``format``.

        """
        cdef Sequence seq = TextSequence.__new__(TextSequence)
        seq._sq = libeasel.sq.esl_sq_Create()
        if not seq._sq:
            raise AllocationError("ESL_SQ")
        seq._sq.abc = NULL
        return cls.parseinto(seq, buffer, format)

    @classmethod
    def parseinto(cls, Sequence seq, bytes buffer, str format):
        """parseinto(cls, seq, buffer, format)\n--

        Parse a sequence from a binary ``buffer`` into ``seq``.

        """
        assert seq._sq != NULL

        cdef int fmt = libeasel.sqio.eslSQFILE_UNKNOWN
        if format is not None:
            format_ = format.lower()
            if format_ not in cls._formats:
                raise ValueError("Invalid sequence format: {!r}".format(format))
            fmt = cls._formats[format_]

        cdef int status = libeasel.sqio.esl_sqio_Parse(buffer, len(buffer), seq._sq, fmt)
        if status == libeasel.eslEFORMAT:
            raise AllocationError("ESL_SQFILE")
        elif status == libeasel.eslOK:
            return seq
        else:
            raise UnexpectedError(status, "esl_sqio_Parse")


    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self.alphabet = None
        self._sqfp = NULL

    def __init__(self, str file, str format=None):
        """__init__(self, file, format=None)\n--

        Create a new sequence file parser wrapping the given ``file``.

        Arguments:
            file (`str`): The path to a file containing sequences in one of
                the supported file formats.
            format (`str`, optional): The format of the file, or `None` to
                autodetect. Supported values are: ``fasta``, ``embl``,
                ``genbank``, ``ddbj``, ``uniprot``, ``ncbi``, ``daemon``,
                ``hmmpgmd``, ``fmindex``.

        """
        cdef int fmt = libeasel.sqio.eslSQFILE_UNKNOWN
        if format is not None:
            format_ = format.lower()
            if format_ not in self._formats:
                raise ValueError("Invalid sequence format: {!r}".format(format))
            fmt = self._formats[format_]

        cdef bytes fspath = os.fsencode(file)
        cdef int status = libeasel.sqio.esl_sqfile_Open(fspath, fmt, NULL, &self._sqfp)
        if status == libeasel.eslENOTFOUND:
            raise FileNotFoundError(2, "No such file or directory: {!r}".format(file))
        elif status == libeasel.eslEMEM:
            raise AllocationError("ESL_SQFILE")
        elif status == libeasel.eslEFORMAT:
            if format is None:
                raise ValueError("Could not determine format of file: {!r}".format(file))
            else:
                raise EOFError("Sequence file is empty")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_sqfile_Open")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __dealloc__(self):
        if self._sqfp:
            warnings.warn("unclosed sequence file", ResourceWarning)
            self.close()

    def __iter__(self):
        return self

    def __next__(self):
        seq = self.read()
        if seq is None:
            raise StopIteration()
        return seq


    # --- Read methods -------------------------------------------------------

    cpdef Sequence read(self, bint skip_info=False, bint skip_sequence=False):
        """read(self, skip_info=False, skip_sequence=False)\n--

        Read the next sequence from the file.

        Arguments:
            skip_info (`bool`): Pass `True` to disable reading the sequence
                *metadata*, and only read the sequence *letters*. Defaults to
                `False`.
            skip_sequence (`bool`): Pass `True` to disable reading the
                sequence *letters*, and only read the sequence *metadata*.
                Defaults to `False`.

        Returns:
            `Sequence`: The next sequence in the file, or `None` if all
            sequences were read from the file.

        Raises:
            `ValueError`: When attempting to read a sequence from a closed
                file, or when the file could not be parsed.

        Hint:
            This method allocates a new sequence, which is not efficient in
            case the sequences are being read within a tight loop. Use
            `SequenceFile.readinto` with an already initialized `Sequence`
            if you can to recycle the internal buffers.

        """
        cdef Sequence seq
        if self.alphabet is None:
            seq = TextSequence()
        else:
            seq = DigitalSequence(self.alphabet)
        return self.readinto(seq, skip_info=skip_info, skip_sequence=skip_sequence)

    cpdef Sequence readinto(self, Sequence seq, bint skip_info=False, bint skip_sequence=False):
        """readinto(self, seq, skip_info=False, skip_sequence=False)\n--

        Read the next sequence from the file, using ``seq`` to store data.

        Arguments:
            seq (`~pyhmmer.easel.Sequence`): A sequence object to use to store
                the next entry in the file. If this sequence was used before,
                it must be properly reset (using the `Sequence.clear` method)
                before using it again with `readinto`.
            skip_info (`bool`): Pass `True` to disable reading the sequence
                *metadata*, and only read the sequence *letters*. Defaults to
                False`.
            skip_sequence (`bool`): Pass `True` to disable reading the
                sequence *letters*, and only read the sequence *metadata*.
                Defaults to `False`.

        Returns:
            `~pyhmmer.easel.Sequence`: A reference to ``seq`` that was passed
            as an input, or `None` if no sequences are left in the file.

        Raises:
            `ValueError`: When attempting to read a sequence from a closed
                file, or when the file could not be parsed.

        Example:
            Use `SequenceFile.readinto` to loop over the sequences in a file
            while recycling the same `Sequence` buffer:

            >>> with SequenceFile("vendor/hmmer/testsuite/ecori.fa") as sf:
            ...     seq = TextSequence()
            ...     while sf.readinto(seq) is not None:
            ...         # ... process seq here ... #
            ...         seq.clear()

        """
        assert seq._sq != NULL

        cdef int (*funcread)(ESL_SQFILE *sqfp, ESL_SQ *sq) nogil
        cdef str   funcname
        cdef int   status

        if not skip_info and not skip_sequence:
            funcname = "esl_sqio_Read"
            funcread = libeasel.sqio.esl_sqio_Read
        elif not skip_info:
            funcname = "esl_sqio_ReadInfo"
            funcread = libeasel.sqio.esl_sqio_ReadInfo
        elif not skip_sequence:
            funcname = "esl_sqio_ReadSequence"
            funcread = libeasel.sqio.esl_sqio_ReadSequence
        else:
            raise ValueError("Cannot skip reading both sequence and metadata.")

        if self._sqfp == NULL:
            raise ValueError("I/O operation on closed file.")
        else:
            status = funcread(self._sqfp, seq._sq)

        if status == libeasel.eslOK:
            return seq
        elif status == libeasel.eslEOF:
            return None
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> libeasel.sqio.esl_sqfile_GetErrorBuf(self._sqfp)
            raise ValueError("Could not parse file: {}".format(msg.decode()))
        else:
            raise UnexpectedError(status, funcname)


    # --- Fetch methods ------------------------------------------------------

    # cpdef Sequence fetch(self, bytes key, bint skip_info=False, bint skip_sequence=False):
    #     cdef Sequence seq = TextSequence()
    #     return self.fetchinto(seq, key, skip_info=skip_info, skip_sequence=skip_sequence)
    #
    # cpdef Sequence fetchinto(self, Sequence seq, bytes key, bint skip_info=False, bint skip_sequence=False):
    #     raise NotImplementedError("TODO SequenceFile.fetchinto")


    # --- Utils --------------------------------------------------------------

    cpdef void close(self):
        """close(self)\n--

        Close the file and free the resources used by the parser.

        """
        libeasel.sqio.esl_sqfile_Close(self._sqfp)
        self._sqfp = NULL

    cpdef Alphabet guess_alphabet(self):
        """guess_alphabet(self)\n--

        Guess the alphabet of an open `SequenceFile`.

        This method tries to guess the alphabet of a sequence file by
        inspecting the first sequence in the file. It returns the alphabet,
        or `None` if the file alphabet cannot be reliably guessed.

        Raises:
            `EOFError`: if the file is empty.
            `OSError`: if a parse error occurred.
            `ValueError`: if this methods is called after the file was closed.

        """
        cdef int ty
        cdef int status
        cdef Alphabet alphabet

        if self._sqfp == NULL:
            raise ValueError("I/O operation on closed file.")

        status = libeasel.sqio.esl_sqfile_GuessAlphabet(self._sqfp, &ty)
        if status == libeasel.eslOK:
            alphabet = Alphabet.__new__(Alphabet)
            alphabet._init_default(ty)
            return alphabet
        elif status == libeasel.eslENOALPHABET:
            return None
        elif status == libeasel.eslENODATA:
            raise EOFError("Sequence file appears to be empty.")
        elif status == libeasel.eslEFORMAT:
            msg = <bytes> libeasel.sqio.esl_sqfile_GetErrorBuf(self._sqfp)
            raise ValueError("Could not parse file: {}".format(msg.decode()))
        else:
            raise UnexpectedError(status, "esl_sqfile_GuessAlphabet")

    cpdef void set_digital(self, Alphabet alphabet):
        """set_digital(self, alphabet)\n--

        Set the `SequenceFile` to read in digital mode with ``alphabet``.

        This method can be called even after the first sequences have been
        read; it only affects subsequent sequences in the file.

        """
        if self._sqfp == NULL:
            raise ValueError("I/O operation on closed file.")

        cdef int status = libeasel.sqio.esl_sqfile_SetDigital(self._sqfp, alphabet._abc)
        if status == libeasel.eslOK:
            self.alphabet = alphabet
        else:
            raise UnexpectedError(status, "esl_sqfile_SetDigital")


cdef class SSIReader:
    """A read-only handler for sequence/subsequence index file.
    """

    Entry = collections.namedtuple(
        "Entry",
        ["fd", "record_offset", "data_offset", "record_length"]
    )

    FileInfo = collections.namedtuple(
        "FileInfo",
        ["name", "format"]
    )

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._ssi = NULL

    def __init__(self, str file):
        """__init__(self, file)\n--

        Create a new SSI file reader for the file at the given location.

        Arguments:
            file (`str`): The path to a sequence/subsequence index file to
                read.

        """
        cdef int      status
        cdef bytes    fspath = os.fsencode(file)

        status = libeasel.ssi.esl_ssi_Open(fspath, &self._ssi)
        if status == libeasel.eslENOTFOUND:
            raise FileNotFoundError(2, "No such file or directory: {!r}".format(file))
        elif status == libeasel.eslEFORMAT:
            raise ValueError("File is not in correct SSI format")
        elif status == libeasel.eslERANGE:
            raise RuntimeError("File has 64-bit file offsets, which are unsupported on this system")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_ssi_Open")

    def __dealloc__(self):
        libeasel.ssi.esl_ssi_Close(self._ssi)

    def __enter__(self):
        return self

    def __exit__(self, exc_value, exc_type, traceback):
        self.close()
        return False

    # --- Methods ------------------------------------------------------------

    def file_info(self, uint16_t fd):
        """file_info(self, fd)\n--

        Retrieve the `~pyhmmer.easel.SSIReader.FileInfo` of the descriptor.

        """
        cdef int   status
        cdef char* filename
        cdef int   format

        if self._ssi == NULL:
            raise ValueError("I/O operation on closed file.")
        if fd >= self._ssi.nfiles:
            raise IndexError(fd)

        status = libeasel.ssi.esl_ssi_FileInfo(self._ssi, fd, &filename, &format)
        if status == libeasel.eslOK:
            return self.FileInfo(os.fsdecode(filename), format)
        else:
            raise UnexpectedError(status, "esl_ssi_FileInfo")

    def find_name(self, bytes key):
        """find_name(self, key)\n--

        Retrieve the `~pyhmmer.easel.SSIReader.Entry` for the given name.

        """
        cdef uint16_t ret_fh
        cdef off_t    ret_roff
        cdef off_t    opt_doff
        cdef int64_t  opt_L
        cdef int      status

        if self._ssi == NULL:
            raise ValueError("I/O operation on closed file.")

        status = libeasel.ssi.esl_ssi_FindName(
            self._ssi, key, &ret_fh, &ret_roff, &opt_doff, &opt_L
        )

        if status == libeasel.eslOK:
            return self.Entry(ret_fh, ret_roff, opt_doff or None, opt_L or None)
        elif status == libeasel.eslENOTFOUND:
            raise KeyError(key)
        elif status == libeasel.eslEFORMAT:
            raise ValueError("malformed index")
        else:
            raise UnexpectedError(status, "esl_ssi_FindName")

    cpdef void close(self):
        """close(self)\n--

        Close the SSI file reader.

        """
        libeasel.ssi.esl_ssi_Close(self._ssi)
        self._ssi = NULL


cdef class SSIWriter:
    """A writer for sequence/subsequence index files.
    """

    # --- Magic methods ------------------------------------------------------

    def __cinit__(self):
        self._newssi = NULL

    def __init__(self, str file, bint exclusive = False):
        """__init__(self, file)\n--

        Create a new SSI file write for the file at the given location.

        Arguments:
            file (`str`): The path to a sequence/subsequence index file to
                write.
            exclusive (`bool`): Whether or not to create a file if one does
                not exist.

        Raises:
            `FileNotFoundError`: When the path to the file cannot be resolved.
            `FileExistsError`: When the file exists and ``exclusive`` is `True`.

        """
        cdef int   status
        cdef bytes fspath = os.fsencode(file)

        status = libeasel.ssi.esl_newssi_Open(fspath, not exclusive, &self._newssi)
        if status == libeasel.eslENOTFOUND:
            raise FileNotFoundError(2, "No such file or directory: {!r}".format(file))
        elif status == libeasel.eslEOVERWRITE:
            raise FileExistsError(17, "File exists: {!r}".format(file))
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_newssi_Open")

    def __dealloc__(self):
        if self._newssi != NULL:
            warnings.warn("unclosed SSI file", ResourceWarning)
            self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # --- Properties -----------------------------------------------------------

    @property
    def closed(self):
        return self._newssi == NULL

    # --- Utils --------------------------------------------------------------

    cdef void _on_write(self):
        if self.closed:
            raise ValueError("I/O operation on closed file.")

    # --- Methods ------------------------------------------------------------

    cpdef uint16_t add_file(self, str filename, int format = 0):
        """add_file(self, filename, format=0)\n--

        Add a new file to the index.

        Arguments:
            filename (str): The name of the file to register.
            format (int): A format code to associate with the file, or *0*.

        Returns:
            `int`: The filehandle associated with the new indexed file.

        """
        cdef int        status
        cdef uint16_t   fd

        self._on_write()
        name = os.fsencode(filename)
        status = libeasel.ssi.esl_newssi_AddFile(self._newssi, name, format, &fd)
        if status == libeasel.eslOK:
            return fd
        elif status == libeasel.eslERANGE:
            raise ValueError("Too many files registered in index.")
        else:
            raise UnexpectedError(status, "esl_newssi_AddFile")

    cpdef void add_key(
        self,
        bytes key,
        uint16_t fd,
        off_t record_offset,
        off_t data_offset = 0,
        int64_t record_length = 0
    ):
        """add_key(self, key, fd, record_offset, data_offset=0, record_length=0)\n--

        Add a new entry to the index with the given ``key``.

        """
        cdef int status

        self._on_write()
        status = libeasel.ssi.esl_newssi_AddKey(
            self._newssi, key, fd, record_offset, data_offset, record_length
        )

        if status == libeasel.eslERANGE:
            raise ValueError("Too many primary keys registered in index.")
        elif status == libeasel.eslENOTFOUND:
            raise OSError("Could not open external temporary files.")
        elif status != libeasel.eslOK:
            raise UnexpectedError(status, "esl_newssi_AddKey")

    cpdef void add_alias(self, bytes alias, bytes key):
        """add_alias(self, alias, key)\n--

        Make ``alias`` an alias of ``key`` in the index.

        """
        cdef int status

        self._on_write()
        status = libeasel.ssi.esl_newssi_AddAlias(self._newssi, alias, key)
        if status == libeasel.eslOK:
            return
        elif status == libeasel.eslERANGE:
            raise ValueError("Too many secondary keys registed in index")
        elif status == libeasel.eslENOTFOUND:
            raise OSError("Could not open external temporary files.")
        else:
            raise UnexpectedError(status, "esl_newssi_AddAlias")

    def close(self):
        """close(self)\n--

        Close the SSI file writer.

        """
        cdef int status

        if not self.closed:

            status = libeasel.ssi.esl_newssi_Write(self._newssi)
            if status == libeasel.eslERANGE:
                raise ValueError("Too many keys registered in index.")
            elif status == libeasel.eslESYS:
                raise RuntimeError("Extern sorting of keys failed.")
            elif status == libeasel.eslEDUP:
                raise ValueError("Index contains duplicate keys.")

            libeasel.ssi.esl_newssi_Close(self._newssi)
            self._newssi = NULL


# --- Module init code -------------------------------------------------------

include "exceptions.pxi"
