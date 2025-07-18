import uuid
from datetime import datetime
import re
from app.models.baseclass import BaseModel
from sqlalchemy.orm import relationship
from app import bcrypt, db

class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    _is_admin = db.Column('is_admin', db.Boolean, default=False)

    # Relationships
    places_r = relationship("Place", back_populates="owner_r", cascade="all, delete-orphan")
    reviews_r = relationship("Review", back_populates="user_r", cascade="all, delete-orphan")

    def hash_password(self, password):
        """Hash the password before storing it."""
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    """
    FIRST NAME
    """
    @property
    def first_name(self):
        """First name Getter"""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """First name Setter, raises a ValueError if first name is more than 50 characters or less than 2 characters"""
        value = value.strip()
        if len(value) <= 50 and len(value) >= 2:
            self._first_name = value
        else:
            raise ValueError("First name must be between 2-50 characters.")

    """
    LAST NAME
    """
    @property
    def last_name(self):
        """Last name Getter"""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Last name Setter, raises a ValueError if last name is more than 50 characters or less than 2 characters"""
        value = value.strip()
        if len(value) <= 50 and len(value) >= 2:
            self._last_name = value
        else:
            raise ValueError("Last name must be between 2-50 characters")

    """
    EMAIL
    """
    @property
    def email(self):
        """Email Getter"""
        return self._email

    @email.setter
    def email(self, value):
        """Email Setter, raises ValueError if invalid email address"""
        value = value.strip()
        if self._is_email_valid(value):
            self._email = value
        else:
            raise ValueError("Invalid email address.")

    def _is_email_valid(self, email):
        """Email validation function using Regex to validate email"""
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

    """
    IS ADMIN
    """
    @property
    def is_admin(self):
        """Admin Getter"""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Admin Setter and return a boolean"""
        self._is_admin = bool(value)

    """
    PASSWORD
    """
    @property
    def password(self):
        """Password is write-only"""
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, value):
        """Password Setter - stores the hashed password directly"""
        if value:
            self._password = value

    """
    SAVE
    """
    def save(self):
        """Function to save created_at time"""
        self.updated_at = datetime.now()

    """
    UPDATE
    """
    def update(self, data):
        """Update user fields and commit to the database"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        

