import os
from flask import (
    Blueprint, jsonify, request, redirect, flash,
    session, url_for, render_template
)
from werkzeug.utils import secure_filename

from models import Property, ListingImage
from extensions import db
from routes.decorators import estate_agent_required, login_required
from utils.location_helper import get_coordinates


properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/')
def index():
    all_properties = Property.query.filter(
        Property.latitude.isnot(None),
        Property.longitude.isnot(None)
    ).all()

    # Convert to serializable dicts
    listings_with_coords = [
        {
            "id": p.id,
            "title": p.title,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "location": p.location,
            "price": p.price,
            "type": p.type
        }
        for p in all_properties
    ]

    return render_template('index.html', listings=listings_with_coords, title="Welcome")

@properties_bp.route('/login')
def login():
    return render_template('login.html', title='Login')

from models import Property, Wishlist

@properties_bp.route('/dashboard')
def dashboard():
    user_id = session.get("user_id")
    query = Property.query

    # Search filters
    location = request.args.get('location')
    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))

    property_type = request.args.get('type')
    if property_type:
        query = query.filter(Property.type == property_type)

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)

    properties = query.all()

    # Get all wishlist listing IDs for this user
    liked_ids = []
    if user_id:
        liked_ids = [
            w.listing_id for w in Wishlist.query.filter_by(user_id=user_id).all()
        ]

    return render_template(
        'dashboard.html',
        properties=properties,
        liked_ids=liked_ids,
        title="Listings"
    )

@properties_bp.route('/detail/<int:listing_id>')
def detail(listing_id):
    listing = Property.query.get_or_404(listing_id)
    return render_template('properties/detail.html', title=listing.title, listing=listing)

@properties_bp.route('/add-listing', methods=['GET', 'POST'])
@estate_agent_required
def add_listing():
    if request.method == 'POST':
        # 1. Grab form data
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        beds = int(request.form['beds'])
        baths = int(request.form['baths'])
        location = request.form['location']
        type = request.form['type']

        latitude, longitude = get_coordinates(location)
        
        # 2. Create Property entry in DB (before saving image paths)
        listing = Property(
            title=title,
            description=description,
            price=price,
            beds=beds,
            baths=baths,
            location=location,
            type=type,
            latitude=latitude,
            longitude=longitude,
            image='',
            agent_id=session.get("user_id")  # <- BOOM: Link listing to logged-in user
        )
        db.session.add(listing)
        db.session.commit()

        # 3. Generate folder path
        listing_folder = os.path.join("static", "assets", str(listing.id))
        additional_folder = os.path.join(listing_folder, "additional")
        os.makedirs(additional_folder, exist_ok=True)

        # 4. Save main image
        main_image = request.files['main_image']
        if main_image:
            filename = "main.jpg"
            main_path = os.path.join(listing_folder, filename)
            main_image.save(main_path)

            # Update listing.image field
            listing.image = f"assets/{listing.id}/{filename}"
            db.session.commit()

        # 5. Save additional images (optional)
        additional_images = request.files.getlist('additional_images')
        for file in additional_images:
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(additional_folder, filename)
                file.save(save_path)

                image_record = ListingImage(filename=filename, listing_id=listing.id)
                db.session.add(image_record)

        db.session.commit()
        flash("Listing and images saved successfully!")
        return redirect(url_for('properties.dashboard'))

    return render_template('add_listing.html', title='Add Listing')

@properties_bp.route('/edit-listing/<int:listing_id>', methods=['GET', 'POST'])
@estate_agent_required
def edit_listing(listing_id):
    listing = Property.query.get_or_404(listing_id)

    # Only the agent who owns the listing can edit
    if listing.agent_id != session.get('user_id'):
        flash("Unauthorized.")
        return redirect(url_for('auth.agent_dashboard'))

    if request.method == 'POST':
        listing.title = request.form['title']
        listing.description = request.form['description']
        listing.price = request.form['price']
        listing.beds = int(request.form['beds'])
        listing.baths = int(request.form['baths'])
        listing.location = request.form['location']
        listing.type = request.form['type']
        db.session.commit()
        flash("Listing updated.")
        return redirect(url_for('auth.agent_dashboard'))

    return render_template('edit_listing.html', title="Edit Listing", listing=listing)


@properties_bp.route('/delete-listing/<int:listing_id>', methods=['POST'])
@estate_agent_required
def delete_listing(listing_id):
    listing = Property.query.get_or_404(listing_id)

    if listing.agent_id != session.get('user_id'):
        flash("Unauthorized.")
        return redirect(url_for('auth.agent_dashboard'))

    # Optionally: delete associated images
    listing_folder = os.path.join("static", "assets", str(listing.id))
    if os.path.exists(listing_folder):
        import shutil
        shutil.rmtree(listing_folder)

    db.session.delete(listing)
    db.session.commit()
    flash("Listing deleted.")
    return redirect(url_for('auth.agent_dashboard'))

@properties_bp.route('/toggle-wishlist/<int:listing_id>', methods=['POST'])
def toggle_wishlist(listing_id):
    print("User ID in session:", session.get('user_id'))
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    existing = Wishlist.query.filter_by(user_id=user_id, listing_id=listing_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'liked': False})  # Removed from wishlist
    else:
        new_entry = Wishlist(user_id=user_id, listing_id=listing_id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'liked': True})  # Added to wishlist