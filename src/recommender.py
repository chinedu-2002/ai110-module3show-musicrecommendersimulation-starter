import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
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
    """Represents a user's taste preferences for music recommendations."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP wrapper that scores and ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        scored = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match: {song.genre} (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match: {song.mood} (+1.0)")
        energy_gap = abs(song.energy - user.target_energy)
        energy_pts = round(1.5 * (1.0 - energy_gap), 2)
        reasons.append(f"energy similarity (+{energy_pts})")
        if user.likes_acoustic and song.acousticness >= 0.7:
            reasons.append("acoustic match (+0.5)")
        return "; ".join(reasons) if reasons else "general match"

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric score for a single song against the user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.5 * (1.0 - abs(song.energy - user.target_energy))
        if user.likes_acoustic and song.acousticness >= 0.7:
            score += 0.5
        return score


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed numeric fields."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons list)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_pts = round(1.5 * (1.0 - energy_gap), 2)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank them, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
