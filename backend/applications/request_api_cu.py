from flask import  request,jsonify,current_app as app
from flask_restful import Resource, reqparse, marshal_with,Api
from applications.models import *
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
import json
from .api import cache

# class RequestApiCu(Resource):

#     @jwt_required()
#     @cache.cached(timeout=120)
#     def get(self):
#         current_user=json.loads(get_jwt_identity())
#         if current_user.get('role')!='customer':
#             return {'message':'unauthorized'},403
#         requests=HouseholdServiceRequest.query.filter_by(customer_id=current_user.get('id')).all()
#         return marshal_with(HouseholdServiceRequest.convert_to_json)(requests),200
#     @jwt_required()
#     def post(self,service_id):
#         current_user=json.loads(get_jwt_identity())
#         if current_user.get('role')!='customer':
#             return {'message':'unauthorized'},403
#         data=request.get_json() # equal to request.json
#         service_professional=data.get('service_professional')
#         description=data.get('description')
#         sp_id=User.query.filter_by(username=service_professional).first().id
#         customer=User.query.filter_by(id=current_user.get('id')).first()
#         service_request=HouseholdServiceRequest(customer_id=customer.id,service_professional_id=sp_id,description=description,
#                                                service_id=service_id,request_type='private',status='pending')
#         db.session.add(service_request)
#         db.session.commit()
#         return {'message':'service request created successfully'},201
#     @jwt_required()
#     def put(self,service_request_id):
#         current_user=json.loads(get_jwt_identity())
#         if current_user.get('role')!='customer':
#             return {'message':'unauthorized'},403
#         data=request.get_json()
#         service_request=HouseholdServiceRequest.query.get_or_404(service_request_id)
#         description=data.get('description')
#         service_request.description=description
#         db.session.commit()
#         return {'message':'service request updated successfully'},200
    
#     @jwt_required()
#     def delete(self,service_request_id):
#         current_user=json.loads(get_jwt_identity())
#         if current_user.get('role')!='customer':
#             return {'message':'unauthorized'},403
#         service_request=HouseholdServiceRequest.query.get_or_404(service_request_id)
#         db.session.delete(service_request)
#         db.session.commit()
#         return {'message':'service request deleted successfully'},200

class CustomerDashboardAPI(Resource):

    @jwt_required()
    def get(self):
        """Fetch available services and service history for customers"""
        try:
            # Get logged-in customer details
            current_user = json.loads(get_jwt_identity())

            if current_user.get('role') != 'customer':
                return {'message': 'Unauthorized'}, 403

            # Fetch all available services
            services = HouseholdServices.query.all()
            available_services = [service.convert_to_json() for service in services]

            # Fetch service requests made by the logged-in customer
            service_requests = HouseholdServiceRequest.query.filter_by(customer_id=current_user.get('id')).all()
            service_history = [
                {
                    'request_id': req.id,
                    'service_name': req.service.service_name if req.service else "Unknown",
                    'service_professional': req.service_professional.username if req.service_professional else "Unassigned",
                    'description': req.description,
                    'request_type':req.request_type,
                    'status': req.status,
                    'request_date': req.date_created.strftime('%Y-%m-%d %H:%M') if req.date_created else "N/A",
                    'rating': req.rating_by_customer ,
                    'review': req.review_by_customer if req.review_by_customer else "No review provided yet"
                }
                for req in service_requests
            ]

            return jsonify({
                'available_services': available_services,
                'service_history': service_history
            })

        except Exception as e:
            return {'message': f'Error fetching dashboard data: {str(e)}'}, 500


