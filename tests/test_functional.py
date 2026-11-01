"""Behavioral checks for CSV loading, explained scoring, and ranked results."""

import csv
from copy import deepcopy
from dataclasses import FrozenInstanceError
import re

import pytest

from src.recommender import (
    ScoringWeights,
    load_songs,
    recommend_songs,
    score_song,
)


HEADERS = [
    "id", "title", "artist", "genre", "mood", "energy", "tempo_bpm",
    "valence", "danceability", "acousticness",
]


@pytest.fixture
def prefs():
    return {"genre": "pop", "mood": "happy", "energy": 0.8}


@pytest.fixture
def csv_row():
    return {
        "id": "1", "title": "Sunrise, Again", "artist": "Test Artist",
        "genre": "pop", "mood": "happy", "energy": "0.8",
        "tempo_bpm": "120", "valence": "0.9", "danceability": "0.7",
        "acousticness": "0.2",
    }


def write_catalog(tmp_path, rows, headers=HEADERS):
    """Write a small realistic CSV, including quoted commas in titles."""
    path = tmp_path / "songs.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_exact_match_score_and_reasons_are_consistent(prefs):
    score, reasons = score_song(prefs, dict(prefs))

    assert score == pytest.approx(4.0)
    assert isinstance(reasons, list)
    assert "genre match (+2.00)" in reasons
    assert "mood match (+1.00)" in reasons
    assert any("energy similarity" in reason and "(+1.00)" in reason
               for reason in reasons)
    contributions = [float(value) for reason in reasons
                     for value in re.findall(r"\(\+([0-9.]+)\)", reason)]
    assert sum(contributions) == pytest.approx(score)


def test_mismatches_are_explained_and_energy_still_contributes(prefs):
    score, reasons = score_song(
        prefs, {"genre": "jazz", "mood": "relaxed", "energy": 0.6}
    )

    assert score == pytest.approx(0.8)
    assert "genre mismatch (+0.00)" in reasons
    assert "mood mismatch (+0.00)" in reasons
    assert any("(+0.80)" in reason for reason in reasons)


def test_energy_rewards_closeness_symmetrically():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.5}
    scores = [score_song(prefs, {**prefs, "energy": energy})[0]
              for energy in (0.3, 0.5, 0.7)]

    assert scores[0] == pytest.approx(scores[2])
    assert scores[1] > scores[0]
    assert scores == pytest.approx([3.8, 4.0, 3.8])


@pytest.mark.parametrize("target,song_energy,expected", [(0, 0, 4), (1, 1, 4), (0, 1, 3)])
def test_energy_boundaries(target, song_energy, expected):
    prefs = {"genre": "pop", "mood": "happy", "energy": target}
    assert score_song(prefs, {**prefs, "energy": song_energy})[0] == pytest.approx(expected)


def test_legacy_preference_keys_match_canonical_keys(prefs):
    legacy = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}
    assert score_song(legacy, dict(prefs)) == score_song(prefs, dict(prefs))


def test_ranking_is_descending_explained_and_does_not_mutate(prefs):
    songs = [
        {"id": 1, "genre": "jazz", "mood": "relaxed", "energy": 0.1},
        {"id": 2, "genre": "pop", "mood": "happy", "energy": 0.8},
        {"id": 3, "genre": "pop", "mood": "intense", "energy": 0.9},
    ]
    before = deepcopy(songs)
    preferences_before = deepcopy(prefs)
    results = recommend_songs(prefs, songs, k=2)

    assert [song["id"] for song, _, _ in results] == [2, 3]
    assert [score for _, score, _ in results] == pytest.approx([4.0, 2.9])
    assert results[0][0] is songs[1]
    assert all(isinstance(reason, str) and "genre" in reason and "energy" in reason
               for _, _, reason in results)
    assert songs == before
    assert prefs == preferences_before


