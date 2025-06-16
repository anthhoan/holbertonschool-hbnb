import uuid
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, is_admin):
        if first_name is None or last_name is None or email is None:
            raise ValueError("Required attributes not specified!")
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def first_name(self):
        return self.first_name

    @first_name.setter
    def first_name(self, value):
        if len(self.value) < 50:
            self.first_name = value
        else:
            raise ValueError("First name cannot exceed 50 characters.")

    @property
    def last_name(self):
        return self.last_name

    @last_name.getter
    def last_name(self, value):
        if len(self.value) < 50:
            self.last_name = value
        else:
            raise ValueError("Last name cannot exceed 50 characters.")

    @property
    def email(self):
        return self.email

    @email.getter
    def email(self, value):
        if str(value)

    def is_admin(self):
        pass

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()