"""Corrected Amino Acid Composition (AAC) feature calculation.

Added by the audit fix PR. The original ``calculate_AAC()`` in
``2. feature selection/feature_selec.ipynb`` operated on the *stringified*
``numeric_sequence`` (e.g. "[1, 12, 3, ...]"): ``sequence.count(str(aa))``
counted substrings (residue 1 also matched 10-19 and 21) and
``len(sequence)`` counted characters instead of residues, corrupting all
26 AAC features. This module works on the parsed integer list (codes 1-26,
same encoding as the notebooks, where 26 = X/unknown).

NOTE: fixing AAC changes all 26 features; every downstream model/metric
must be recomputed. Do not treat previous results as comparable.
"""

import ast

NUM_FEATURES = 26  # amino-acid codes 1..26 used by the numeric encoding


def parse_numeric_sequence(sequence):
    """Accept a list of ints or its string representation; return list of ints."""
    if isinstance(sequence, str):
        sequence = ast.literal_eval(sequence)
    return [int(item) for item in sequence]


def calculate_AAC(sequence):
    """Return AAC percentages (0-100) for residue codes 1..26.

    Keys are the integer codes 1..26 (as in the notebook version);
    values sum to 100.0 for non-empty sequences.
    """
    seq = parse_numeric_sequence(sequence)
    total_aa = len(seq)
    if total_aa == 0:
        return {aa: 0.0 for aa in range(1, NUM_FEATURES + 1)}
    return {aa: (seq.count(aa) / total_aa) * 100 for aa in range(1, NUM_FEATURES + 1)}
