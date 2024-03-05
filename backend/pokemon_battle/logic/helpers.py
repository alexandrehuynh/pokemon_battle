from backend.pokemon_battle.models import Battle, Pokemon, Move  # Ensure you import your database models correctly
import random


def apply_status_effects(pokemon):
    # Assuming 'status_effects' dictionary contains all possible effects and their impacts
    if pokemon.status == 'burn' or pokemon.status == 'poisoned':
        pokemon.hp -= 10  # These reduce HP; adjust as necessary.
    elif pokemon.status == 'paralyzed':
        if random.random() < 0.25:  # 25% chance to not move
            return False  # Pokémon cannot make a move this turn
    elif pokemon.status == 'sleep':
        if pokemon.sleep_turns > 0:
            pokemon.sleep_turns -= 1  # Counting down the turns of sleep
            return False  # Pokémon cannot make a move this turn
    elif pokemon.status == 'frozen':
        if random.random() < 0.2:  # 20% chance to thaw out
            pokemon.status = None  # Pokémon thaws and can move again
            return True
        else:
            return False  # Pokémon cannot make a move this turn
    # More status effects can be added here following the pattern.
    return True  # Default case where Pokémon can make a move

def get_type_effectiveness(attack_type, defender_type):
    # Simplified; real games have a complex type chart
    effectiveness_chart = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fighting": 2, "Poison": 0.5, "Steel": 0.5, "Fire": 0.5, "Dragon": 2, "Dark": 2}
}

    return effectiveness_chart.get((attack_type, defender_type), 1)  # Default to 1 for neutral effectiveness

def check_and_update_faint(pokemon):
    """
    Check if a Pokémon's HP has dropped to 0 or below and update its status to 'fainted' if so.
    
    Parameters:
    pokemon (Pokemon): The Pokémon instance to check.
    
    Returns:
    bool: True if the Pokémon has fainted, False otherwise.
    """
    if pokemon.hp <= 0:
        pokemon.hp = 0  # Ensure HP doesn't go below 0
        pokemon.status = 'fainted'  # Update status to indicate the Pokémon has fainted
        return True
    return False