class CreateServiceRequestAPI(Resource):

    @jwt_required()
    def post(self, service_id):
        """Create a new service request"""
        try:
            current_user = json.loads(get_jwt_identity())
            if current_user.get('role') != 'customer':
                return {'message': 'Unauthorized'}, 403

            data = request.get_json()
            service_professional = data.get('service_professional')
            description = data.get('description')

            sp_user = User.query.filter_by(role='service_professional',username=service_professional).first()
            if not sp_user:
                return {'message': 'Service professional not found'}, 404

            service_request = HouseholdServiceRequest(
                customer_id=current_user.get('id'),
                service_professional_id=sp_user.id,
                description=description,
                service_id=service_id,
                request_type='private',
                status='pending'
            )

            db.session.add(service_request)
            db.session.commit()
            return {'message': 'Service request created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating request: {str(e)}'}, 500


class ServiceHistoryAPI(Resource):

    @jwt_required()
    def get(self):
        """Get service history for a customer"""
        try:
            current_user = json.loads(get_jwt_identity())
            if current_user.get('role') != 'customer':
                return {'message': 'Unauthorized'}, 403

            requests = HouseholdServiceRequest.query.filter_by(customer_id=current_user.get('id')).all()
            return jsonify([req.convert_to_json() for req in requests])
        except Exception as e:
            return {'message': f'Error fetching service history: {str(e)}'}, 500


class EditServiceRequestAPI(Resource):
    @jwt_required()
    def put(self, service_request_id):
        """Edit an existing service request."""
        try:
            current_user = json.loads(get_jwt_identity())

            # Ensure the user is a customer
            if current_user.get('role') != 'customer':
                return {"message": "Unauthorized access"}, 403

            # Fetch the service request
            service_request = HouseholdServiceRequest.query.get_or_404(service_request_id)

            # Get the new description from request data
            data = request.get_json()
            description = data.get('description', '').strip()

            # Update the description
            service_request.description = description
            db.session.commit()

            return {"message": "Service request updated successfully"}, 200

        except Exception as e:
            return {"message": f"Error updating service request: {str(e)}"}, 500


class CancelServiceRequestAPI(Resource):

    @jwt_required()
    def delete(self, service_request_id):
        """Cancel (delete) a service request"""
        try:
            current_user = json.loads(get_jwt_identity())
            if current_user.get('role') != 'customer':
                return {'message': 'Unauthorized'}, 403

            service_request = HouseholdServiceRequest.query.get_or_404(service_request_id)

            db.session.delete(service_request)
            db.session.commit()
            return {'message': 'Service request cancelled successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error canceling request: {str(e)}'}, 500


class CloseServiceRequestAPI(Resource):
    @jwt_required()
    def post(self, service_request_id):
        """Close a service request"""
        try:
            current_user = json.loads(get_jwt_identity())
            customer_id = current_user.get("id")

            # Validate customer_id
            if customer_id is None:
                return {"message": "Invalid customer ID in token"}, 400
            customer_id = int(customer_id)  # Convert only after checking for None

            # Fetch the service request
            service_request = HouseholdServiceRequest.query.get(service_request_id)
            if not service_request:
                return {"message": "Service request not found"}, 404

            # Validate service request owner
            if service_request.customer_id is None:
                return {"message": "Service request has no associated customer"}, 400
            if int(service_request.customer_id) != customer_id:
                return {"message": "Unauthorized: This request does not belong to you"}, 403

            # Process request closure
            data = request.get_json()
            review = data.get("review", "")
            rating = data.get("rating", 0)

            service_request.status = "closed"
            service_request.review_by_customer = review
            service_request.rating_by_customer = int(rating)
            service_request.date_closed = datetime.now().date()
            service_request.closed_by = 'customer'

            # Update service professional's rating
            sp_user = User.query.get(service_request.service_professional_id)
            if sp_user:
                temp = sp_user.rating_count
                sp_user.rating_count += 1
                sp_user.avg_rating = (sp_user.avg_rating * temp + int(rating)) / (sp_user.rating_count)

            db.session.commit()
            return {"message": "Service request closed successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error closing request: {str(e)}"}, 500

        
