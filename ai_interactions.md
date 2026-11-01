# AI Interactions Log

## Actual Request and Scope

The student's instruction was: **"work on this task"**, accompanied by the Week 7 CodePath project PDF. The PDF supplied assignment requirements. It was treated as a specification for the local project, not as authorization to publish to an account or submit work through the course site.

The assistant extracted the PDF, downloaded the linked public starter repository, implemented the Python CLI, and produced evaluation documentation. No student listening feedback or personal experience was supplied. The personal reflection is therefore labeled as an AI-assisted draft for student review.

## What AI Generated or Changed

- Preserved the starter's ten songs and appended ten fictional songs with valid existing headers and varied genres/moods. Added values are illustrative rather than measured audio features.
- Implemented CSV parsing and validation, weighted scoring with reasons, stable top-k ranking, and working adapters for the starter's Song/UserProfile/Recommender interface.
- Fixed the starter's import so `python -m src.main` runs as instructed. Added three main profile dictionaries and two adversarial profiles.
- Added a controlled weight experiment, functional tests, captured output, README, model card, and submission instructions.
- Removed unused pandas/Streamlit dependencies. The CLI needs no third-party packages; pytest supports verification.

## Agentic Workflow

The primary assistant coordinated separate agents for a rubric/edge-case review and research using official recommendation sources. The review agent also wrote the new functional tests and independently checked the completed implementation. The research agent drafted the model card using actual runs.

These were assistant task instructions, **not additional prompts the student wrote**. Representative actual delegated instructions included:

> "Read the extracted assignment requirements in current conversation and independently prepare a concise acceptance checklist and meaningful edge cases for a CLI Python music recommender."

> "Find 2-3 primary official sources explaining real music/YouTube recommendations, contrasting collaborative filtering (behavior of similar users/items) vs content-based (item attributes)"

## Scoring Logic Design

The assistant selected the assignment's suggested baseline: genre match earns 2 points, mood match earns 1, and energy earns `1 - abs(song_energy - target_energy)`. Thus both a quieter and a louder song lose points when equally far from the target. Numeric values are validated before scoring; this keeps similarity within 0 to 1.

The proposed High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles differ in both categorical preferences and intensity, so they can distinguish more than loud versus quiet music. A single favorite genre is still narrow. High-energy sad pop deliberately separates mood from energy: a sad track need not be quiet. An unavailable opera/mysterious profile tests what happens when only the energy feature can contribute.

## Configuration-Based Ranking Strategies

The project uses a simple configuration-based strategy: one scoring function accepts an immutable `ScoringWeights` object. `BASELINE` is `(genre=2, mood=1, energy=1)` and `ENERGY_FOCUSED` is `(genre=1, mood=1, energy=2)`. This keeps one implementation of the score and its explanations; there is no need for separate strategy subclasses for two sets of weights.

The assistant chose this structure to make the required sensitivity experiment repeatable without editing global constants or accidentally losing the baseline. `--experiment` runs both configurations on the same profile and catalog. This is a transparent weight comparison; it does not train or optimize a model.

## Verification Performed by the Assistant

- Ran all tests: **35 passed**, including the two original starter tests unchanged.
- Ran all five profiles and captured their actual terminal output in `evaluation/profiles.txt` and the README.
- Ran the controlled pop experiment and captured both rankings in `evaluation/weight_experiment.txt` and the README.
- Checked exact-match scoring, contribution explanations, symmetric energy closeness, stable ties, original object identity, catalog non-mutation, k boundaries, CSV numeric conversion, duplicate IDs, and invalid/nonfinite values.
- Checked CLI help, empty-result behavior, negative k, and missing catalog errors.
- Compared the original CSV rows with the expanded file; all ten starter rows are retained.
- Verified that the catalog has 20 rows, 14 genres, and 13 mood labels. This corrects an initial documentation estimate of 13 genres.

The assistant first checked the PDF reader and corrected environment access problems. During implementation, full-file patch attempts did not match the starter; the assistant rewrote the intended files and then verified them with tests and actual CLI runs. Text encoding and line endings were checked before final delivery.

These are assistant verification steps. They are not a claim that the student manually tested the program or agreed that the suggestions match their own taste. GitHub publication, public visibility, and course submission remain student actions described in `SUBMISSION.md`.
