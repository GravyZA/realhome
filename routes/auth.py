import os
from werkzeug.utils import secure_filename
from extensions import db
from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from models import AgentProfile, User, Property
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Ensures user.id is available before commit

        # Auto-create blank agent profile if registering as an Estate Agent
        if role == "Estate Agent":
            profile = AgentProfile(agent_id=user.id)
            db.session.add(profile)

        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            session['user_name'] = user.name
            return redirect(url_for('properties.dashboard'))
        flash('Invalid login credentials.')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('properties.index'))

@auth_bp.route('/agent/dashboard')
def agent_dashboard():
    agent_id = session.get('user_id')
    if not agent_id or session.get("user_role") != "Estate Agent":
        flash("Unauthorized access.")
        return redirect(url_for("auth.login"))

    agent = User.query.get(agent_id)
    profile = agent.agent_profile
    listings = Property.query.filter_by(agent_id=agent_id).all()
    return render_template("agent/dashboard.html", agent=agent, profile=profile, listings=listings)


@auth_bp.route('/agent/update-profile', methods=['POST'])
def update_profile():
    agent_id = session.get('user_id')
    if not agent_id:
        flash("Login required.")
        return redirect(url_for("auth.login"))

    agent = User.query.get(agent_id)
    profile = agent.agent_profile

    # Check for duplicate email
    new_email = request.form['email']
    existing = User.query.filter(User.email == new_email, User.id != agent_id).first()
    if existing:
        flash("Email already in use.")
        return redirect(url_for("auth.agent_dashboard"))

    # Update user fields
    agent.name = request.form['name']
    agent.email = new_email
    agent.phone = request.form.get('phone')

    # Update agent profile fields
    profile.agency_name = request.form.get('agency_name')
    profile.license_number = request.form.get('license_number')
    profile.phone = request.form.get('phone')
    profile.website = request.form.get('website')
    profile.facebook = request.form.get('facebook')
    profile.linkedin = request.form.get('linkedin')
    profile.twitter = request.form.get('twitter')

    # Handle profile image upload
    file = request.files.get('profile_image')
    if file and file.filename:
        filename = secure_filename(file.filename)
        folder = os.path.join('static', 'assets', 'agents', str(agent_id))
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        file.save(file_path)
        profile.profile_image = f"assets/agents/{agent_id}/{filename}"

    db.session.commit()
    flash("Profile updated successfully!")
    return redirect(url_for("auth.agent_dashboard"))