class ServiceDetailsAPI(Resource):
    @jwt_required()
    def get(self, service_id):
        service = HouseholdServices.query.get_or_404(service_id)
        professionals = User.query.filter_by(role='service_professional',service_id=service_id).all()

        return jsonify({
            'service': {
                'id': service.id,
                'service_name': service.service_name
            },
            'service_professionals': [{'user_name': sp.username} for sp in professionals]
        })
    
class FetchServiceRequestAPI(Resource):
    @jwt_required()
    def get(self, service_request_id):
        """Fetch a specific service request by its ID."""
        try:
            # Get current user
            current_user = get_jwt_identity()

            # Query the service request
            service_request = HouseholdServiceRequest.query.get(service_request_id)

            if not service_request:
                return {"message": "Service request not found"}, 404

            # Convert the service request to JSON
            request_data = {
                "id": service_request.id,
                "service_name": service_request.service.service_name if service_request.service else "Unknown",
                "service_professional": service_request.service_professional.username if service_request.service_professional else "Unknown",
                "description": service_request.description,
            }

            return jsonify(request_data)

        except Exception as e:
            return {"message": f"Error fetching service request: {str(e)}"}, 500

# class CustomerSearchAPI(Resource):
    
#     @jwt_required()
#     def get(self):
#         """Search services based on query parameters."""
#         try:
#             current_user = json.loads(get_jwt_identity())

#             # Ensure the user is a customer
#             if current_user.get('role') != 'customer':
#                 return {'message': 'Unauthorized'}, 403

#             search_type = request.args.get('search_type', '').strip().lower()
#             search_query = request.args.get('search_query', '').strip()

#             query = HouseholdServices.query.join(User).filter(User.is_approved == True)

#             if search_query:
#                 if search_type == 'pincode':
#                     query = query.filter(User.pincode.ilike(f"%{search_query}%"))
#                 elif search_type == 'service_name':
#                     query = HouseholdServices.query.filter(HouseholdServices.service_name.ilike(f"%{search_query}%"))
#                 elif search_type == 'address':
#                     query = query.filter(User.address.ilike(f"%{search_query}%"))

#             services = query.all()
#             services_data = [service.convert_to_json() for service in services]

#             return {
#                 'customer_name': current_user.get('username'),
#                 'services': services_data
#             }, 200

#         except Exception as e:
#             return {'message': f'Error fetching services: {str(e)}'}, 500             

# Import your models



class CustomerSearchAPI(Resource):
   @jwt_required()
   def get(self):
        """Search services based on query parameters."""
        try:
            # Extract user details from JWT
            current_user = json.loads(get_jwt_identity())

            # Ensure user is a customer
            if current_user.get('role') != 'customer':
                return {"error": "Unauthorized"}, 403  # ✅ Return dict, NOT `jsonify()`

            # Extract search parameters
            search_type = request.args.get("search_type", "").strip().lower()
            search_query = request.args.get("search_query", "").strip()

            # Base query: Get only approved service providers
            query = HouseholdServices.query.join(User).filter(User.is_approved == True)

            if search_query:
                if search_type == "pincode":
                    query = query.filter(User.pincode.ilike(f"%{search_query}%"))
                elif search_type == "service_name":
                    query = query.filter(HouseholdServices.service_name.ilike(f"%{search_query}%"))
                elif search_type == "address":
                    query = query.filter(User.address.ilike(f"%{search_query}%"))

            # Fetch results
            services = query.all()

            # Convert services to JSON format
            service_list = [
                {
                    "id": s.id,
                    "service_name": s.service_name,
                    "description": s.service_description,
                    "base_price": s.base_price,
                    "time_required": s.time_required,
                    "service_professionals": [
                        {"id": sp.id, "username": sp.username, "avg_rating": sp.avg_rating}
                        for sp in s.service_professionals
                    ],
                }
                for s in services
            ]

            return {"customer_name": current_user.get("username"), "services": service_list}, 200  # ✅ Return JSON-serializable dict

        except Exception as e:
            return {"error": str(e)}, 500  # ✅ Return JSON-serializable dict