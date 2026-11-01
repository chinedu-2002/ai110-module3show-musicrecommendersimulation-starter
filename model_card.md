# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0 — Music Recommender Simulation**

## 2. Intended Use

### Goal / Task

Suggest the top songs in a small catalog for an explicitly provided musical taste profile. The user chooses a favorite genre, a favorite mood, and a target energy between 0 and 1. The system ranks songs by those preferences and explains every score.

This is a classroom demonstration for exploring recommendation logic, feature weights, and bias. Its scores measure agreement with the chosen rules; they are not probabilities that a listener will enjoy a song.

### Non-Intended Use

This version is not designed to replace a streaming service, learn a listener's tastes automatically, or measure the quality of an artist. It should not be used for decisions about artist payments or promotion, or to infer someone's identity, emotions, or mental health.

## 3. How the Model Works

The system uses a weighted content-based rule. A matching genre earns 2 points and a matching mood earns 1 point. Energy earns up to 1 point: an exact match earns the full point, and the points decrease by the distance from the target. For example, energy 0.82 is 0.02 away from a target of 0.80, so it earns 0.98 points. A song matching both labels at that energy scores 3.98 out of 4.

Every song is scored independently. The program then sorts the complete list from highest score to lowest and returns the requested number of songs. Exact ties preserve the original catalog order. Explanations show the contribution from genre, mood, and energy, including zero points for mismatches.

The project fills in the starter's unfinished loading, scoring, ranking, and explanation behavior. It keeps the starter's `Song`, `UserProfile`, and `Recommender` interface while adding dictionary-based functions, validation, selectable profiles, and a separate set of experimental weights. The baseline uses hand-chosen weights and does not train on other users' behavior.

## 4. Data

The catalog contains **20 fictional songs**, with **14 genre labels** and **13 mood labels**. The original 10 starter rows are preserved, and 10 AI-generated rows were added with the same CSV headers. The additions include r&b, Indian classical, afrobeats, country, salsa, classical, and hip hop, as well as extra pop and rock examples. The metadata are illustrative values, not measurements extracted from real recordings.

