# Hardely's Travelogue

Hardely's Travelogue is a comprehensive Django-based platform designed for travel enthusiasts, riding clubs, and specialized shops. It provides a centralized hub for managing trips, gear rentals, and community interactions.

## 🚀 Features

### For Riders (Users)
- **Personalized Profiles**: Manage bio, personal details, and travel history.
- **Club Memberships**: Join various riding clubs and stay updated.
- **Event Participation**: Browse, sign up, and track upcoming travel events/rides.
- **E-commerce**: Purchase travel gear from specialized shops.
- **Rental System**: Rent equipment for specific durations with automated tracking.
- **Feedback**: Provide feedback on events and services.

### For Riding Clubs
- **Event Management**: Create and organize rides, specifying routes, destinations, and estimated costs.
- **Articles & Posts**: Share experiences and travelogues with the community.
- **Member Management**: Track member requests and participation.
- **Rental Services**: Offer equipment for rent to club members.

### For Shops
- **Product Listing**: Sell travel-related products with stock management.
- **Order Tracking**: Manage customer orders and delivery status.

## 🛠️ Tech Stack
- **Framework**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Auth**: Custom user authentication (AbstractUser)

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VishnuSuresh0204/Hardely-s-Travelogue.git
   cd Hardely-s-Travelogue
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. **Install dependencies** (if applicable):
   ```bash
   pip install django
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---
*Created with ❤️ for the travel and riding community.*
