# 🏠 RealHome

A modern real estate listing web application built with Flask, SQLAlchemy, Bootstrap 5, and Leaflet.js.  
Developed as part of a **Work Integrated Learning (WIL)** module, this project demonstrates both full-stack development practices and real-world application architecture.

---

## 📸 Project Overview

RealHome allows users to:

- 🏘️ Browse properties by location, type, and price  
- 💬 View property details with an image gallery and map  
- ❤️ Save listings to their wishlist (auth required)  
- 🧑‍💼 Agents can manage listings (create, edit, delete)  
- 🌍 View all listings on an interactive map  
- 🔐 Secure login and registration system  

---

## 🧠 Tech Stack

| Layer       | Technology               |
|-------------|---------------------------|
| Frontend    | HTML, Bootstrap 5         |
| Backend     | Python (Flask), Jinja2    |
| Database    | SQLite (via SQLAlchemy)   |
| Mapping     | Leaflet.js + OpenStreetMap|
| Auth        | Flask-Login               |
| Forms       | Flask-WTF + WTForms       |

---

## ⚙️ Features Breakdown

### 💼 General User
- Browse and search property listings
- Use filters: **Location**, **Price Range**, **Property Type**
- Save listings to Wishlist (persisted by user ID)
- View individual listings with:
  - Image carousel
  - Interactive map
  - Agent contact details

### 🧑‍💼 Estate Agent
- Create, edit, delete property listings
- Upload main and multiple additional images
- Geolocation lookup from string-based location
- Agent-only sidebar dashboard

### 📍 Mapping
- Leaflet.js map on index with **clustered pins**
- Color-coded markers by property type
- Clickable pins with preview tooltips and popups
- Automatic zoom to bounds of active markers

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/GravyZA/realhome.git
cd realhome
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
flask run
```
ℹ️ Ensure your .env file is set up correctly for environment variables like FLASK_APP and FLASK_ENV.

---

## 📓 WIL Requirements Alignment
| Requirement                        | Status            |
|-----------------------------------|-------------------|
| User registration & login         | ✅ Complete        |
| Agent dashboard to manage listings| ✅ Complete        |
| Listings CRUD                     | ✅ Complete        |
| Image uploads (main + additional) | ✅ Complete        |
| Detail page with carousel & map   | ✅ Complete        |
| Property search & filtering       | ✅ Complete        |
| Interactive map with marker clusters | ✅ Complete     |
| Wishlist (Favorites) system       | ✅ Complete        |
| Custom styling and branding       | ✅ Complete        |
| README + Documentation            | ✅ You’re reading it! |

---

## 🎯 Future Improvements
- ✅ Marker clustering (done!)
- 🔄 Live search + map sync
- ✨ Notifications for more actions
- 📈 Admin dashboard / analytics
- 🧪 Unit tests and test coverage

---

## 🧑‍🎓 Author
Damian De Vos
Built as part of a WIL module — 2025
