import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Change this to your actual backend API URL

// Add a Pokemon to a user's pool
export const addPokemonToPool = async (pokemonData: { pokemon_id: string; pokemon_name: string; type: string }) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/pokemon/pool/add`, pokemonData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`, // Assuming you store your token in localStorage
      },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to add Pokémon to pool', error);
    throw error;
  }
};

// Similarly, define other operations here...
