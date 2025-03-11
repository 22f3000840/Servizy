from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask import jsonify,request
from applications.models import *
from applications.tasks import export_service_requests
from sqlalchemy.exc import SQLAlchemyError
import json
from applications.api import cache

class ServiceRequestAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=5)
    def get(self):
        """Fetch all service requests"""
        try:
            requests = HouseholdServiceRequest.query.all()

            if not requests:
                return {"requests": []}, 200  # ✅ Always return JSON

            requests_data = []
            for req in requests:
                requests_data.append({
                    "id": req.id,
                    "service_professional": {
                        "id": req.service_professional.id if req.service_professional else None,
                        "user_name": req.service_professional.username if req.service_professional else "N/A"
                    },
                    "date_created": req.date_created.strftime("%Y-%m-%d") if req.date_created else "N/A",
                    "status": req.status
                })

            return {"requests": requests_data}, 200  # ✅ Proper JSON response

        except Exception as e:
            print(f"Error fetching requests: {e}")  # ✅ Debugging Log
            return {"message": f"Error fetching requests: {str(e)}"}, 500

class AdminSearchAPI(Resource):

    @jwt_required()
    def get(self):
        """Search users or services based on query parameters."""
        try:
            current_user = json.loads(get_jwt_identity())

            # Ensure the user is an admin
            if current_user.get('role') != 'admin':
                return {"message": "Unauthorized access"}, 403

            search_type = request.args.get('search_type', '').strip().lower()
            search_query = request.args.get('search_query', '').strip()

            if not search_type:
                return {"message": "Missing search_type parameter"}, 400

            if search_type == "user":
                if search_query:
                    results = User.query.filter(User.username.ilike(f"%{search_query}%")).all()
                else:
                    results = User.query.all()  # Return all users if no query
                users = [user.convert_to_json() for user in results]
                return {"users": users}, 200

            elif search_type == "service":
                if search_query:
                    results = HouseholdServices.query.filter(HouseholdServices.service_name.ilike(f"%{search_query}%")).all()
                else:
                    results = HouseholdServices.query.all()  # Return all services if no query
                services = [service.convert_to_json() for service in results]
                return {"services": services}, 200

            else:
                return {"message": "Invalid search_type. Use 'user' or 'service'."}, 400

        except SQLAlchemyError as e:
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

    @jwt_required()
    def patch(self, user_id):
        """Block or unblock a user."""
        try:
            current_user = json.loads(get_jwt_identity())

            # Ensure the user is an admin
            if current_user.get('role') != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get the user to update
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            # Toggle the is_flagged status
            user.is_flagged = not user.is_flagged
            db.session.commit()

            return {
                "message": "User updated successfully",
                "user": user.convert_to_json()
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

class BlockUserAPI(Resource):
    @jwt_required()
    def patch(self, user_id):
        try:
            current_user = json.loads(get_jwt_identity())

            # Ensure the user is an admin
            if current_user.get('role') != 'admin':
                return {"message": "Unauthorized access"}, 403

            # Get the user to update
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            # Toggle the is_flagged status
            user.is_flagged = not user.is_flagged
            db.session.commit()

            return {
                "message": "User updated successfully",
                "user": user.convert_to_json()  # Return the updated user object
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
        
class ExportDataAPI(Resource):
    @jwt_required()
    def get(self,sp_id):
        try:
            current_user = json.loads(get_jwt_identity())
            if current_user.get('role') != 'admin':
                return {"message": "Unauthorized access"}, 403
            sp = User.query.get(sp_id)
            if not sp:
                return {"message": "Service Professional not found"}, 404
            
            # Fetch closed service requests handled by the service professional
            requests = HouseholdServiceRequest.query.filter_by(
                service_professional_id=sp_id, status='closed', closed_by='service_professional'
            ).all()
            # Prepare data response
            data = [
                {
                    "service_id": req.service_id,
                    "customer_id": req.customer_id,
                    "professional_id": req.service_professional_id,
                    "date_of_request": req.date_created.strftime('%Y-%m-%d') if req.date_created else None,
                    "description": req.description  # Assuming "remarks" refers to "description"
                }
                for req in requests
            ]
            export_service_requests(sp_id)
            return {"message": "Data exported successfully", "data": data}, 200

        except SQLAlchemyError as e:
            return {"message": "Database error", "error": str(e)}, 500
           