import requests
from flask import Blueprint, jsonify

# Define the blueprint
pokedex_bp = Blueprint('pokedex', __name__)

@pokedex_bp.route('/pokedex', methods=['GET'])
def get_pokemon_list():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
    if response.status_code == 200:
        pokemon_list = response.json()['results']
        return jsonify(pokemon_list)
    else:
        return jsonify({'error': 'Failed to fetch Pokémon list'}), response.status_code

@pokedex_bp.route('/pokedex/<string:pokemon_name>', methods=['GET'])
def get_pokemon_details(pokemon_name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if response.status_code == 200:
        pokemon_details = response.json()
        return jsonify(pokemon_details)
    else:
        return jsonify({'error': f'Failed to fetch details for Pokémon {pokemon_name}'}), response.status_code
