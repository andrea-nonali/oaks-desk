from django.test import TestCase, Client

from coreAPI.models.pokemon import Pokemon, POKEMON_STATUS
from coreAPI.models.pokemon_stats import PokemonStats
from coreAPI.models.pokemon_type_intersections import PokemonTypeIntersections
from pokemonAPI.utils.iterators_operations import sort_dictionary_descending_order


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_pokemon(
    pokedex_number=1,
    name='Bulbasaur',
    japanese_name='フシギダネ',
    generation=1,
    status='Normal',
    species='Seed Pokemon',
    type_1='Grass',
    type_2='Poison',
    height_m=0.7,
    weight_kg=6.9,
):
    return Pokemon.objects.create(
        pokedex_number=pokedex_number,
        name=name,
        japanese_name=japanese_name,
        generation=generation,
        status=status,
        species=species,
        type_1=type_1,
        type_2=type_2,
        height_m=height_m,
        weight_kg=weight_kg,
    )


def make_type_intersections(pokemon, **overrides):
    """
    Default values represent a Grass/Poison type (Bulbasaur-like):
      weak (> 1):    fire, flying, ice, psychic
      strong (< 1):  fairy, fight, grass, water
      neutral (= 1): everything else
    """
    defaults = dict(
        against_bug=1.0,
        against_dark=1.0,
        against_dragon=1.0,
        against_electric=1.0,
        against_fairy=0.5,
        against_fight=0.5,
        against_fire=2.0,
        against_flying=2.0,
        against_ghost=1.0,
        against_grass=0.25,
        against_ground=1.0,
        against_ice=2.0,
        against_normal=1.0,
        against_poison=1.0,
        against_psychic=2.0,
        against_rock=1.0,
        against_steel=1.0,
        against_water=0.5,
    )
    defaults.update(overrides)
    return PokemonTypeIntersections.objects.create(pokemon=pokemon, **defaults)


def make_stats(pokemon, hp=45, attack=49, sp_attack=65, defense=49,
               sp_defense=65, speed=45, total_points=318):
    return PokemonStats.objects.create(
        pokemon=pokemon,
        hp=hp, attack=attack, sp_attack=sp_attack,
        defense=defense, sp_defense=sp_defense,
        speed=speed, total_points=total_points,
    )


# ---------------------------------------------------------------------------
# Utility: sort_dictionary_descending_order
# ---------------------------------------------------------------------------

class SortDictionaryDescendingOrderTest(TestCase):
    def test_sorts_values_descending(self):
        result = sort_dictionary_descending_order({'b': 1, 'a': 3, 'c': 2})
        self.assertEqual(list(result.items()), [('a', 3), ('c', 2), ('b', 1)])

    def test_empty_dict_returns_empty(self):
        self.assertEqual(sort_dictionary_descending_order({}), {})

    def test_single_entry_unchanged(self):
        self.assertEqual(sort_dictionary_descending_order({'x': 5}), {'x': 5})

    def test_ties_preserve_original_relative_order(self):
        result = sort_dictionary_descending_order({'a': 1, 'b': 1})
        self.assertEqual(set(result.keys()), {'a', 'b'})
        self.assertEqual(list(result.values()), [1, 1])


# ---------------------------------------------------------------------------
# Pokemon model: is_mega_evolution / has_mega_evolution / get_mega_evolution
# ---------------------------------------------------------------------------

class PokemonMegaEvolutionTest(TestCase):
    def setUp(self):
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur')
        self.charizard = make_pokemon(pokedex_number=6, name='Charizard', type_1='Fire', type_2='Flying')
        self.mega_charizard = make_pokemon(pokedex_number=6, name='Mega Charizard X', type_1='Fire', type_2='Dragon')

    def test_is_mega_evolution_false_for_base(self):
        self.assertFalse(self.bulbasaur.is_mega_evolution())
        self.assertFalse(self.charizard.is_mega_evolution())

    def test_is_mega_evolution_true_when_name_contains_mega(self):
        self.assertTrue(self.mega_charizard.is_mega_evolution())

    def test_is_mega_evolution_case_insensitive(self):
        upper = make_pokemon(pokedex_number=99, name='MEGA Venusaur')
        self.assertTrue(upper.is_mega_evolution())

    def test_has_mega_evolution_true(self):
        self.assertTrue(self.charizard.has_mega_evolution())

    def test_has_mega_evolution_false_for_standalone(self):
        # Bulbasaur has no mega in this test db
        self.assertFalse(self.bulbasaur.has_mega_evolution())

    def test_has_mega_evolution_false_when_self_is_mega(self):
        # A mega-evolution itself should not report having a mega
        self.assertFalse(self.mega_charizard.has_mega_evolution())

    def test_get_mega_evolution_returns_mega(self):
        result = self.charizard.get_mega_evolution()
        self.assertEqual(result, self.mega_charizard)

    def test_get_mega_evolution_returns_none_when_no_mega(self):
        result = self.bulbasaur.get_mega_evolution()
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Pokemon model: get_pokemon_by_name / get_pokemons_for
# ---------------------------------------------------------------------------

