import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import axios from 'axios';
import Navbar from './Navbar';

export default function Pokemon() {
  let params = useParams();
  const [pokemon, setPokemon] = useState({})
  const [pokemonAbilities, setPokemonAbilities] = useState({})
  const [pokemonStats, setPokemonStats] = useState({})

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/get-pokemon-data?pokemon_id=${params.pokemonId}`)
    .then(response => {
        setPokemon(response.data)
    })
    axios.get(`http://127.0.0.1:8000/api/get-abilities?pokemon_id=${params.pokemonId}`)
    .then(response => {
        setPokemonAbilities(response.data)
    })
    axios.get(`http://127.0.0.1:8000/api/get-stats?pokemon_id=${params.pokemonId}`)
    .then(response => {
        setPokemonStats(response.data)
    })
  }, []);

  return (
    <div>
      <header className="PokemonList-header">
              <Navbar />
      </header>
      <div className="flex">
        <div className="w1-/6 h-screen">
          <img className="w-30 h-30 rounded-full m-2 p-2" src="/blank-profile.png" alt="" width="200" height="200"/>
        </div>
        <div className="h-screen w-5/6 ml-3">
          <h1 className="mt-3 text-5xl font-extrabold">{pokemon.name}</h1>
          <p className="font-extralight mt-2">Generation {pokemon.generation}</p>
          <div className="mt-3">
            <h3 className="text-3xl">Type</h3>
            <div className="flex">
              <p>{pokemon.type_1}</p>
              <p className="ml-3">{pokemon.type_2}</p>
            </div>
            <h3 className="text-3xl mt-5">Abilities</h3>
            <div className="flex">
              <p>{pokemonAbilities.ability_1}</p>
              <p className="ml-3">{pokemonAbilities.ability_2}</p>
              <p className="ml-3">{pokemonAbilities.ability_hidden}</p>
            </div>
            <h3 className="text-3xl mt-5">Stats</h3>
            <div>
              <p>HP: {pokemonStats.hp}</p>
              <p>Attack: {pokemonStats.attack}</p>
              <p>Special Attack: {pokemonStats.sp_attack}</p>
              <p>Defense: {pokemonStats.defense}</p>
              <p>Special Defense: {pokemonStats.sp_defense}</p>
              <p>Speed: {pokemonStats.speed}</p>
              <p>Total: {pokemonStats.total_points}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}