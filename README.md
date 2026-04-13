# Music Recommender Simulation

## Project Summary

This project simulates how a content-based music recommendation system works. Given a user's taste profile (preferred genre, mood, and energy level), the system scores every song in a catalog and returns the top 5 matches along with plain-English reasons for each recommendation.

The goal is to make the inner workings of a recommender transparent and testable rather than treating it as a black box.

---

## How The System Works

Real-world platforms like Spotify combine two main strategies:

- **Content-based filtering** scores songs by comparing their audio features (genre, energy, mood) directly to the user's stated preferences.
- **Collaborative filtering** uses the listening history of many users to surface songs that "people like you" enjoy.

This simulation uses content-based filtering only.

### Song features

Each `Song` stores: `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

### User profile fields

A `UserProfile` (OOP path) stores: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.  
The functional path uses a plain dict with keys `genre`, `mood`, and `energy`.

### Algorithm Recipe

For each song the system computes:

| Rule | Points |
|---|---|
| Genre matches user preference | +2.0 |
| Mood matches user preference | +1.0 |
| Energy similarity `1.5 × (1 − |song_energy − target_energy|)` | 0–1.5 |
| Acoustic match (OOP only, when `likes_acoustic=True` and `acousticness ≥ 0.7`) | +0.5 |

Songs are then sorted highest-to-lowest and the top K are returned.

**Potential bias:** giving genre double the weight of mood means songs from the preferred genre almost always dominate the list, even when a cross-genre song would be a better energy and mood fit. This is a deliberate trade-off that creates a mild filter bubble.

### Data flow

```
Input: User Prefs (genre, mood, energy)
       ↓
Load: data/songs.csv  →  list of song dicts
       ↓
Score: score_song(user_prefs, song) → (float, [reasons])  ← applied to every song
       ↓
Rank: sorted by score descending
       ↓
Output: Top-K (song, score, explanation) tuples
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac / Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the recommender:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments

### Weight Shift: doubling energy, halving genre

When the genre weight was reduced to +1.0 and the energy multiplier raised to 3.0, the High-Energy Pop profile promoted "Bass Drop Kingdom" (EDM, energy 0.97) above several pop songs. The results felt less aligned to genre preference but more consistent in raw sonic intensity. This shows how sensitive the system is to the relative importance of each weight.

### Feature Removal: dropping mood

Commenting out the mood bonus (+1.0) made the Chill Lofi and Rock profiles nearly indistinguishable in their #3–5 positions because those slots were previously broken by mood tiebreakers. Rankings became flatter and harder to explain to a user.

### Three user profiles tested

| Profile | Top Result | Score | Notes |
|---|---|---|---|
| High-Energy Pop | Saturday Feeling | 4.50 | Perfect genre + mood + energy match |
| Chill Lofi | Library Rain | 4.46 | Top 4 all lofi — catalog saturation visible |
| Deep Intense Rock | Storm Runner | 4.48 | Top 3 near-tied; only 3 rock/intense songs exist |

---

## Limitations and Risks

- Only works on a 20-song catalog; real systems have millions of tracks.
- No user history — recommends the same songs every time for the same profile.
- Genre weight dominance can create a filter bubble (users rarely see cross-genre suggestions).
- Underrepresented genres (folk, EDM, ambient) give users fewer choices.
- Does not consider lyrics, language, or cultural context.

See [model_card.md](model_card.md) for a full bias analysis.

---

## Reflection

See the Personal Reflection section in [model_card.md](model_card.md).

Key takeaways:
- A recommender is a sorting algorithm whose weights encode a point of view. Choosing those weights is a design decision with real consequences for what users see.
- Content-based filtering is surprisingly effective at producing results that *feel* intelligent, but achieving genuine diversity and fairness requires deliberate extra work beyond a simple scoring formula.
