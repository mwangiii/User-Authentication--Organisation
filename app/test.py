# run.py

from app import app, db  # Import the Flask app and SQLAlchemy instance
from app.models import User

# Ensure app context is pushed
with app.app_context():
    # Create any necessary database tables
    db.create_all()

    # Example usage to add a new user record
    new_user = User(userid="10000", firstname='Kwanza', lastname='Pili', email='kwanzapilipili@example.com', password='password', phone='1234567890')

    # Add the new user to the session
    db.session.add(new_user)

    # Commit the session to persist changes to the database
    db.session.commit()

    print("User added successfully!")
