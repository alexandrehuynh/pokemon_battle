from backend.pokemon_battle.models import Battle, Pokemon, Move  # Ensure you import your database models correctly
from sqlalchemy.orm import joinedload
import random
from .utils import get_battle_by_id, get_move_by_id, get_pokemon_by_id, save_to_database
from .helpers import get_type_effectiveness, apply_status_effects, check_and_update_faint

def start_battle(pokemon1_id, pokemon2_id):
    pokemon1 = get_pokemon_by_id(pokemon1_id)
    pokemon2 = get_pokemon_by_id(pokemon2_id)
    battle = Battle(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, status='pending')
    # Further logic to set up initial battle conditions goes here
    save_to_database(battle)
    return battle


def calculate_damage(attack_move, attacker, defender):
    # Calculate type effectiveness
    type_effectiveness = get_type_effectiveness(attack_move.type, defender.type)

    # Check for STAB
    stab = 1.5 if attack_move.type in attacker.types else 1

    # Determine if the move hits critically
    critical = 2 if random.random() < 0.1 else 1  # Assuming a 10% chance for critical hits

    # Random variation between 0.85 and 1.0
    variation = random.uniform(0.85, 1.0)

    # Basic damage formula
    damage = (((2 * attacker.level / 5 + 2) * attack_move.power * (attacker.attack / defender.defense) / 50) + 2) * stab * type_effectiveness * critical * variation

    return max(1, int(damage))  # Ensure damage is at least 1

def determine_turn_order(pokemon1, pokemon2):
    # Initially sort by speed to determine the natural order
    ordered_pokemon = sorted([pokemon1, pokemon2], key=lambda p: p.speed, reverse=True)
    
    # Adjust for status effects that might alter turn order
    # Example: Paralysis reduces speed by 50% for this calculation
    for pokemon in ordered_pokemon:
        if pokemon.status == 'paralyzed':
            pokemon.speed *= 0.5
    
    # Reorder after adjusting for status effects
    ordered_pokemon = sorted(ordered_pokemon, key=lambda p: p.speed, reverse=True)
    
    # Reset speed changes for fairness in subsequent turns
    for pokemon in ordered_pokemon:
        if pokemon.status == 'paralyzed':
            pokemon.speed /= 0.5
    
    return ordered_pokemon

def update_battle_state(battle_id, attacker_id, defender_id, move_id):
    # Fetch battle, attacker, defender, and move details
    battle = get_battle_by_id(battle_id)
    attacker = get_pokemon_by_id(attacker_id)
    defender = get_pokemon_by_id(defender_id)
    selected_move = get_move_by_id(move_id)

    # Apply pre-move status checks for the attacker
    if not apply_status_effects(attacker):
        return {"message": "Attacker is unable to move due to status effects"}

    # Calculate damage
    damage = calculate_damage(selected_move, attacker, defender)
    
    # Apply damage to the defender
    defender.hp -= damage
    check_and_update_faint(defender)

    # Update the battle state, proceed to next turn or conclude the battle
    update_battle_progress(battle, attacker, defender)

    # Additional logic for handling turns, status updates, and battle conclusion
    # Save changes to the database
    save_to_database(battle)
    save_to_database(attacker)
    save_to_database(defender)

    return {"message": "Move executed", "damage": damage, "defender_new_hp": defender.hp}


def check_battle_outcome(battle_id):
    # Check if the battle has concluded (one team is out of usable Pokémon)
    # Update the battle status to completed and record the winner and loser
    pass

# Additional helper functions as needed for type effectiveness, status effects, etc.
def update_battle_progress(battle_id, attacker_id, defender_id, move_id):
    # This function would manage the battle's state transitions,
    # Turn progression and battle conclusion based on the Pokémon's statuses.
    pass