class PokemonQueryTest(TestCase):
    def setUp(self):
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur', generation=1)
        self.pikachu = make_pokemon(pokedex_number=25, name='Pikachu', generation=1, type_1='Electric', type_2='')
        self.chikorita = make_pokemon(pokedex_number=152, name='Chikorita', generation=2)

    def test_get_pokemon_by_name_exact_match(self):
        self.assertEqual(Pokemon.get_pokemon_by_name('Pikachu'), self.pikachu)

    def test_get_pokemon_by_name_case_insensitive(self):
        self.assertEqual(Pokemon.get_pokemon_by_name('pikachu'), self.pikachu)
        self.assertEqual(Pokemon.get_pokemon_by_name('PIKACHU'), self.pikachu)

    def test_get_pokemon_by_name_partial_match(self):
        self.assertEqual(Pokemon.get_pokemon_by_name('pika'), self.pikachu)

    def test_get_pokemon_by_name_not_found(self):
        self.assertIsNone(Pokemon.get_pokemon_by_name('MissingNo'))

    def test_get_pokemons_for_returns_all_when_no_generation(self):
        self.assertEqual(Pokemon.get_pokemons_for().count(), 3)

    def test_get_pokemons_for_filters_by_generation(self):
        gen1 = Pokemon.get_pokemons_for(generation=1)
        self.assertEqual(gen1.count(), 2)
        names = list(gen1.values_list('name', flat=True))
        self.assertIn('Bulbasaur', names)
        self.assertIn('Pikachu', names)

    def test_get_pokemons_for_generation_with_no_match(self):
        self.assertEqual(Pokemon.get_pokemons_for(generation=99).count(), 0)

    def test_str_includes_name_and_number(self):
        s = str(self.bulbasaur)
        self.assertIn('Bulbasaur', s)
        self.assertIn('1', s)


# ---------------------------------------------------------------------------
# PokemonTypeIntersections: weak / strong / neutral / covering
# ---------------------------------------------------------------------------

