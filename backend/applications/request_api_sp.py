from flask import  request,current_app as app
from flask_restful import Resource, reqparse, marshal_with,Api
from applications.models import *
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
import json


class RequestApiSp(Resource):
    @jwt_required()
    def get(self):
        current_user = json.loads(get_jwt_identity())
        print("JWT Payload:", current_user)  

        if current_user.get('role') != 'service_professional':
            return {'message': 'unauthorized'}, 403

        sp = User.query.filter_by(username=current_user.get('username')).first()
        if not sp:
            return {'message': 'User not found'}, 404
        if not sp.is_approved:
            return {'message': 'your account is not approved by admin'}, 400
        if sp.service_id is None:
            return {'message': 'you are not associated with any service'}, 400

        pending_requests = HouseholdServiceRequest.query.filter_by(service_professional_id=sp.id, status='pending').all()
        accepted_requests = HouseholdServiceRequest.query.filter_by(service_professional_id=sp.id, status='accepted').all()
        closed_requests = HouseholdServiceRequest.query.filter_by(service_professional_id=sp.id, status='closed').all()

        return {
            'pending_requests': [r.convert_to_json() for r in pending_requests],
            'accepted_requests': [r.convert_to_json() for r in accepted_requests],
            'closed_requests': [r.convert_to_json() for r in closed_requests]
        }, 200

    # @jwt_required()
    # def patch(self, service_request_id):
    #     current_user = json.loads(get_jwt_identity())

    #     if current_user.get('role') != 'service_professional':
    #         return {'message': 'unauthorized'}, 403

    #     sp = User.query.filter_by(username=current_user.get('username')).first()
    #     service_request = HouseholdServiceRequest.query.get_or_404(service_request_id)

    #     # Ensure only the assigned service professional can modify the request
    #     if service_request.service_professional_id != sp.id:
    #         return {'message': 'unauthorized'}, 403

    #     if service_request.status == 'pending':
    #         service_request.status = 'accepted'
    #         db.session.commit()
    #         return {'message': 'service request accepted successfully'}, 200
    #     else:
    #         return {'message': 'service request already accepted or closed'}, 400   
    @jwt_required()
    def patch(self,service_request_id):
        """Handles accepting, rejecting, and closing service requests."""
        current_user = json.loads(get_jwt_identity())

        # Ensure only service professionals and customers can modify requests
        if current_user.get("role") not in ["service_professional", "customer"]:
            return {"message": "Unauthorized"}, 403

        request_data = request.get_json()
        action = request_data.get("action")

        service_request = HouseholdServiceRequest.query.get(service_request_id)

        if not service_request:
            return {"message": "Service request not found"}, 404

        if action == "accept":
            service_request.status = "accepted"
        elif action == "reject":
            service_request.status = "rejected"
        elif action == "close":
            if service_request.status != "accepted":
                return {"message": "Only accepted requests can be closed"}, 400
            
            service_request.status = "closed"
            service_request.date_closed = datetime.utcnow()

            # Store who closed the request
            if current_user["role"] == "service_professional":
                service_request.closed_by = "service_professional"
            elif current_user["role"] == "customer":
                service_request.closed_by = "customer"
        else:
            return {"message": "Invalid action"}, 400

        db.session.commit()
        return {"message": f"Request {action}d successfully", "closed_by": service_request.closed_by}, 200

    @jwt_required()
    def delete(self, service_request_id):
        current_user = json.loads(get_jwt_identity())

        if current_user.get('role') != 'service_professional':
            return {'message': 'unauthorized'}, 403

        sp = User.query.filter_by(username=current_user.get('username')).first()
        service_request = HouseholdServiceRequest.query.get_or_404(service_request_id)

        # Ensure only the assigned service professional can modify the request
        if service_request.service_professional_id != sp.id:
            return {'message': 'unauthorized'}, 403

        if service_request.status == 'pending':
            service_request.status = 'rejected'
            db.session.commit()
            return {'message': 'service request rejected successfully'}, 200
        else:
            return {'message': 'service request already accepted or closed'}, 400