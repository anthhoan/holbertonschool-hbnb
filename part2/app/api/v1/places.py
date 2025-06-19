from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.place import Place

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_input_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_output_model = api.inherit('PlaceOutput', place_input_model, {
    'id': fields.String(description='ID of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        data = api.payload

        if not data.get('title') or not data.get('price') or not data.get('latitude') or not data.get('longitude') or not data.get('owner_id'):
            return {'message': 'Missing required fields'}, 400


        new_place = Place(**data)
        facade.place_repo.add(new_place)

        return {'message': 'Place successfully created'}, 201
    
    @api.marshal_list_with(place_output_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        return facade.place_repo.get_all()

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        pass


    this is a test