class PokemonTypeIntersectionsTest(TestCase):
    def setUp(self):
        # Bulbasaur (Grass/Poison): weak to fire, flying, ice, psychic
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur', generation=1)
        self.bulb_ti = make_type_intersections(self.bulbasaur)

    # --- get_weak_types_against ---

    def test_weak_types_contain_only_values_greater_than_one(self):
        result = self.bulb_ti.get_weak_types_against()
        for key, val in result.items():
            if key != 'pokemon':
                self.assertGreater(val, 1, msg=f'{key}={val} should be > 1')

    def test_weak_types_includes_expected_weaknesses(self):
        result = self.bulb_ti.get_weak_types_against()
        for expected in ('against_fire', 'against_flying', 'against_ice', 'against_psychic'):
            self.assertIn(expected, result)

    def test_weak_types_excludes_resistances(self):
        result = self.bulb_ti.get_weak_types_against()
        for excluded in ('against_grass', 'against_fairy', 'against_fight', 'against_water'):
            self.assertNotIn(excluded, result)

    def test_weak_types_includes_pokemon_name(self):
        result = self.bulb_ti.get_weak_types_against()
        self.assertEqual(result['pokemon'], 'Bulbasaur')

    # --- get_strong_types_against ---

    def test_strong_types_contain_only_values_less_than_one(self):
        result = self.bulb_ti.get_strong_types_against()
        for key, val in result.items():
            if key != 'pokemon':
                self.assertLess(val, 1, msg=f'{key}={val} should be < 1')

    def test_strong_types_includes_expected_resistances(self):
        result = self.bulb_ti.get_strong_types_against()
        for expected in ('against_fairy', 'against_fight', 'against_grass', 'against_water'):
            self.assertIn(expected, result)

    def test_strong_types_excludes_weaknesses(self):
        result = self.bulb_ti.get_strong_types_against()
        for excluded in ('against_fire', 'against_flying', 'against_ice', 'against_psychic'):
            self.assertNotIn(excluded, result)

    # --- get_neutral_types_against ---

    def test_neutral_types_contain_only_values_equal_to_one(self):
        result = self.bulb_ti.get_neutral_types_against()
        for key, val in result.items():
            if key != 'pokemon':
                self.assertEqual(val, 1.0, msg=f'{key}={val} should be 1.0')

    def test_neutral_types_includes_expected_neutrals(self):
        result = self.bulb_ti.get_neutral_types_against()
        for expected in ('against_bug', 'against_dark', 'against_dragon', 'against_electric',
                         'against_ghost', 'against_ground', 'against_normal', 'against_poison',
                         'against_rock', 'against_steel'):
            self.assertIn(expected, result)

    # --- get_fully_covering_pokemons ---

    def test_fully_covering_pokemon_found(self):
        # A Pokemon that resists all of Bulbasaur's weaknesses (fire, flying, ice, psychic)
        entei = make_pokemon(pokedex_number=244, name='Entei', generation=2, type_1='Fire', type_2='')
        make_type_intersections(
            entei,
            against_fire=0.5, against_flying=0.5, against_ice=0.5, against_psychic=0.5,
            against_fairy=0.5, against_fight=0.5, against_grass=0.25, against_water=0.5,
        )
        coverers = self.bulb_ti.get_fully_covering_pokemons()
        self.assertIn(entei, coverers)

    def test_partial_coverage_not_included(self):
        # Only resists fire — does not cover flying, ice, psychic
        squirtle = make_pokemon(pokedex_number=7, name='Squirtle', type_1='Water', type_2='')
        make_type_intersections(squirtle, against_fire=0.5)
        coverers = self.bulb_ti.get_fully_covering_pokemons()
        self.assertNotIn(squirtle, coverers)

    def test_fully_covering_filtered_by_generation(self):
        gen2_entei = make_pokemon(pokedex_number=244, name='Entei', generation=2, type_1='Fire', type_2='')
        make_type_intersections(
            gen2_entei,
            against_fire=0.5, against_flying=0.5, against_ice=0.5, against_psychic=0.5,
            against_fairy=0.5, against_fight=0.5, against_grass=0.25, against_water=0.5,
        )
        # Should appear in gen2 results but not gen1 results
        self.assertNotIn(gen2_entei, self.bulb_ti.get_fully_covering_pokemons(generation=1))
        self.assertIn(gen2_entei, self.bulb_ti.get_fully_covering_pokemons(generation=2))

    def test_no_coverers_when_none_exist(self):
        coverers = self.bulb_ti.get_fully_covering_pokemons()
        # No other Pokemon in db has been given the right resistances
        self.assertEqual(coverers, [])


# ---------------------------------------------------------------------------
# PokemonStats: _get_available_statuses_list
# ---------------------------------------------------------------------------

class PokemonStatsAvailableStatusesTest(TestCase):
    def test_always_includes_normal_and_sub_legendary(self):
        for include_leg, include_myth in [(True, True), (True, False), (False, True), (False, False)]:
            statuses = PokemonStats._get_available_statuses_list(include_leg, include_myth)
            self.assertIn(POKEMON_STATUS['normal'], statuses)
            self.assertIn(POKEMON_STATUS['sub_legendary'], statuses)

    def test_includes_legendary_when_flag_true(self):
        statuses = PokemonStats._get_available_statuses_list(True, False)
        self.assertIn(POKEMON_STATUS['legendary'], statuses)

    def test_excludes_legendary_when_flag_false(self):
        statuses = PokemonStats._get_available_statuses_list(False, True)
        self.assertNotIn(POKEMON_STATUS['legendary'], statuses)

    def test_includes_mythical_when_flag_true(self):
        statuses = PokemonStats._get_available_statuses_list(False, True)
        self.assertIn(POKEMON_STATUS['mythical'], statuses)

    def test_excludes_mythical_when_flag_false(self):
        statuses = PokemonStats._get_available_statuses_list(True, False)
        self.assertNotIn(POKEMON_STATUS['mythical'], statuses)

    def test_only_two_statuses_when_both_excluded(self):
        statuses = PokemonStats._get_available_statuses_list(False, False)
        self.assertEqual(len(statuses), 2)


