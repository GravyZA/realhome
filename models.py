from extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    price = db.Column(db.Float) 
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    type = db.Column(db.String(50))
    location = db.Column(db.String(120))
    image = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to agent
    agent = relationship("User", backref="listings")
    additional_images = db.relationship(
        'ListingImage',
        backref='listing',
        cascade="all, delete-orphan"
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class AgentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    agency_name = db.Column(db.String(120))
    license_number = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))  # Path to profile picture
    website = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    twitter = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('agent_profile', uselist=False))

class ListingImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('property.id'))

    user = db.relationship("User", backref="wishlist_items")
    listing = db.relationship("Property", backref="wishlisted_by")
