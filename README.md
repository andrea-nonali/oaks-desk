# Oak's Desk

A Pokémon competitive battle analytics API and dashboard. The dataset covers all 8 generations (updated through 2020).

**Coolest feature:** given any Pokémon, the API finds every other Pokémon that fully covers its type weaknesses, a query no popular competitive site provides directly.

---

## Stack

**Backend** — Django · Django REST Framework · SQLite · Pipenv  
**Frontend** — React · Tailwind CSS

---

## API Endpoints

| Endpoint | Query params | Description |
|---|---|---|
| `GET /api/get-all-pokemons` | — | All Pokémon |
| `GET /api/get-pokemon-data` | `pokemon_id` | Full data for a single Pokémon |
| `GET /api/get-abilities` | `pokemon_id` | Abilities for a Pokémon |
| `GET /api/get-stats` | `pokemon_id` | Base stats for a Pokémon |
| `GET /api/get-weak-against-pokemons` | `pokemon_id` | Types this Pokémon is weak against (multiplier > 1) |
| `GET /api/get-strong-against-pokemons` | `pokemon_id` | Types this Pokémon resists (multiplier < 1) |
| `GET /api/get-neutral-against-pokemons` | `pokemon_id` | Types this Pokémon is neutral to |
| `GET /api/get-fully-covering-pokemons` | `pokemon_id`, `generation` (optional) | Pokémon that cover all type weaknesses |
| `GET /api/get-mega-evolutions` | `generation` (optional) | All Pokémon with a mega evolution |
| `GET /api/get-best_pokemons_stats` | `generation`, `type`, `include_legendaries`, `include_mythicals`, `include_mega_evolutions` | Pokémon ranked by base stat total |

---

## Quick Start

### Backend

```bash
cd src/Backend
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

### Frontend

```bash
cd src/Frontend/frontend
npm install
npm start
```

### Tests

```bash
cd src/Backend
pipenv run python manage.py test coreAPI
```

---

## Requirements

- Python 3.9, Pipenv
- Node.js

---

## Data Source

[Complete Pokémon dataset (Kaggle)](https://www.kaggle.com/mariotormo/complete-pokemon-dataset-updated-090420)