The loader reads `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. It converts the ID and numeric features to numbers and validates their ranges. **Only genre, mood, and energy affect scores.** Title and artist identify the results; tempo, valence, danceability, and acousticness are available for future work. The starter's `likes_acoustic` preference is retained for compatibility but does not affect this scoring rule.

Pop has 4 songs, lofi has 3, rock has 2, and each of the other 11 genres has 1. Happy, chill, and intense each have 3 songs; sad has 2; the other 9 moods each have 1. There are no listening histories, likes, skips, lyrics, audio files, or human preference ratings. The dataset cannot represent the full range of musical taste.

## 5. Strengths

The default profiles produce results consistent with their labels and target energy. Library Rain leads the chill lofi list with a perfect 4.00 because it matches lofi, chill, and energy 0.35. Storm Runner leads the intense rock list with 3.99, while Sunrise City leads the happy pop list with 3.98. These results fit the metadata, although the fictional songs cannot be evaluated by listening.

Energy rewards closeness rather than assuming that louder or more intense music is always better. Explanations also make surprising results inspectable: Gym Hero reaches the happy pop top five despite its intense mood because its genre match earns 2 points. The same scoring function drives the functional and object interfaces, so their explanations agree with their rankings.

## 6. Limitations and Bias

The tiny catalog gives pop listeners four same-genre options, while eleven genres have only one each, so the available choices are uneven. A 2-point genre match can outweigh a better mood and energy match from another genre, as Rooftop Lights shows for the pop profile. Exact labels treat pop and indie pop as unrelated, and repeated recommendations from the same labels could reinforce a filter bubble because there is no diversity or exploration rule. Scores ignore lyrics, language, cultural context, and listening feedback, so a high score does not establish that someone will enjoy a song.

## 7. Evaluation

The following commands were run against the expanded catalog:

```text
python -m src.main --all-profiles
python -m src.main --profile pop --experiment
python -m pytest -q
```

The test suite passed: **35 tests**. These check software behavior, including loading, scoring, ranking, validation, and compatibility with the starter interface. Separate CLI runs checked the profile output and command-line error handling. These checks do not measure musical recommendation accuracy. Complete terminal output with scores and reasons is included in the README.

### Profiles and Observed Results

| Profile | Genre / mood / target energy | First recommendation | Score | Observation |
| --- | --- | --- | --- | --- |
| High-Energy Pop | pop / happy / 0.80 | Sunrise City | 3.98 | Golden Hour Parade also scores 3.98; catalog order resolves the tie. |
| Chill Lofi | lofi / chill / 0.35 | Library Rain | 4.00 | The exact energy match puts it above Midnight Coding at 3.93. |
| Deep Intense Rock | rock / intense / 0.90 | Storm Runner | 3.99 | Afterburn also scores 3.99; both match the requested genre and mood. |
| Conflicting: High-Energy Sad Pop | pop / sad / 0.90 | Neon Goodbye | 3.98 | Sad mood and high energy are valid independent preferences. |
| Unknown Genre and Mood | opera / mysterious / 0.50 | Velvet Heartbreak | 0.98 | Neither requested label exists, so every ranking uses energy alone. |

The sad, energetic profile is an edge case, not an invalid combination: a song can be emotionally sad and still energetic. The unknown-label profile exposes a different limitation: returning Velvet Heartbreak does not mean the system understands opera or mysterious music. It is simply the closest energy value in the catalog.

### Pairwise Profile Comparisons

The table covers all ten pairs of the five profiles. "Pop," "lofi," and "rock" refer to the first three profiles above; "sad pop" and "unknown" refer to the last two.

| Pair | What changed and why it makes sense |
| --- | --- |
| Pop / lofi | All five results differ: the pop list starts with Sunrise City and Golden Hour Parade, while the lofi list starts with Library Rain and Midnight Coding, following the different labels and lower energy target of 0.35. |
| Pop / rock | Storm Runner and Afterburn replace the happy pop leaders because rock and intense match; Gym Hero and Neon Goodbye remain in both top fives because their high energy helps both profiles. |
| Lofi / rock | These top fives share no songs because chill lofi near energy 0.35 and intense rock near 0.90 reward opposite parts of this catalog. |
| Pop / sad pop | Four songs stay in the top five, but Neon Goodbye rises from third to first when sad becomes the preferred mood and the energy target rises to 0.90. |
| Pop / unknown | The top fives share no songs because the unknown profile earns no label points and instead favors moderate-energy tracks such as Velvet Heartbreak. |
| Lofi / sad pop | These top fives share no songs because the sad pop profile rewards pop and sad labels plus much higher energy, while lofi rewards its quieter chill tracks. |
| Lofi / unknown | Midnight Coding, Focus Flow, and Coffee Shop Stories appear in both lists, but Velvet Heartbreak leads the unknown list through energy closeness alone instead of the lofi and chill bonuses that favor Library Rain. |
| Rock / sad pop | Neon Goodbye rises from fourth in rock to first in sad pop because both requested labels match; Storm Runner and Afterburn drop out when their rock and intense bonuses disappear. |
| Rock / unknown | These top fives share no songs because rock rewards intense tracks near 0.90, while unknown has no label bonuses and ranks tracks by distance from 0.50. |
| Sad pop / unknown | Velvet Heartbreak moves from fifth to first because unknown removes the pop genre advantage and its energy target of 0.50 is close to that song's 0.48. |

### Controlled Weight Experiment

The experiment keeps the catalog, happy pop profile, mood weight, and top-five size unchanged. It halves the genre weight from 2 to 1 and doubles the energy weight from 1 to 2. Each configuration still has a maximum possible score of 4. The baseline remains available separately.

| Song | Baseline rank | Baseline score | Experiment rank | Experiment score |
| --- | ---: | ---: | ---: | ---: |
| Sunrise City | 1 | 3.98 | 1 | 3.96 |
| Golden Hour Parade | 2 | 3.98 | 2 | 3.96 |
| Rooftop Lights | 5 | 1.96 | 3 | 2.92 |
| Neon Goodbye | 3 | 2.92 | 4 | 2.84 |
| Gym Hero | 4 | 2.87 | 5 | 2.74 |

Rooftop Lights is the most informative change. Its indie pop label receives no genre points, but happy matches and its energy of 0.76 is close to 0.80. Giving energy more influence moves it above the two pop tracks with mismatched moods. All five songs remain in the top five, and the leading two songs remain tied. This demonstrates sensitivity to the weights; it does not demonstrate improved accuracy because no listener ratings or user feedback were collected.

## 8. Future Work

- Allow several favorite genres and mood tags, and explore relationships such as pop and indie pop instead of relying only on exact labels.
- Add a simple artist or genre diversity rule and measure how it changes relevance and variety for each profile.
- Evaluate a larger, more balanced catalog with listener feedback before tuning weights or adding scored features such as acousticness and tempo.

## 9. Personal Reflection

**AI-assisted reflection draft for student review:** The paragraphs below describe lessons supported by this implementation. Review and personalize them before submission so the reflection represents your own learning and experience.

The central learning point in this project is the difference between scoring one song and ranking the whole catalog. The energy calculation makes that distinction concrete: closeness creates a useful numerical signal, and sorting turns those signals into suggestions. A surprising result is that such a small rule can produce recognizable pop, lofi, and rock lists without training a model. Rooftop Lights also shows how a plausible recommendation can be hidden by an exact genre label and a strong weight.

AI assistance supported research, implementation, dataset expansion, and documentation, but the generated work needed checks against the starter interfaces, the CSV schema, and actual terminal output. Manual score calculations and automated tests help check the math, while official sources help check descriptions of real recommendation systems. The weight experiment is a reminder that a changed ranking is not evidence of a better listening experience. A useful next step would be a more balanced catalog and listener feedback, followed by a small diversity rule whose effects can be compared with the baseline.
