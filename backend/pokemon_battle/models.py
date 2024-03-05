from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validates, ValidationError, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field



#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow() #makes marshmallow object


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object

#think of these as admin (keeping track of what products are available to sell)
class User(db.Model, UserMixin): 
    #CREATE TABLE User, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30),  nullable=True)
    username = db.Column(db.String(30), nullable=True, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    pokemons = db.relationship('Pokemon', backref='user', lazy='dynamic')
    teams = db.relationship('Team', back_populates='user')

    
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #this is going to grab a timestamp as soon as a User object is instantiated


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    
class Pokemon(db.Model):
    poke_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    pokemon_id = db.Column(db.Integer, unique=True, nullable=False)
    pokemon_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))  # URL to the default sprite
    shiny_image_url = db.Column(db.String(255))  # URL to the shiny sprite
    base_experience = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    special_attack = db.Column(db.Integer)
    special_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    type = db.Column(db.String(50), nullable=False)
    abilities = db.Column(db.String(200))
    moves = db.relationship('Move', secondary='pokemon_moves', lazy='subquery',
                            backref=db.backref('pokemons', lazy=True))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    teams = db.relationship('TeamMember', back_populates='pokemon')


    def __repr__(self):
        return f"<Pokemon: {self.pokemon_name}>"

class Move(db.Model):
    move_id = db.Column(db.Integer, primary_key=True)
    move_name = db.Column(db.String(50), nullable=False)
    move_type = db.Column(db.String(50), nullable=False)  # Physical, Special, or Status
    power = db.Column(db.Integer)
    pp = db.Column(db.Integer)  # Power Points
    accuracy = db.Column(db.Integer)
    effect = db.Column(db.String(255))  # Description of the move's effect

    def __repr__(self):
        return f"<Move: {self.move_name} (Type: {self.move_type})>"

# This association table creates a many-to-many relationship between the Pokemon and Move models.
# It stores the connections between Pokemon and their moves, where each Pokemon can have multiple moves,
# and each move can be associated with multiple Pokemon.
pokemon_moves = db.Table('pokemon_moves',
    db.Column('pokemon_id', db.ForeignKey('pokemon.pokemon_id'), primary_key=True),
    db.Column('move_id', db.ForeignKey('move.move_id'), primary_key=True)
)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='teams')
    members = db.relationship('TeamMember', back_populates='team')


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    poke_id = db.Column(db.String(50), db.ForeignKey('pokemon.poke_id'), nullable=False)
    team = db.relationship('Team', back_populates='members')
    pokemon = db.relationship('Pokemon', back_populates='teams')

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # e.g., pending, ongoing, completed
    winner_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=True)
    loser_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=True)
    battle_started = db.Column(db.DateTime, default=datetime.utcnow)
    battle_ended = db.Column(db.DateTime, nullable=True)
    participants = db.relationship('User', secondary='battle_participants', backref='battles')

battle_participants = db.Table('battle_participants',
    db.Column('battle_id', db.Integer, db.ForeignKey('battle.id'), primary_key=True),
    db.Column('user_id', db.String, db.ForeignKey('user.user_id'), primary_key=True)
)

class BattleHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    battle_id = db.Column(db.Integer, db.ForeignKey('battle.id'), nullable=False)
    result = db.Column(db.String(50))  # win or loss

    user = db.relationship('User', backref='battle_history')
    battle = db.relationship('Battle', backref='battle_history')



class PokemonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon
        sqla_session = db.session
        load_instance = True
        include_fk = True
        include_relationships = True  # Include relationships in serialization

    # ... include other fields as auto_field ...

    # New fields to be included
    pokemon_id = auto_field(required=True)
    shiny_image_url = auto_field(required=False)
    base_experience = auto_field(required=False)
    hp = auto_field(required=False)
    attack = auto_field(required=False)
    defense = auto_field(required=False)
    special_attack = auto_field(required=False)
    special_defense = auto_field(required=False)
    speed = auto_field(required=False)

    # Updating the moves field to handle relationship serialization
    moves = fields.Nested('MoveSchema', many=True, only=['move_name', 'move_type', 'power', 'pp', 'accuracy', 'effect'])
    teams = fields.Nested('TeamMemberSchema', many=True, exclude=('pokemon',))

# Move schema for serialization
class MoveSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Move
        sqla_session = db.session
        load_instance = True

    # Fields for the Move model
    move_id = auto_field(required=True)
    move_name = auto_field(required=True)
    move_type = auto_field(required=True)
    power = auto_field(required=False)
    pp = auto_field(required=False)
    accuracy = auto_field(required=False)
    effect = auto_field(required=False)

class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        sqla_session = db.session
        load_instance = True
        include_fk = True

    # Fields to include
    id = auto_field()
    name = auto_field()
    user_id = auto_field()

    # Nested relationship for user
    user = fields.Nested('UserSchema', only=('user_id', 'username', 'email'))

    # Nested relationship for team members
    members = fields.Nested('TeamMemberSchema', many=True)

class TeamMemberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember
        sqla_session = db.session
        load_instance = True
        include_fk = True

    # Fields to include
    id = auto_field()
    team_id = auto_field()
    poke_id = auto_field()

    # Define the nested relationship for the team
    team = fields.Nested('TeamSchema', only=('id', 'name'))
    
    # Define the nested relationship for the pokemon
    pokemon = fields.Nested('PokemonSchema', only=('poke_id', 'pokemon_name', 'image_url', 'type'))

class BattleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Battle
        sqla_session = db.session
        load_instance = True
        include_fk = True
        include_relationships = True

    id = auto_field()
    status = auto_field()
    winner_id = auto_field()
    loser_id = auto_field()
    battle_started = auto_field()
    battle_ended = auto_field()
    participants = fields.Nested('UserSchema', many=True, only=('user_id', 'username'))

class BattleHistorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BattleHistory
        sqla_session = db.session
        load_instance = True
        include_fk = True

    id = auto_field()
    user_id = auto_field()
    battle_id = auto_field()
    result = auto_field()
    user = fields.Nested('UserSchema', only=('user_id', 'username'))
    battle = fields.Nested(BattleSchema, only=('id', 'status', 'winner_id', 'loser_id'))


# Instantiate schemas
move_schema = MoveSchema()
moves_schema = MoveSchema(many=True)
pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)
team_schema = TeamSchema()
teams_schema = TeamSchema(many=True) 
team_member_schema = TeamMemberSchema()
team_members_schema = TeamMemberSchema(many=True) 
battle_schema = BattleSchema()
battles_schema = BattleSchema(many=True)  
battle_history_schema = BattleHistorySchema()
battle_histories_schema = BattleHistorySchema(many=True)  
