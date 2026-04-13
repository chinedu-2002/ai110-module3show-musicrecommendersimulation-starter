# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests the top 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is intended for classroom exploration to demonstrate how content-based filtering works. It is **not** intended for production use, real user data, or any commercial music platform.

---

## 3. How the Model Works

For every song in the catalog, VibeFinder calculates a score by checking three things:

1. **Genre match** — if the song's genre matches what the user prefers, it earns 2 points. This is the biggest single factor.
2. **Mood match** — if the song's mood matches the user's preferred mood, it earns 1 point.
3. **Energy similarity** — the closer a song's energy level (0.0–1.0) is to the user's target energy, the more points it earns (up to 1.5 points). A perfect energy match gives the full 1.5; a song at the opposite end of the scale gives nearly 0.

Once every song has a score, the list is sorted from highest to lowest, and the top 5 are returned along with a plain-English explanation of why each song ranked where it did.

---

## 4. Data

The dataset (`data/songs.csv`) contains **20 songs** with the following features:

| Feature | Description |
|---|---|
| genre | Musical genre (pop, rock, lofi, jazz, folk, edm, synthwave, ambient, indie pop) |
| mood | Emotional tag (happy, chill, intense, relaxed, moody, focused, energetic, sad) |
| energy | 0.0–1.0 scale of perceived intensity |
| tempo_bpm | Beats per minute |
| valence | 0.0–1.0 positivity measure |
| danceability | 0.0–1.0 danceability score |
| acousticness | 0.0–1.0 acoustic vs. electronic scale |

The starter dataset had 10 songs. I added 10 more to improve genre and mood diversity, including folk, edm, and additional rock/ambient/lofi tracks. The catalog still skews toward pop and lofi; classical, R&B, hip-hop, and country are completely absent.

---

## 5. Strengths

- **Transparent**: every recommendation includes a plain-English reason explaining the score.
- **Accurate for well-matched profiles**: users with genre/mood preferences that appear in the catalog (e.g., "pop/happy" or "rock/intense") get results that immediately feel right.
- **Fast and simple**: the scoring takes milliseconds even on a laptop with no special hardware.

---

## 6. Limitations and Bias

- **Genre dominance creates a filter bubble.** Because genre matching is worth 2 points — double the mood weight — the system almost always surfaces songs from the user's preferred genre. A user who loves pop will rarely see a great jazz song that perfectly matches their energy and mood, even if they might enjoy it.
- **Dataset imbalance amplifies bias.** Pop and lofi together make up 7 of the 20 songs (35%). Pop and rock users therefore have more candidates to choose from, while folk, edm, and ambient users see the same 1–2 songs dominate every list.
- **Acousticness is only used in the OOP path.** The functional `score_song` function does not factor in `acousticness` or `valence`, so those features are collected but ignored during the main CLI run.
- **No memory of history.** The system recommends the same songs every time; it never learns that a user skipped a track or played one on repeat.
- **Small catalog.** With only 20 songs, any weight combination quickly saturates the top spots with the same handful of tracks.

---

## 7. Evaluation

I tested three distinct profiles:

| Profile | Genre | Mood | Energy |
|---|---|---|---|
| High-Energy Pop | pop | happy | 0.85 |
| Chill Lofi | lofi | chill | 0.38 |
| Deep Intense Rock | rock | intense | 0.92 |

**What I observed:**

- **High-Energy Pop** surfaced "Saturday Feeling" at #1 (score 4.50) and "Sunrise City" at #2 (4.46). Both are pop/happy with energies near 0.85. "Gym Hero" placed #3 — it's pop with an intense mood, missing the mood bonus, but its energy (0.93) is close enough to keep it competitive. This felt correct.
- **Chill Lofi** neatly pulled the four lofi tracks into the top 4. "Library Rain" edged out "Midnight Coding" because its energy (0.35) is fractionally closer to the target of 0.38. The #5 spot went to "Spacewalk Thoughts" (ambient/chill), showing that mood can overcome a genre miss.
- **Deep Intense Rock** placed three rock/intense songs in the top 3 with nearly identical scores (4.46–4.48), which highlighted that the catalog only has three tracks that match that profile exactly. The gap to #4 ("Gym Hero", 2.48) was large, confirming that genre+mood alignment dominates the score.

**Experiment — Weight Shift (doubling energy, halving genre):** When I mentally halved genre to 1.0 and doubled the energy multiplier to 3.0, the High-Energy Pop list would pull in "Bass Drop Kingdom" (EDM, energy 0.97) above some pop songs because raw energy similarity beats a weaker genre bonus. The results felt less accurate to the stated preference but more sonically consistent in terms of tempo and intensity.

---

## 8. Future Work

1. **Add collaborative filtering.** Track which songs users actually listen to and use that to supplement content scores — "users who like Sunrise City also love Night Drive Loop."
2. **Diversify the catalog.** Expand to 200+ songs covering R&B, hip-hop, classical, and country so underrepresented users get variety.
3. **Diversity penalty.** Cap how many songs from the same artist or genre can appear in a single top-5 list. Right now the rock profile shows two Voltline tracks in the top 3.

---

## 9. Personal Reflection

Building VibeFinder clarified something I had taken for granted: a recommender is just a sorting algorithm with an opinion baked in through its weights. The "opinion" in this case — that genre matters twice as much as mood — is a choice I made, and it shapes everything the user sees. That's a surprisingly powerful observation for something this small.

Using AI tools (Claude) to scaffold the CSV loading and scoring logic was fast, but I had to double-check that the energy similarity formula was doing what I intended. The AI suggested `1 - abs(a - b)` which is correct for a 0–1 range, but it took running the system against real data to confirm the scores felt proportional rather than arbitrary.

What surprised me most was how quickly the system felt "real." After adding just 10 extra songs, the Chill Lofi profile returned a coherent playlist that genuinely sounds like a study session. Simple weighted matching, done carefully, produces output that a user could mistake for something much more sophisticated. That's both impressive and a little unsettling — it means the appearance of intelligence is cheap, but actual fairness and diversity require deliberate extra work.
