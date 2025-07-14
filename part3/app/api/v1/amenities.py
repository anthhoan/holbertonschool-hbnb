from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

link_model = api.model('AmenityLink', {
    'amenity_id': fields.String(required=True, description="ID of the amenity to add")
})

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def amenity_to_dict(amenity):
    return {
        "id": amenity.id,
        "name": amenity.name,
    }

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.json
        try:
            amenity = facade.create_amenity(data)
            return amenity_to_dict(amenity), 201
        except Exception as e:
            return {"Error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity_to_dict(a) for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"Error": "Amenity not found"}, 404
        return amenity_to_dict(amenity), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.json
        try:
            amenity = facade.update_amenity(amenity_id, data)
            if not amenity:
                return {"Error": "Amenity not found"}, 404
            return {"Success": "Amenity updated successfully"}, 200
        except Exception as e:
            return {"Error": str(e)}, 400
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        success = facade.amenity_repo.delete(amenity_id)
        if success:
            return {"Success": "Amenity deleted successfully"}, 200
        return {"Error": "Amenity not found"}, 404
    
