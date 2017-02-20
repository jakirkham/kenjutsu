__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Dec 08, 2016 14:20:52 GMT-0500$"


import collections
import itertools
import numbers


def index_to_slice(index):
    """
        Convert an index to a slice.

        Note:
            A single index behaves differently from a length 1 ``slice``. When
            applying the former one reduces that dimension; whereas, applying
            the latter results in a singleton dimension being retained. Also
            if an index is out of bounds, one gets an ``IndexError``. However,
            with an out of bounds length 1 ``slice``, one simply doesn't get
            the requested range.

        Args:
            index(int):                  an index to convert to a slice

        Returns:
            (slice):                     a slice corresponding to the index

        Examples:

            >>> index_to_slice(1)
            slice(1, 2, 1)

            >>> index_to_slice(-1)
            slice(-1, -2, -1)
    """

    if not isinstance(index, numbers.Integral):
        raise TypeError(
            "Expected an integral type. Instead got `%s`." % str(index)
        )

    step = -1 if index < 0 else 1

    return slice(index, index + step, step)


def reformat_slice(a_slice, a_length=None):
    """
        Takes a slice and reformats it to fill in as many undefined values as
        possible.

        Args:
            a_slice(slice):        a slice to reformat.

            a_length(int):         a length to fill for stopping if not
                                   provided.

        Returns:
            (slice):               a new slice with as many values filled in as
                                   possible.

        Examples:

            >>> reformat_slice(slice(2, -1, None))
            slice(2, -1, 1)

            >>> reformat_slice(slice(2, -1, None), 10)
            slice(2, 9, 1)
    """

    new_slice = a_slice
    if (new_slice is Ellipsis) or (new_slice == tuple()):
        new_slice = slice(None)
    elif isinstance(a_slice, numbers.Integral):
        new_slice = index_to_slice(a_slice)
    elif isinstance(a_slice, collections.Sequence):
        if not all(map(lambda i: isinstance(i, numbers.Integral), a_slice)):
            raise TypeError(
                "Arbitrary sequences not permitted."
                " All elements must be of integral type."
            )

        # Normalize each integer in the range.
        new_slice = []
        for i in a_slice:
            new_slice.append(reformat_slice(i, a_length))
        return new_slice
    elif not isinstance(a_slice, slice):
        raise TypeError(
            "Expected an index acceptable type."
            " Instead got, `%s`." % str(a_slice)
        )

    if new_slice.step == 0:
        raise ValueError("Slice cannot have a step size of `0`.")

    start = new_slice.start
    stop = new_slice.stop
    step = new_slice.step

    # Fill unknown values.
    if step is None:
        step = 1
    if start is None:
        if step > 0:
            start = 0
        elif step < 0:
            start = -1
    if (stop is None) and (step > 0):
        stop = a_length

    stop_i = stop is not None

    # Make adjustments for length
    if a_length is not None:
        # Normalize out-of-bound step sizes.
        if step < -a_length:
            step = -a_length
        elif step > a_length:
            step = a_length

        # Normalize bounded negative values.
        if -a_length <= start < 0:
            start += a_length
        if stop_i and (-a_length <= stop < 0):
            stop += a_length

        # Handle out-of-bound limits.
        if step > 0:
            if (start > a_length) or (stop < -a_length):
                start = stop = 0
                step = 1
            else:
                if start < -a_length:
                    start = 0
                if stop > a_length:
                    stop = a_length
        elif step < 0:
            if (start < -a_length) or (stop_i and stop >= (a_length - 1)):
                start = stop = 0
                step = 1
            else:
                if start >= a_length:
                    start = a_length - 1
                if stop_i and stop < -a_length:
                    stop = None
                    stop_i = False

    # Catch some known empty slices.
    if stop_i and (start == stop):
        start = stop = 0
        step = 1
    elif (step > 0) and (stop == 0):
        start = stop = 0
        step = 1
    elif (step < 0) and (stop == -1):
        start = stop = 0
        step = 1
    elif stop_i and (start >= 0) and (stop >= 0):
        if (step > 0) and (start > stop):
            start = stop = 0
            step = 1
        elif (step < 0) and (start < stop):
            start = stop = 0
            step = 1

    new_slice = slice(start, stop, step)
    if isinstance(a_slice, numbers.Integral):
        if new_slice.start == new_slice.stop == 0:
            raise IndexError("Index out of range.")
        new_slice = new_slice.start

    return(new_slice)


