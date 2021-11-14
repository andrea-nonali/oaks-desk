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
      <header className="App-header">
        <div>
          <h1>Pokemon</h1>
        </div>
        <div>
            {
              pokemonData.name
            }
        </div>
      </header>
    </div>
  );
}