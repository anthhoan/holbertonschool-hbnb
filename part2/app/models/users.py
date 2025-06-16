import uuid
from datetime import datetime
import re

class User:
    def __init__(self, first_name, last_name, email, is_admin=False):
        self.id = str(uuid.uuid4())
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

#Getters and Setters
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        value = value.strip()
        if len(value) <= 50:
            self._first_name = value
        else:
            raise ValueError("First name cannot exceed 50 characters.")

    @property
    def last_name(self):
        return self._last_name

    @last_name.getter
    def last_name(self, value):
        value = value.strip()
        if len(value) <= 50:
            self._last_name = value
        else:
            raise ValueError("Last name cannot exceed 50 characters.")

    @property
    def email(self):
        return self._email

    @email.getter
    def email(self, value):
        value = value.strip()


# Methods
    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()