import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

export default function Pokemon() {
    const [pokemonList, setpokemonList] = useState([{}])

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/get-all-pokemons')
        .then(response => {
            setpokemonList(response.data)
        })
    }, [])
    
    return (
        <div className="Pokemon">
          <header className="App-header">
            <div className=" border-2">
                <h1 className="flex-auto text-xl font-medium">Lista di Pokemon</h1>
            </div>
            <div>
                {
                    pokemonList.map( pokemon => {
                        return (
                            <div>
                                <Link className="flex-auto text-s"
                                    to={`/pokemons/${pokemon.id}`}
                                    key={pokemon.id}
                                >
                                    { pokemon.name }
                                </Link>
                                <br/>
                            </div>
                        )
                    })
                }
            </div>
          </header>
        </div>
      );
}