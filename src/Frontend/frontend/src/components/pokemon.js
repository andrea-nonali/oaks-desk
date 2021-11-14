import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import axios from 'axios';

export default function Pokemon() {
  let params = useParams();
  const [pokemonData, setPokemonData] = useState({})

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/get-pokemon-data?pokemon-id=${params.pokemonId}`)
    .then(response => {
        setPokemonData(response.data)
    })
  }, []);

  return (
    <div>
        <div className="flex">
          <div className="w-1/6 bg-gray-500 h-screen">
            <img class="w-30 h-30 rounded-full m-2 p-2" src="/blank-profile.png" alt="" width="200" height="200"/>
          </div>
          <div className="w-5/6 bg-red-500 h-screen">
            <h1 className="mt-3 text-5xl font-extrabold">{pokemonData.name}</h1>
            <p className="font-extralight ml-2">Generation {pokemonData.generation}</p>
            <div className="mt-3">
              <h3 className="text-3xl">Type</h3>
              <div className="flex">
                <p>{pokemonData.type_1}</p>
                <p className="ml-3">{pokemonData.type_2}</p>
              </div>
            </div>
          </div>
        </div>
    </div>
  );
}