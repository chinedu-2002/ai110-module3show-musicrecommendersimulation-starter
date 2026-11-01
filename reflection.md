# Reflection: Profile Comparisons

These comparisons describe actual results from the current implementation. The full AI-assisted engineering reflection is in [model_card.md](model_card.md#9-personal-reflection), and all five profile outputs appear in the [README](README.md#sample-recommendation-output).

## High-Energy Pop vs. Chill Lofi

The pop profile requests pop, happy, and energy 0.80. Sunrise City leads at 3.98, tied with Golden Hour Parade. The lofi profile requests lofi, chill, and energy 0.35. Library Rain leads at 4.00 because all three requested attributes match exactly. The two top-five lists share no songs: both the category bonuses and the target intensity change.

## Chill Lofi vs. Deep Intense Rock

The rock profile requests rock, intense, and energy 0.90. Storm Runner and Afterburn lead at 3.99, while the quieter Library Rain and Midnight Coding lead for lofi. These top-five lists also share no songs. This follows from both the different labels and the large difference between the target energies, rather than from an assumption that higher energy is always better.

## High-Energy Pop vs. Deep Intense Rock

Both profiles target relatively high energy, but their genre and mood bonuses favor different leaders. Gym Hero and Neon Goodbye appear in both top-five lists. Gym Hero is fourth for happy pop at 2.87, where only genre matches; it is third for intense rock at 1.97, where only mood matches. Those scores express agreement with different profiles, so they should not be interpreted as a universal measure of song quality.

## What the Weight Experiment Shows

Halving genre weight and doubling energy weight moves Rooftop Lights from fifth to third for the happy pop profile. Its happy mood and nearby energy outweigh the reduced genre advantage of the sad and intense pop tracks. This is a useful example of how a design choice can hide a plausible cross-genre recommendation. The changed order does not prove that listeners would prefer the experimental list; that would require feedback.
