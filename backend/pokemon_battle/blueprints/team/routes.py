import requests
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from ...models import db, Team, TeamMember, Pokemon, team_schema
from ..auth.routes import verify_token

# Blueprint for team management
team_bp = Blueprint('team', __name__)

team_bp.route('/team', methods=['POST'])
@verify_token
@login_required
def create_team():
    data = request.get_json()
    team_name = data.get('name')
    pokemon_ids = data.get('pokemon_ids', [])
    
    if not team_name:
        return jsonify({'error': 'Team name is required.'}), 400
    
    if len(pokemon_ids) > 6:
        return jsonify({'error': 'A team cannot have more than 6 Pokémon.'}), 400
    
    new_team = Team(name=team_name, user_id=current_user.id)
    db.session.add(new_team)
    db.session.flush()  # Flush to get the team id for the new team before committing

    for poke_id in pokemon_ids:
        pokemon = Pokemon.query.get(poke_id)
        if not pokemon:
            db.session.rollback()
            return jsonify({'error': f'Pokemon with id {poke_id} does not exist.'}), 400
        team_member = TeamMember(team_id=new_team.id, pokemon_id=poke_id)
        db.session.add(team_member)
    
    db.session.commit()
    return jsonify({'message': 'Team created successfully', 'team_id': new_team.id}), 201

@team_bp.route('/pokemon/pool/add', methods=['POST'])
@verify_token
@login_required
def add_pokemon_to_pool():
    data = request.get_json()
    new_pokemon = Pokemon(
        pokemon_id=data['pokemon_id'],
        pokemon_name=data['pokemon_name'],
        type=data['type'],
        user_id=current_user.user_id
    )
    db.session.add(new_pokemon)
    db.session.commit()
    return jsonify({'message': 'Pokémon added to your pool successfully'}), 201



@team_bp.route('/team/<int:team_id>/add', methods=['POST'])
@verify_token
@login_required
def add_pokemon_to_team(team_id):
    data = request.get_json()
    pokemon_id = data.get('pokemon_id')
    
    team = Team.query.get(team_id)
    if team.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if len(team.pokemons) >= 6:
        return jsonify({'error': 'Team is already at maximum capacity.'}), 400
    
    # Assume pokemon_id is validated to exist
    team_member = TeamMember(team_id=team_id, pokemon_id=pokemon_id)
    db.session.add(team_member)
    db.session.commit()
    
    return jsonify({'message': 'Pokémon added to the team successfully.'}), 201

@team_bp.route('/team/<int:team_id>', methods=['GET'])
@verify_token
@login_required
def get_team(team_id):
    team = Team.query.get(team_id)
    if team.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Serialize team and its Pokémon members to JSON
    team_info = team_schema.dump(team)
    return jsonify(team_info), 200


@team_bp.route('/team/<int:team_id>', methods=['PUT'])
@verify_token
@login_required
def update_team(team_id):
    data = request.get_json()
    pokemon_ids = data.get('pokemon_ids', [])
    if len(pokemon_ids) > 6:
        return jsonify({'error': 'A team cannot have more than 6 Pokémon.'}), 400
    TeamMember.query.filter_by(team_id=team_id).delete()
    for poke_id in pokemon_ids:
        db.session.add(TeamMember(team_id=team_id, poke_id=poke_id))
    db.session.commit()
    return jsonify({'message': 'Team updated successfully.'}), 200

@team_bp.route('/team/<int:team_id>/pokemon/<poke_id>/remove', methods=['DELETE'])
@verify_token
@login_required
def remove_pokemon_from_team(team_id, poke_id):
    team_member = TeamMember.query.filter_by(team_id=team_id, poke_id=poke_id).first()
    if team_member:
        db.session.delete(team_member)
        db.session.commit()
        return jsonify({'message': 'Pokémon removed from team successfully'}), 200
    return jsonify({'error': 'Pokémon not found in team'}), 404



