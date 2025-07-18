from app.services import facade
from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace("reviews", description="Review operations")

# Define the review model for input validation and documentation
review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(
            required=True, description="Rating of the place (1-5)"
        ),
        "user_id": fields.String(required=True, description="ID of the user"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)


def review_to_dict(review):
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user.id,
        "place_id": review.place.id,
    }


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new review"""
        data = request.json
        try:
            review = facade.create_review(data)
            return review_to_dict(review), 201
        except Exception as e:
            return {"Error": str(e)}, 400

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review_to_dict(r) for r in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"Error": "Review not found"}, 404
        return review_to_dict(review), 200

    @api.expect(review_model)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        """Update a review's information"""
        data = request.json
        try:
            review = facade.update_review(review_id, data)
            if review is None:
                return {"Error": "Review not found"}, 404
            return {"Success": "Review updated successfully"}, 200
        except ValueError as e:
            return {"Error": "Invalid input data"}, 400

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {"Error": "Review not found"}, 404
        return {"Success": "Review deleted successfully"}, 200


@api.route("/places/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"Error": "Place not found"}, 404
        return [review_to_dict(r) for r in reviews], 200
