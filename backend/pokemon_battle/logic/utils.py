from backend.pokemon_battle.models import db, Pokemon, Move, Battle  # Import necessary models
import datetime

def get_pokemon_by_id(pokemon_id):
    """Fetch a Pokemon instance by its ID."""
    return Pokemon.query.get(pokemon_id)

def get_move_by_id(move_id):
    """Fetch a Move instance by its ID."""
    return Move.query.get(move_id)

def save_to_database(instance):
    """Add a new instance to the database and commit the session."""
    db.session.add(instance)
    db.session.commit()

def update_pokemon_status(pokemon_id, status):
    """Update the status effect of a Pokemon."""
    pokemon = get_pokemon_by_id(pokemon_id)
    if pokemon:
        pokemon.status = status
        db.session.commit()

def create_battle(pokemon1_id, pokemon2_id):
    """Create a new Battle instance."""
    battle = Battle(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, status='pending')
    save_to_database(battle)
    return battle

def end_battle(battle_id, winner_id, loser_id):
    """End a battle, updating its status and setting the winner and loser."""
    battle = Battle.query.get(battle_id)
    if battle:
        battle.status = 'completed'
        battle.winner_id = winner_id
        battle.loser_id = loser_id
        battle.end_time = datetime.utcnow() 
        db.session.commit()

def get_battle_by_id(battle_id):
    """Fetch a Battle instance by its ID."""
    return Battle.query.get(battle_id)


# Additional utility functions can be added here as needed
