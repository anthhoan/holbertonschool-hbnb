import uuid
from datetime import datetime
import re

class User:
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.password = password

    # First Name
    @property
    def first_name(self):
        """First name Getter"""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """First name Setter, raises a ValueError if first name is more than 50 characters"""
        value = value.strip()
        if len(value) <= 50:
            self._first_name = value
        else:
            raise ValueError("First name cannot exceed 50 characters.")

    # Last Name
    @property
    def last_name(self):
        """Last name Getter"""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Last name Setter, raises a ValueError if last name is more than 50 characters"""
        value = value.strip()
        if len(value) <= 50:
            self._last_name = value
        else:
            raise ValueError("Last name cannot exceed 50 characters.")

    # Email
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

    # Is Admin
    @property
    def is_admin(self):
        """Admin Getter"""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Admin Setter and return a boolean"""
        self._is_admin = bool(value)

    # Methods
    def save(self):
        """Function to save created_at time"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Function to save updated_at time"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