def reformat_slices(slices, lengths=None):
    """
        Takes a tuple of slices and reformats them to fill in as many undefined
        values as possible.

        Args:
            slices(tuple(slice)):        a tuple of slices to reformat.
            lengths(tuple(int)):         a tuple of lengths to fill.

        Returns:
            (slice):                     a tuple of slices with all default
                                         values filled if possible.

        Examples:

            >>> reformat_slices(
            ...     (
            ...         slice(None),
            ...         slice(3, None),
            ...         slice(None, 5),
            ...         slice(None, None, 2)
            ...     ),
            ...     (10, 13, 15, 20)
            ... )
            (slice(0, 10, 1), slice(3, 13, 1), slice(0, 5, 1), slice(0, 20, 2))
    """

    new_slices = slices
    if new_slices == tuple():
        new_slices = Ellipsis

    try:
        len(new_slices)
    except TypeError:
        new_slices = (new_slices,)

    new_lengths = lengths
    try:
        if new_lengths is not None:
            len(new_lengths)
    except TypeError:
        new_lengths = (new_lengths,)

    el_idx = None
    try:
        el_idx = new_slices.index(Ellipsis)
    except ValueError:
        pass

    if new_lengths is not None and el_idx is None:
        if len(new_slices) < len(new_lengths):
            new_slices += (Ellipsis,)
            el_idx = new_slices.index(Ellipsis)
        elif len(new_slices) > len(new_lengths):
            raise ValueError(
                "Shape must be as large or larger than the number of slices."
            )
    elif new_lengths is not None:
        if (len(new_slices) - 1) > len(new_lengths):
            raise ValueError(
                "Shape must be as large or larger than the number of slices"
                " without the Ellipsis."
            )

    if el_idx is not None:
        # Break into three cases.
        #
        # 1. Before the Ellipsis
        # 2. The Ellipsis
        # 3. After the Ellipsis
        #
        # Cases 1 and 3 are trivially solved as before.
        # Case 2 is either a no-op or a bunch of `slice(None)`s.
        #
        # The result is a combination of all of these.

        slices_before = new_slices[:el_idx]
        slices_after = new_slices[el_idx+1:]

        if Ellipsis in slices_before or Ellipsis in slices_after:
            raise ValueError("Only one Ellipsis is permitted. Found multiple.")

        new_lengths_before = None
        new_lengths_after = None
        slice_el = (Ellipsis,)
        if new_lengths is not None:
            pos_before = len(slices_before)
            pos_after = len(new_lengths) - len(slices_after)

            new_lengths_before = new_lengths[:pos_before]
            new_lengths_after = new_lengths[pos_after:]

            new_lengths_el = new_lengths[pos_before:pos_after]
            slice_el = len(new_lengths_el) * (slice(None),)
            if slice_el:
                slice_el = reformat_slices(
                    slice_el,
                    new_lengths_el
                )

        if slices_before:
            slices_before = reformat_slices(slices_before, new_lengths_before)
        if slices_after:
            slices_after = reformat_slices(slices_after, new_lengths_after)

        new_slices = slices_before + slice_el + slices_after
    else:
        if new_lengths is None:
            new_lengths = [None] * len(new_slices)

        new_slices = list(new_slices)
        for i, each_length in enumerate(new_lengths):
            new_slices[i] = reformat_slice(new_slices[i], each_length)

        new_slices = tuple(new_slices)

    n_seqs = sum(map(
        lambda i: isinstance(i, collections.Sequence), new_slices
    ))
    if n_seqs > 1:
        raise ValueError(
            "Only one integral sequence supported."
            " Instead got `%s`." % str(n_seqs)
        )

    return(new_slices)


def split_indices(slices):
    """
        Splits slices with multiple indices into multiple splices.

        Support of slices with a sequence of indices is varied. Some
        libraries like NumPy support them without issues. Other libraries
        like h5py support them as long as they are in sequential order.
        In still other libraries support is non-existent. However, in
        all those cases normally a single index is permissible. This
        converts slices with multiple indices into a list of slices with
        a single index each. While this still leaves it up to the user
        to iterate over these and combine the results in some sensible
        way, it is better than just getting a failure and should extend
        well to a variety of cases.

        Args:
            slices(tuple(slice)):        a tuple of slices to split

        Returns:
            (list(tuple(slice))):        a list of a tuple of slices

        Examples:

            >>> split_indices(
            ...     (
            ...         3,
            ...         Ellipsis,
            ...         [0, 1, 2],
            ...         slice(2, 5),
            ...         slice(4, 6, 2)
            ...     )
            ... )  # doctest: +NORMALIZE_WHITESPACE
            [(3, Ellipsis, slice(0, 1, 1), slice(2, 5, 1), slice(4, 6, 2)),
             (3, Ellipsis, slice(1, 2, 1), slice(2, 5, 1), slice(4, 6, 2)),
             (3, Ellipsis, slice(2, 3, 1), slice(2, 5, 1), slice(4, 6, 2))]
    """

    ref_slices = reformat_slices(slices)

    mtx_slices = []
    for each_dim_slice in ref_slices:
        if each_dim_slice is Ellipsis:
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, numbers.Integral):
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, slice):
            mtx_slices.append([each_dim_slice])
        elif isinstance(each_dim_slice, collections.Sequence):
            new_slice = []
            for i in each_dim_slice:
                new_slice.append(index_to_slice(i))
            mtx_slices.append(new_slice)

    result_slices = []
    for each_dim_slice in itertools.product(*mtx_slices):
        result_slices.append(tuple(each_dim_slice))

    return result_slices
