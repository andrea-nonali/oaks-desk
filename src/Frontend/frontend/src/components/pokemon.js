import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
                <h1 className="flex-auto text-xl font-bold">Lista di Pokemon</h1>
            </div>
            <div>
                {
                    pokemonList.map((pokemon) => {
                        return (
                            <div>
                                <p>{pokemon.name}</p>
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