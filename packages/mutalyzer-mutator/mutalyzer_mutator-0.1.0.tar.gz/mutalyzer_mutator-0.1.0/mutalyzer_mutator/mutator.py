"""
Module to mutate sequences based on a variants list.

Assumptions for which no check is performed:
 - Only ``deletion insertion`` operations.
 - Only exact locations, i.e., no uncertainties such as `10+?`.
 - Locations are zero-based right-open with ``start > end``.
 - There is no overlapping between variants locations.

Notes:
  - If any of the above is not met, the result will be bogus.
  - There can be empty inserted lists.
"""


from .util import reverse_complement


class UnknownInsertedSource(Exception):
    pass


def _get_inverted(sequence):
    """
    Reverse complement inversion using code extracted from BioPython.
    """
    return reverse_complement(sequence)


def _get_start_end(location):
    """
    Get the start and the end of a location object. For point locations both
    start and end equal the position value.
    """
    if location["type"] == "range":
        return location["start"]["position"], location["end"]["position"]
    elif location["type"] == "point":
        return location["position"], location["position"]


def _get_inserted_sequence(inserted, sequences):
    """
    Retrieves the actual sequence mentioned in the insertion.
    """
    if inserted["source"] == "description":
        sequence = inserted["sequence"]
    elif inserted["source"] == "reference":
        sequence = sequences[inserted["source"]][
            slice(*_get_start_end(inserted["location"]))
        ]
    elif isinstance(inserted["source"], dict) and inserted["source"].get("id"):
        sequence = sequences[inserted["source"]["id"]][
            slice(*_get_start_end(inserted["location"]))
        ]
    else:
        raise UnknownInsertedSource("Inserted source not supported.")

    if (
        inserted.get("repeat_number")
        and inserted["repeat_number"].get("value") is not None
    ):
        sequence = sequence * inserted.get("repeat_number")["value"]

    if inserted.get("inverted"):
        sequence = _get_inverted(sequence)

    return sequence


def mutate(sequences, variants):
    """
    Mutate the reference sequence under ``sequences["reference"]`` according
    to the provided variants operations.

    :arg dict sequences: Sequences dictionary.
    :arg list variants: Operations list.
    :returns: Mutated sequence.
    :rtype: str
    """
    reference = sequences["reference"]

    variants = sorted(variants, key=lambda v: (_get_start_end(v["location"])))

    parts = []
    current_index = 0
    for variant in variants:
        start, end = _get_start_end(variant["location"])
        parts.append(reference[current_index:start])
        for insertion in variant["inserted"]:
            parts.append(_get_inserted_sequence(insertion, sequences))
        current_index = end

    parts.append(reference[current_index:])

    return "".join(parts)
