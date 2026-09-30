"""Unit tests for the corrected AAC calculation (audit fix PR)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aac_utils import NUM_FEATURES, calculate_AAC


def test_feature_count():
    feats = calculate_AAC("[1, 2, 3]")
    assert len(feats) == NUM_FEATURES
    assert set(feats.keys()) == set(range(1, NUM_FEATURES + 1))


def test_percentages_sum_to_100():
    feats = calculate_AAC("[1, 12, 3, 5, 5]")
    assert abs(sum(feats.values()) - 100.0) < 1e-9


def test_single_residue_sequence():
    # all residues code 1 -> code 1 = 100%, everything else 0
    feats = calculate_AAC("[1, 1, 1, 1]")
    assert feats[1] == 100.0
    assert all(v == 0.0 for k, v in feats.items() if k != 1)


def test_two_residue_sequence():
    # codes 1 and 3 alternating -> 50/50
    feats = calculate_AAC("[1, 3, 1, 3]")
    assert feats[1] == 50.0
    assert feats[3] == 50.0
    assert all(v == 0.0 for k, v in feats.items() if k not in (1, 3))


def test_multidigit_codes_not_overcounted():
    # regression test for the original substring-counting bug:
    # code 10 must not be counted as code 1
    feats = calculate_AAC("[10, 10, 10]")
    assert feats[10] == 100.0
    assert feats[1] == 0.0


def test_list_input_accepted():
    feats = calculate_AAC([26, 26])
    assert feats[26] == 100.0


def test_empty_sequence():
    feats = calculate_AAC([])
    assert all(v == 0.0 for v in feats.values())
