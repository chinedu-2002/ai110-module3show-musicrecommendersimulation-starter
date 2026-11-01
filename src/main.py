"""Run reproducible profile demonstrations and a controlled weight experiment."""

import argparse
import csv
from pathlib import Path

from .recommender import BASELINE, ENERGY_FOCUSED, ScoringWeights, load_songs, recommend_songs


PROFILES = {
    "pop": {"genre": "pop", "mood": "happy", "energy": 0.80},
    "lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "rock": {"genre": "rock", "mood": "intense", "energy": 0.90},
    "conflicting": {"genre": "pop", "mood": "sad", "energy": 0.90},
    "unknown": {"genre": "opera", "mood": "mysterious", "energy": 0.50},
}
PROFILE_NAMES = {
    "pop": "High-Energy Pop",
    "lofi": "Chill Lofi",
    "rock": "Deep Intense Rock",
    "conflicting": "Conflicting: High-Energy Sad Pop",
    "unknown": "Unknown Genre and Mood",
}
DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def display_profile(songs: list[dict], name: str, k: int, weights: ScoringWeights) -> None:
    """Print the profile and ranked songs with all scoring reasons."""
    prefs = PROFILES[name]
    print(f"\nProfile: {PROFILE_NAMES[name]}")
    print(f"Preferences: genre={prefs['genre']}, mood={prefs['mood']}, energy={prefs['energy']:.2f}")
    print(f"Weights: genre={weights.genre:.2f}, mood={weights.mood:.2f}, energy={weights.energy:.2f}")
    recommendations = recommend_songs(prefs, songs, k, weights)
    if not recommendations:
        print("No recommendations.")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']} | Score: {score:.2f}")
        print(f"   Because: {explanation}")


def main(argv: list[str] | None = None) -> None:
    """Parse CLI options and run the baseline, all profiles, or weight experiment."""
    parser = argparse.ArgumentParser(description="VibeFinder: an explainable music recommender")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CATALOG, help="Path to the song catalog")
    parser.add_argument("--profile", choices=PROFILES, default="pop", help="Taste profile to use")
    parser.add_argument("--all-profiles", action="store_true", help="Run all five evaluation profiles")
    parser.add_argument("--experiment", action="store_true", help="Compare baseline and energy-focused weights")
    parser.add_argument("--k", type=int, default=5, help="Number of songs to recommend (default: 5)")
    args = parser.parse_args(argv)
    if args.k < 0:
        parser.error("--k must be nonnegative")
    try:
        songs = load_songs(args.csv)
    except (OSError, ValueError, csv.Error) as exc:
        parser.error(str(exc))
    print(f"Loaded songs: {len(songs)}")
    names = list(PROFILES) if args.all_profiles else [args.profile]
    for name in names:
        if args.experiment:
            print("\n=== Baseline ===")
        display_profile(songs, name, args.k, BASELINE)
        if args.experiment:
            print("\n=== Experiment: halve genre weight; double energy weight ===")
            display_profile(songs, name, args.k, ENERGY_FOCUSED)


if __name__ == "__main__":
    main()
