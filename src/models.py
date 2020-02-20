from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import json
from datetime import datetime

db = SQLAlchemy()

class Gender(Enum):
    WOMAN = "woman"
    MAN = "man"
    OTHER = "other"

class Arms(Enum):
    SHORT = "short"
    AVERAGE = "average"
    LONGY = "long"

class Shoulders(Enum):
    NARROW = 'narrow'
    AVERAGE = 'average'
    WIDE = 'wide'

class Torso(Enum):
    SHORT = 'short'
    AVERAGE = 'average'
    LONGY = 'long'

class Hips(Enum):
    NARROW = 'narrow'
    AVERAGE = 'average'
    WIDE = 'wide'

class Legs(Enum):
    SHORT = 'short'
    AVERAGE = 'average'
    LONGY = 'long'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genderuser = db.Column(db.Enum(Gender), nullable=False)
    # look = db.Column(db.Enum(Lookchoice), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    mobilenumber = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(280), nullable=False)
    socialmedia = db.Column(db.String(280))
    sizetop = db.Column(db.String(280), nullable=False)
    sizebottom = db.Column(db.String(280), nullable=False)
    sizeshoes = db.Column(db.String(280), nullable=False)
    igaccount = db.Column(db.String(140), nullable=True)
    height = db.Column(db.Integer, nullable=False)
    waist = db.Column(db.Integer, nullable=False)
    armsuser = db.Column(db.Enum(Arms), nullable=False)
    shouldersuser = db.Column(db.Enum(Shoulders), nullable=False)
    torsouser = db.Column(db.Enum(Torso), nullable=False)
    hipsuser = db.Column(db.Enum(Hips), nullable=False)
    legsuser = db.Column(db.Enum(Legs), nullable=False)
    thebudget = db.relationship("Budget", back_populates="user", uselist=False)
    thechildren = db.relationship("Children", back_populates="user")

    def __init__(self, new_user_data):
        self.genderuser = new_user_data["genderuser"]
        self.datecreated = datetime.strptime(new_user_data["datecreated"], "%Y/%m/%d")
        self.username = new_user_data["username"]
        self.email = new_user_data["email"]
        self.birthdate = datetime.strptime(new_user_data["birthdate"], "%Y/%m/%d")
        self.name = new_user_data["name"]
        self.lastname = new_user_data["lastname"]
        self.mobilenumber = new_user_data["mobilenumber"]
        self.address = new_user_data["address"]
        self.socialmedia = new_user_data["socialmedia"]
        self.sizetop = new_user_data["sizetop"]
        self.sizebottom = new_user_data["sizebottom"]
        self.sizeshoes = new_user_data["sizeshoes"]
        self.igaccount = new_user_data["igaccount"]
        self.height = int(new_user_data["height"])
        self.waist = int(new_user_data["waist"])
        self.armsuser = new_user_data["armsuser"]
        self.shouldersuser = new_user_data["shouldersuser"]
        self.torsouser = new_user_data["torsouser"]
        self.hipsuser = new_user_data["hipsuser"]
        self.legsuser = new_user_data["legsuser"]
        # self.thebudget = new_user_data["thebudget"]
        # self.thechildren = new_user_data["thechildren"]
        
    def serialize(self):

        return {
            "id": self.id,
            "genderuser": self.genderuser,
            "datecreated": self.datecreated,
            "username": self.username,
            "email": self.email,
            "age": datetime.today() - self.birthdate,
            "name": self.name,
            "lastname": self.lastname,
            "mobilenumber": self.mobilenumber,
            "address": self.address,
            "socialmedia": self.socialmedia,
            "sizetop": self.sizetop,
            "sizebottom": self.sizebottom,
            "sizeshoes": self.sizeshoes,
            "igaccount": self.igaccount,
            "height": self.height,
            "waist": self.waist,
            "armsuser": self.armsuser,
            "shouldersuser": self.shouldersuser,
            "torsouser": self.torsouser,
            "hipsuser": self.hipsuser,
            "legsuser": self.legsuser,
            "budget": [budget.serialize() for budget in self.thebudget],
            "children": [children.serialize() for children in self.thechildren]
            }

    def update(self, new_user_data):
        """ actualiza la informacion del usuario """
        self.email = new_user_data["email"]
        self.mobilenumber = new_user_data["mobilenumber"]
        self.address = new_user_data["address"]
        self.socialmedia = new_user_data["socialmedia"]
        self.sizetop = new_user_data["sizetop"]
        self.sizebottom = new_user_data["sizebottom"]
        self.sizeshoes = new_user_data["sizeshoes"]
        self.igaccount = new_user_data["igaccount"]
        self.waist = new_user_data["waist"]
        self.hipsuser = new_user_data["hipsuser"]
        self.budgettop = new_user_data["budgettop"]
        self.budgetbottom = new_user_data["budgetbottom"]
        self.budgetshoes = new_user_data["budgetshoes"]
        self.budgetbag = new_user_data["budgetbag"]
        self.budgetaccesories = new_user_data["budgetaccesories"]


class Lookchoice(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    look_url = db.Column(db.String(400), nullable=False)
    lookorder = db.Column(db.Integer, nullable=False)

class Dislikes(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

class Occasions(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

class Jeans(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    jeanschoiceurl = db.Column(db.String(400), nullable=False)

class Fittop(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    fittoporder = db.Column(db.Integer, nullable=False)

class Fitbottom(db.Model):
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    fitbottomorder = db.Column(db.Integer, nullable=False)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budgettop = db.Column(db.Integer, nullable=True)
    budgetbottom = db.Column(db.Integer, nullable=True)
    budgetshoes = db.Column(db.Integer, nullable=True)
    budgetsportshoes = db.Column(db.Integer, nullable=True)
    budgetbag = db.Column(db.Integer, nullable=True)
    budgetaccesories = db.Column(db.Integer, nullable=True)
    user = db.relationship("User", back_populates="thebudget")
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, new_user_data, user_id):
        self.budgettop = new_user_data["budgettop"]
        self.budgetbottom = new_user_data["budgetbottom"]
        self.budgetshoes = new_user_data["budgetshoes"]
        self.budgetbag = new_user_data["budgetbag"]
        self.budgetaccesories = new_user_data["budgetaccesories"]
        self.user_userid = user_id

class Children(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.DateTime, nullable=False)
    genderuser = db.Column(db.Enum(Gender), nullable=False)
    user = db.relationship("User", back_populates="thechildren")
    user_userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, children_data, user_id):
        self.birthdate = datetime.strptime(children_data["birthdate"], "%Y/%m/%d")
        self.genderuser = children_data["genderuser"]
        self.user_userid = user_id