# ---------------------------------------------------------------------------
# PokemonStats: get_best_base_total_stats_pokemon_for
# ---------------------------------------------------------------------------

class PokemonStatsRankingTest(TestCase):
    def setUp(self):
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur', generation=1,
                                     status='Normal', type_1='Grass', type_2='Poison')
        self.mewtwo = make_pokemon(pokedex_number=150, name='Mewtwo', generation=1,
                                   status='Legendary', type_1='Psychic', type_2='')
        self.mew = make_pokemon(pokedex_number=151, name='Mew', generation=1,
                                status='Mythical', type_1='Psychic', type_2='')
        self.bulb_stats = make_stats(self.bulbasaur, total_points=318)
        self.mewtwo_stats = make_stats(self.mewtwo, total_points=680)
        self.mew_stats = make_stats(self.mew, total_points=600)

    def test_results_ordered_by_total_descending(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for())
        totals = [r.total_points for r in results]
        self.assertEqual(totals, sorted(totals, reverse=True))

    def test_highest_stat_pokemon_is_first(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for())
        self.assertEqual(results[0].pokemon, self.mewtwo)

    def test_exclude_legendaries(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for(include_legendaries=False))
        names = [r.pokemon.name for r in results]
        self.assertNotIn('Mewtwo', names)
        self.assertIn('Bulbasaur', names)

    def test_exclude_mythicals(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for(include_mythicals=False))
        names = [r.pokemon.name for r in results]
        self.assertNotIn('Mew', names)
        self.assertIn('Mewtwo', names)

    def test_exclude_legendaries_and_mythicals(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for(
            include_legendaries=False, include_mythicals=False
        ))
        names = [r.pokemon.name for r in results]
        self.assertNotIn('Mewtwo', names)
        self.assertNotIn('Mew', names)
        self.assertIn('Bulbasaur', names)

    def test_filter_by_type(self):
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for(type='Psychic'))
        names = [r.pokemon.name for r in results]
        self.assertIn('Mewtwo', names)
        self.assertIn('Mew', names)
        self.assertNotIn('Bulbasaur', names)

    def test_filter_by_generation(self):
        chikorita = make_pokemon(pokedex_number=152, name='Chikorita', generation=2, type_1='Grass', type_2='')
        make_stats(chikorita, total_points=318)
        results = list(PokemonStats.get_best_base_total_stats_pokemon_for(generation=2))
        names = [r.pokemon.name for r in results]
        self.assertIn('Chikorita', names)
        self.assertNotIn('Mewtwo', names)

    def test_exclude_mega_evolutions(self):
        mega_mewtwo = make_pokemon(
            pokedex_number=150, name='Mega Mewtwo X', generation=1,
            status='Legendary', type_1='Psychic', type_2='Fighting',
        )
        make_stats(mega_mewtwo, total_points=780)
        results_with = list(PokemonStats.get_best_base_total_stats_pokemon_for(include_mega_evolutions=True))
        results_without = list(PokemonStats.get_best_base_total_stats_pokemon_for(include_mega_evolutions=False))
        with_names = [r.pokemon.name for r in results_with]
        without_names = [r.pokemon.name for r in results_without]
        self.assertIn('Mega Mewtwo X', with_names)
        self.assertNotIn('Mega Mewtwo X', without_names)


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

class PokemonsAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur', generation=1)
        self.pikachu = make_pokemon(pokedex_number=25, name='Pikachu', generation=1, type_1='Electric', type_2='')

    def test_get_all_pokemons_status_200(self):
        response = self.client.get('/api/get-all-pokemons')
        self.assertEqual(response.status_code, 200)

    def test_get_all_pokemons_returns_all_entries(self):
        data = self.client.get('/api/get-all-pokemons').json()
        self.assertEqual(len(data), 2)

    def test_get_all_pokemons_response_shape(self):
        data = self.client.get('/api/get-all-pokemons').json()
        pokemon = data[0]
        for field in ('id', 'pokedex_number', 'name', 'generation', 'status', 'type_1', 'type_2'):
            self.assertIn(field, pokemon)


class TypeIntersectionAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur')
        self.ti = make_type_intersections(self.bulbasaur)

    def test_weak_against_status_200(self):
        response = self.client.get(f'/api/get-weak-against-pokemons?pokemon_id={self.bulbasaur.id}')
        self.assertEqual(response.status_code, 200)

    def test_weak_against_returns_correct_pokemon_name(self):
        data = self.client.get(f'/api/get-weak-against-pokemons?pokemon_id={self.bulbasaur.id}').json()
        self.assertEqual(data['pokemon'], 'Bulbasaur')

    def test_weak_against_all_values_gt_1(self):
        data = self.client.get(f'/api/get-weak-against-pokemons?pokemon_id={self.bulbasaur.id}').json()
        for key, val in data.items():
            if key != 'pokemon':
                self.assertGreater(val, 1)

    def test_strong_against_status_200(self):
        response = self.client.get(f'/api/get-strong-against-pokemons?pokemon_id={self.bulbasaur.id}')
        self.assertEqual(response.status_code, 200)

    def test_strong_against_all_values_lt_1(self):
        data = self.client.get(f'/api/get-strong-against-pokemons?pokemon_id={self.bulbasaur.id}').json()
        for key, val in data.items():
            if key != 'pokemon':
                self.assertLess(val, 1)

    def test_neutral_against_status_200(self):
        response = self.client.get(f'/api/get-neutral-against-pokemons?pokemon_id={self.bulbasaur.id}')
        self.assertEqual(response.status_code, 200)

    def test_neutral_against_all_values_eq_1(self):
        data = self.client.get(f'/api/get-neutral-against-pokemons?pokemon_id={self.bulbasaur.id}').json()
        for key, val in data.items():
            if key != 'pokemon':
                self.assertEqual(val, 1.0)

    def test_weak_against_not_found_returns_404(self):
        response = self.client.get('/api/get-weak-against-pokemons?pokemon_id=99999')
        self.assertEqual(response.status_code, 404)

    def test_strong_against_not_found_returns_404(self):
        response = self.client.get('/api/get-strong-against-pokemons?pokemon_id=99999')
        self.assertEqual(response.status_code, 404)

    def test_fully_covering_status_200(self):
        response = self.client.get(f'/api/get-fully-covering-pokemons?pokemon_id={self.bulbasaur.id}')
        self.assertEqual(response.status_code, 200)

    def test_fully_covering_returns_list(self):
        data = self.client.get(f'/api/get-fully-covering-pokemons?pokemon_id={self.bulbasaur.id}').json()
        self.assertIsInstance(data, list)


class MegaEvolutionAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.charizard = make_pokemon(pokedex_number=6, name='Charizard', type_1='Fire', type_2='Flying')
        self.mega = make_pokemon(pokedex_number=6, name='Mega Charizard X', type_1='Fire', type_2='Dragon')
        self.bulbasaur = make_pokemon(pokedex_number=1, name='Bulbasaur')

    def test_get_mega_evolutions_status_200(self):
        response = self.client.get('/api/get-mega-evolutions')
        self.assertEqual(response.status_code, 200)

    def test_get_mega_evolutions_returns_list(self):
        data = self.client.get('/api/get-mega-evolutions').json()
        self.assertIsInstance(data, list)

    def test_get_mega_evolutions_includes_mega(self):
        data = self.client.get('/api/get-mega-evolutions').json()
        names = [p['name'] for p in data]
        self.assertIn('Mega Charizard X', names)

    def test_get_mega_evolutions_excludes_no_mega_pokemon(self):
        data = self.client.get('/api/get-mega-evolutions').json()
        names = [p['name'] for p in data]
        self.assertNotIn('Bulbasaur', names)
        self.assertNotIn('Charizard', names)

    def test_get_mega_evolutions_filtered_by_generation(self):
        gen2 = make_pokemon(pokedex_number=248, name='Tyranitar', generation=2, type_1='Rock', type_2='Dark')
        make_pokemon(pokedex_number=248, name='Mega Tyranitar', generation=2, type_1='Rock', type_2='Dark')
        data = self.client.get('/api/get-mega-evolutions?generation=2').json()
        names = [p['name'] for p in data]
        self.assertIn('Mega Tyranitar', names)
        self.assertNotIn('Mega Charizard X', names)
