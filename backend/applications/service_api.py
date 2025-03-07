from flask import  request,current_app as app
from flask_restful import Resource, reqparse, marshal_with,Api
from applications.models import *
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
import json
from .api import cache

class ServiceApi(Resource):
#     # @jwt_required()
#     # @cache.cached(timeout=50)
#     def get(self):
#         services=HouseholdServices.query.all()
#         service_json=[]
#         for service in services:
#             # service_dict={"name":service.service_name,"price":service.base_price,"time":service.time_required,"description":service.service_description}
#             # service_json.append(service_dict)
#             service_json.append(service.convert_to_json())
#         return service_json,200
    def get(self, service_id=None):
        if service_id:
            # Fetch a specific service by ID
            service = HouseholdServices.query.get(service_id)
            if not service:
                return {"error": "Service not found"}, 404
            return service.convert_to_json(), 200
        else:
            # Fetch all services
            services = HouseholdServices.query.all()
            service_json = [service.convert_to_json() for service in services]
            return service_json, 200
    @jwt_required()
    def post(self):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        data=request.get_json()
        if not (data.get('service_name') or data.get('base_price') or data.get('time_required') or data.get('service_description')):
            return {'message':'invalid data'},400
        if len(data.get('service_name').strip())>80 or len(data.get('service_name').strip())<2:
            return {'message':'service name should be between 2 and 80 characters'},400
        name=data.get('service_name')
        price=data.get('base_price')
        time=data.get('time_required')
        description=data.get('service_description')
        new_service=HouseholdServices(service_name=name,base_price=price,time_required=time,service_description=description)
        db.session.add(new_service)
        db.session.commit()
        return {'message':'service created successfully'},201
    @jwt_required()
    def put(self,service_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        data=request.get_json()
        name=data.get('service_name')
        price=data.get('base_price')
        time=data.get('time_required')
        description=data.get('service_description')
        service=HouseholdServices.query.get(service_id)
        if not service:
            return {'message':'service not found'},404
        service.service_name=name
        service.base_price=price
        service.time_required=time
        service.service_description=description
        db.session.commit()
        return {'message':'service updated successfully'},200
    @jwt_required()
    def delete(self,service_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        service=HouseholdServices.query.get(service_id)
        if not service:
            return {'message':'service not found'},404 
        db.session.delete(service)
        db.session.commit()
        return {'message':'service deleted successfully'},200
    