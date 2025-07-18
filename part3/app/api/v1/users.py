from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the user update model (only first_name and last_name can be updated)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})

@api.route('/')
class UserList(Resource):

    @api.response(200, 'List of users')
    def get(self):
        """Get all users"""
        users = facade.user_repo.get_all()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        
        print(">>> POST /users route triggered")  # Add this line first
    

        user_data = api.payload

        # Check if email already exists
        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
        except Exception:
            # If there's an error checking email, continue (might be first user)
            pass

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print("CREATE USER ERROR:", e)
            # Catch database integrity errors and other exceptions
            error_msg = str(e)
            if 'UNIQUE constraint failed' in error_msg or 'already registered' in error_msg:
                return {'error': 'Email already registered'}, 400
            return {'error': 'An error occurred while creating the user'}, 500

@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print("UPDATE USER ERROR:", e)  # This helps you debug in the terminal
            return {'error': 'An error occurred while updating the user'}, 500

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        try:
            success = facade.delete_user(user_id)
            if not success:
                return {'error': 'User not found'}, 404
            return {'message': 'User deleted successfully'}, 200
        except Exception:
            return {'error': 'An error occurred while deleting the user'}, 500
