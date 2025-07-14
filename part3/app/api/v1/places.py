from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask import request



api = Namespace("places", description="Place operations")

link_model = api.model('AmenityLink', {
    'amenity_id': fields.String(required=True, description="ID of the amenity to add")
})

# Define the models for related entities
amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

# Add the review model for nested reviews
review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

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

place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='ID of the place'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner ID'),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))
})





@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new place"""
        data = api.payload

        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        if not all(data.get(field) for field in required_fields):
            return {'Error': 'Missing required fields'}, 400

        # Extract amenities from data before creating place
        amenities = data.pop('amenities', [])

        try:
            # Create place using facade
            new_place = facade.create_place(data)

            # Handle amenities if provided
            if amenities:
                for amenity_id in amenities:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        new_place.add_amenity(amenity)

            return {
                'message': 'Place successfully created',
                'place': {
                    'id': new_place.id,
                    'title': new_place.title,
                    'description': new_place.description,
                    'price': new_place.price,
                    'latitude': new_place.latitude,
                    'longitude': new_place.longitude,
                    'owner_id': new_place.owner_id
                }
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.marshal_list_with(place_output_model)
    @api.response(200, 'List of places retrieved successfully')

    
    def get(self):
        """Retrieve a list of all places with amenities and reviews"""
        places = facade.place_repo.get_all()
        return [place.to_dict() for place in places]



@api.route("/<place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id.strip())

        if not place:
            return {"Error": "Place not found"}, 404

        return place.to_dict() if hasattr(place, "to_dict") else str(place), 200

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload

        updated_place = facade.update_place(place_id.strip(), data)

        if not updated_place:
            return {'Error': 'Place not found'}, 404

        return {
            'Success': 'Place updated successfully',
            'Updated': updated_place.to_dict() if hasattr(updated_place, 'to_dict') else str(updated_place)
        }, 200
    
    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    def delete(self, place_id):
        """Delete a place by ID"""
        success = facade.delete_place(place_id.strip())

        if not success:
            return {"Error": "Place not found"}, 404

        return {"Success": "Place deleted successfully"}, 200
    
@api.route('/<place_id>/add_amenity')
class AddAmenityToPlace(Resource):
    @api.expect(link_model)
    @api.response(200, 'Amenity successfully added to place')
    @api.response(404, 'Place or amenity not found')
    def post(self, place_id):
        """Add an amenity to a place"""
        data = request.get_json()
        amenity_id = data.get("amenity_id")
        try:
            place = facade.add_amenity_to_place(place_id, amenity_id)
            return place.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