def test_equal_scores_preserve_catalog_order(prefs):
    songs = [{"id": song_id, **prefs} for song_id in (9, 2, 7)]
    assert [song["id"] for song, _, _ in recommend_songs(prefs, songs, k=3)] == [9, 2, 7]


def test_k_zero_empty_catalog_and_oversized_k(prefs):
    songs = [dict(prefs)]
    assert recommend_songs(prefs, songs, k=0) == []
    assert recommend_songs(prefs, [], k=5) == []
    assert len(recommend_songs(prefs, songs, k=100)) == 1


def test_negative_k_is_rejected(prefs):
    with pytest.raises(ValueError):
        recommend_songs(prefs, [dict(prefs)], k=-1)


@pytest.mark.parametrize("invalid_k", [1.5, "2"])
def test_noninteger_k_is_rejected(prefs, invalid_k):
    with pytest.raises(TypeError):
        recommend_songs(prefs, [dict(prefs)], k=invalid_k)


def test_weight_experiment_changes_rank_without_changing_baseline():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.9}
    songs = [
        {"id": 1, "genre": "pop", "mood": "sad", "energy": 0.0},
        {"id": 2, "genre": "rock", "mood": "happy", "energy": 0.9},
    ]
    baseline = recommend_songs(prefs, songs, k=2)
    experimental = recommend_songs(
        prefs, songs, k=2, weights=ScoringWeights(genre=1, mood=1, energy=2)
    )

    assert [song["id"] for song, _, _ in baseline] == [1, 2]
    assert [score for _, score, _ in baseline] == pytest.approx([2.1, 2.0])
    assert [song["id"] for song, _, _ in experimental] == [2, 1]
    assert [score for _, score, _ in experimental] == pytest.approx([3.0, 1.2])
    assert recommend_songs(prefs, songs, k=2) == baseline


@pytest.mark.parametrize("kwargs", [
    {"genre": -1}, {"mood": float("nan")}, {"energy": float("inf")},
])
def test_weights_reject_negative_or_nonfinite_values(kwargs):
    with pytest.raises(ValueError):
        ScoringWeights(**kwargs)


def test_weights_are_immutable():
    weights = ScoringWeights()
    with pytest.raises(FrozenInstanceError):
        weights.genre = 9


def test_load_songs_converts_numbers_and_preserves_quoted_text(tmp_path, csv_row):
    path = write_catalog(tmp_path, [csv_row])
    songs = load_songs(path)

    assert len(songs) == 1
    assert songs[0]["id"] == 1
    assert isinstance(songs[0]["id"], int)
    assert songs[0]["title"] == "Sunrise, Again"
    for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
        assert isinstance(songs[0][field], float)
        assert songs[0][field] == pytest.approx(float(csv_row[field]))


def test_load_songs_rejects_missing_required_header(tmp_path, csv_row):
    headers = [field for field in HEADERS if field != "mood"]
    row = {field: value for field, value in csv_row.items() if field != "mood"}
    path = write_catalog(tmp_path, [row], headers)

    with pytest.raises(ValueError):
        load_songs(path)


@pytest.mark.parametrize("field,value", [
    ("id", "1.5"), ("energy", "loud"), ("energy", "nan"),
    ("energy", "inf"), ("energy", "-0.1"), ("energy", "1.1"),
    ("valence", "1.1"), ("danceability", "-0.1"),
    ("acousticness", "1.1"), ("tempo_bpm", "0"),
    ("tempo_bpm", "-30"), ("genre", ""),
])
def test_load_songs_rejects_invalid_values(tmp_path, csv_row, field, value):
    path = write_catalog(tmp_path, [{**csv_row, field: value}])
    with pytest.raises(ValueError):
        load_songs(path)


def test_load_songs_rejects_duplicate_ids(tmp_path, csv_row):
    path = write_catalog(tmp_path, [csv_row, {**csv_row, "title": "Another Song"}])
    with pytest.raises(ValueError):
        load_songs(path)
