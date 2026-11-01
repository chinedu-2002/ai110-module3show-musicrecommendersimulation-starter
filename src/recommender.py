"""Load a song catalog and rank it with an explainable weighted content score."""

import csv
from dataclasses import asdict, dataclass
from math import isfinite
from pathlib import Path
from typing import Mapping


@dataclass
class Song:
    """Represent the attributes in one catalog row."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represent a taste profile using the starter's object interface."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    # Retained for starter compatibility; baseline scoring uses three features.
    likes_acoustic: bool = False


@dataclass(frozen=True)
class ScoringWeights:
    """Keep feature weights explicit so experiments do not change the baseline."""

    genre: float = 2.0
    mood: float = 1.0
    energy: float = 1.0

    def __post_init__(self) -> None:
        """Reject negative or nonfinite weights before scoring."""
        for name in ("genre", "mood", "energy"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} weight must be a finite nonnegative number")
            if not isfinite(value) or value < 0:
                raise ValueError(f"{name} weight must be a finite nonnegative number")


BASELINE = ScoringWeights()
ENERGY_FOCUSED = ScoringWeights(genre=1.0, mood=1.0, energy=2.0)
SongData = dict[str, str | int | float]
Recommendation = tuple[SongData, float, str]
CATALOG_FIELDS = tuple(Song.__dataclass_fields__)


def _label(value: object, name: str) -> str:
    """Normalize a nonempty category for case-insensitive matching."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value.strip().casefold()


def _number(value: object, name: str, *, unit_interval: bool = True) -> float:
    """Validate finite numbers and the catalog's documented numeric ranges."""
    try:
        if isinstance(value, bool):
            raise ValueError
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be a finite number")
    if unit_interval and not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    if not unit_interval and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def load_songs(csv_path: str | Path) -> list[SongData]:
    """Read validated song dictionaries with numeric fields from a UTF-8 CSV."""
    songs: list[SongData] = []
    seen_ids: set[int] = set()
    with Path(csv_path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = set(CATALOG_FIELDS) - set(fields)
        if missing:
            raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing))}")
        if len(fields) != len(set(fields)):
            raise ValueError("CSV contains duplicate column names")
        for line, row in enumerate(reader, start=2):
            try:
                if None in row:
                    raise ValueError("row has extra values")
                if any(row[field] is None or not row[field].strip() for field in CATALOG_FIELDS):
                    raise ValueError("row has missing or blank values")
                song: SongData = {field: row[field].strip() for field in CATALOG_FIELDS}
                try:
                    song_id = int(song["id"])
                except ValueError as exc:
                    raise ValueError("id must be a positive integer") from exc
                if song_id <= 0 or song_id in seen_ids:
                    raise ValueError("id must be positive and unique")
                song["id"] = song_id
                song["genre"] = _label(song["genre"], "genre")
                song["mood"] = _label(song["mood"], "mood")
                for field in ("energy", "valence", "danceability", "acousticness"):
                    song[field] = _number(song[field], field)
                song["tempo_bpm"] = _number(song["tempo_bpm"], "tempo_bpm", unit_interval=False)
                seen_ids.add(song_id)
                songs.append(song)
            except ValueError as exc:
                raise ValueError(f"{csv_path}: row {line}: {exc}") from exc
    return songs


def score_song(
    user_prefs: Mapping[str, object],
    song: Mapping[str, object],
    weights: ScoringWeights = BASELINE,
) -> tuple[float, list[str]]:
    """Return a weighted genre/mood/energy score and each feature's contribution."""
    genre = _label(user_prefs.get("genre", user_prefs.get("favorite_genre")), "preferred genre")
    mood = _label(user_prefs.get("mood", user_prefs.get("favorite_mood")), "preferred mood")
    target = _number(user_prefs.get("energy", user_prefs.get("target_energy")), "target energy")
    genre_match = genre == _label(song.get("genre"), "song genre")
    mood_match = mood == _label(song.get("mood"), "song mood")
    gap = abs(_number(song.get("energy"), "song energy") - target)
    genre_points = weights.genre if genre_match else 0.0
    mood_points = weights.mood if mood_match else 0.0
    energy_points = weights.energy * (1.0 - gap)
    reasons = [
        f"genre {'match' if genre_match else 'mismatch'} (+{genre_points:.2f})",
        f"mood {'match' if mood_match else 'mismatch'} (+{mood_points:.2f})",
        f"energy similarity {1.0 - gap:.2f} (+{energy_points:.2f})",
    ]
    return genre_points + mood_points + energy_points, reasons


def recommend_songs(
    user_prefs: Mapping[str, object],
    songs: list[SongData],
    k: int = 5,
    weights: ScoringWeights = BASELINE,
) -> list[Recommendation]:
    """Score every song and return the top k; ties retain the catalog's order."""
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k < 0:
        raise ValueError("k must be nonnegative")
    ranked = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        ranked.append((song, score, "; ".join(reasons)))
    return sorted(ranked, key=lambda result: result[1], reverse=True)[:k]


class Recommender:
    """Adapt the starter's object interface to the same scoring implementation."""

    def __init__(self, songs: list[Song], weights: ScoringWeights = BASELINE):
        """Store the catalog and the chosen weights."""
        self.songs = songs
        self.weights = weights

    def recommend(self, user: UserProfile, k: int = 5) -> list[Song]:
        """Return original Song objects in the functional recommender's order."""
        rows = [asdict(song) for song in self.songs]
        objects_by_row = {id(row): song for row, song in zip(rows, self.songs)}
        ranked = recommend_songs(asdict(user), rows, k, self.weights)
        return [objects_by_row[id(row)] for row, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a recommendation with the same contributions used for ranking."""
        _, reasons = score_song(asdict(user), asdict(song), self.weights)
        return "; ".join(reasons)
