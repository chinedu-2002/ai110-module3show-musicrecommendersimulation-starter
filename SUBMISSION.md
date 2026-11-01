# Submission Details

## Project

**VibeFinder 1.0 - Music Recommender Simulation** for CodePath AI110 Project 3 / Week 7.

Repository URL:

https://github.com/chinedu-2002/ai110-module3show-musicrecommendersimulation-starter

## Completed Work

- Working Python CLI with validated CSV loading, explained weighted scores, and stable top-k ranking.
- Twenty-song catalog with ten original starter songs and ten diverse added examples.
- Three main taste profiles, two supplementary edge cases, and actual captured output.
- Controlled experiment, all ten profile-pair comparisons, completed model card, and completed AI-assisted process reflection.
- Thirty-five passing tests and preserved starter interfaces.
- Existing public-fork history integrated without force-pushing.

## Publication and Course Status

GitHub publication is being finalized. Course submission requires an authenticated CodePath browser session and will be recorded here after it is confirmed.

The PDF lists a deadline of Sunday, November 1, 2026, at 10:59 PM CST. That date comes from the assignment PDF; the live course page may contain updates.

## Reproduce the Results

From this project folder:

```console
python -m src.main --all-profiles
python -m src.main --profile pop --experiment
python -m pytest -q
```

The accompanying source ZIP excludes Git internals, browser sessions, caches, and the assignment PDF. The original working folder retains the full Git history.
