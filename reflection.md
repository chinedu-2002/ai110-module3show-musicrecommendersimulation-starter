# Reflection: Profile Comparisons

## High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile (genre: pop, mood: happy, energy: 0.85) surfaced upbeat, fast-tempo dance tracks at the top — "Saturday Feeling" and "Sunrise City." The Chill Lofi profile (genre: lofi, mood: chill, energy: 0.38) returned slow, atmospheric study tracks — "Library Rain" and "Midnight Coding." The contrast is sharp and makes intuitive sense: the two profiles sit at opposite ends of the energy scale and belong to completely different genres, so almost none of the same songs appear in both lists. The system correctly treated these as two very different listeners.

## Chill Lofi vs. Deep Intense Rock

The Chill Lofi profile favored quiet, high-acousticness tracks (energy ~0.35–0.42). The Deep Intense Rock profile (genre: rock, mood: intense, energy: 0.92) favored distorted, high-tempo songs (energy ~0.89–0.95). The top-3 for rock were all clustered within 0.02 score points of each other — Storm Runner, Thunder Anthem, and Rage Circuit — because the catalog only has three rock/intense songs. The lofi list was similarly saturated with lofi tracks filling the top 4 slots. This reveals a real limitation: a small catalog means genre-matching users see the same songs repeatedly regardless of minor preference differences.

## High-Energy Pop vs. Deep Intense Rock

Both profiles have high energy targets (0.85 vs. 0.92) and upbeat/intense moods. Yet their lists share zero songs in the top 5. The genre weight (+2.0) is strong enough to keep pop and rock completely separated even when energy profiles nearly overlap. A user who listens to both high-energy pop and rock would get no cross-genre discovery from this system — which is exactly the filter bubble problem. If genre weight were lowered to +0.5, "Gym Hero" (pop/intense, energy 0.93) would likely appear in the rock profile's top 5 because its energy is a near-perfect match, even though its genre is different.
