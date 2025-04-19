import shutil
import os
from flask import Flask
from config import Config
from models import AgentProfile, Property, User
from extensions import db

def seed_users():
    if not User.query.filter_by(email="user@example.com").first():
        user = User(name="Normal User", email="user@example.com", role="User")
        user.set_password("Password1!")
        db.session.add(user)

    if not User.query.filter_by(email="agent@example.com").first():
        agent = User(name="Estate Agent", email="agent@example.com", role="Estate Agent")
        agent.set_password("Password1!")
        db.session.add(agent)
        db.session.flush()

        profile = AgentProfile(agent_id=agent.id, agency_name="Property Pros", phone="012 345 6789")
        db.session.add(profile)

    existing_listing = Property.query.filter_by(title="Modern Family Home").first()
    if not existing_listing:
        listing = Property(
            title="Modern Family Home",
            description="A beautiful and modern 3-bedroom family home located in the suburbs of Cape Town.",
            price=2500000.00,
            beds=3,
            baths=2,
            latitude= -33.9249,
            longitude= 18.4241,  # Cape Town 💙
            location="Cape Town",
            type="House",
            agent_id=agent.id,
            image=""  # to be set after file copy
        )
        db.session.add(listing)
        db.session.flush()  # populate listing.id

        # Copy main image
        dest_folder = os.path.join("static", "assets", str(listing.id))
        os.makedirs(dest_folder, exist_ok=True)
        main_src = os.path.join("static", "assets", "seed", "main.jpg")
        main_dst = os.path.join(dest_folder, "main.jpg")
        shutil.copyfile(main_src, main_dst)
        listing.image = f"assets/{listing.id}/main.jpg"

        # Copy additional images
        additional_src = os.path.join("static", "assets", "seed", "additional")
        additional_dest = os.path.join(dest_folder, "additional")
        os.makedirs(additional_dest, exist_ok=True)

        from models import ListingImage
        for filename in os.listdir(additional_src):
            src_file = os.path.join(additional_src, filename)
            dst_file = os.path.join(additional_dest, filename)
            shutil.copyfile(src_file, dst_file)
            db.session.add(ListingImage(filename=filename, listing_id=listing.id))

        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes.properties import properties_bp
    from routes.auth import auth_bp
    app.register_blueprint(properties_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        seed_users()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)