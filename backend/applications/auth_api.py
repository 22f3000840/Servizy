from flask import  request,current_app as app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_restful import Resource, reqparse, marshal_with,Api
from applications.models import *
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
import json

api=Api()


class LoginApi(Resource):
    def post(self):
        email=request.get_json().get('email')
        password=request.get_json().get('password')
        user=User.query.filter_by(email=email).first()
        if user and user.password==password:
            if user.role=='service_professional':
                if user.is_approved==False:
                    return {'message':'your account is not approved yet by admin'},400
                if user.is_flagged==True:
                    return {'message':'your account is blocked by admin'},400
                services=HouseholdServices.query.all()
                if user.service_id not in [service.id for service in services]:
                    return {'message':'your service is not available,please register for another service'},400
            elif user.role=='customer':
                if user.is_flagged==True:
                    return {'message':'your account is blocked by admin'},400
            token=create_access_token(identity=json.dumps({'id':str(user.id),'username':user.username,'role':user.role}))
            return {'message':'login successful','token':token,'user_role':user.role,'user_name':user.username},200
        else:
            return {'message':'invalid email or password'},400
class AuthApi(Resource):
    @jwt_required()
    def get(self):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        sps=User.query.filter_by(role='service_professional',is_approved=False).all()
        sp_json=[]
        for sp in sps:
            sp_json.append(sp.convert_to_json())
        return sp_json,200





    def post(self):
        # data=request.get_json() # equal to request.json
        # if not (data.get('email') or data.get('password')):
        #     return {'message':'both email and password are required'},400
        # user=User.query.filter_by(email=data.get('email')).first()
        # if not user:
        #     return {'message':'user not found'},404
        # if user.password!=data.get('password'):
        #         return {'message':'password incorrect'},400
        # if user.is_approved==False and user.role=='service_professional':
        #     return {'message':'your account is not approved by admin'},400
        # token=create_access_token(identity=json.dumps({'id':str(user.id),'username':user.username,'role':user.role}))
        # return {'message':'login successful','token':token,'user_role':user.role,'username':user.username},200   

    
        email=request.get_json().get('email')
        password=request.get_json().get('password')
        user=User.query.filter_by(email=email).first()
        if user and user.password==password:
            if user.role=='service_professional':
                if user.is_approved==False:
                    return {'message':'your account is not approved yet by admin'},400
                if user.is_flagged==True:
                    return {'message':'your account is blocked by admin'},400
                services=HouseholdServices.query.all()
                if user.service_id not in [service.id for service in services]:
                    return {'message':'your service is not available,please register for another service'},400
            elif user.role=='customer':
                if user.is_flagged==True:
                    return {'message':'your account is blocked by admin'},400
            token=create_access_token(identity=json.dumps({'id':str(user.id),'username':user.username,'role':user.role}))
            return {'message':'login successful','token':token,'user_role':user.role,'username':user.username},200
    
    @jwt_required()
    def patch(self,sp_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        sp=User.query.filter_by(id=sp_id).first()
        if not sp:
            return {'message':'service professional not found'},404
        sp.is_approved=True
        db.session.commit()
        return {'message':'service professional approved successfully'},200
    
    @jwt_required()
    def delete(self,sp_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        sp=User.query.filter_by(id=sp_id).first()
        if not sp:
            return {'message':'service professional not found'},404
        db.session.delete(sp)
        db.session.commit()
        return {'message':'service professional rejected successfully'},200
        
            
        
# class SignupApi(Resource):
#     def post(self):
#         data=request.get_json()
#         if not (data.get('username') or data.get('password') or data.get('role')):
#             return {'message':'invalid data'},400
#         if len(data.get('username').strip())>60 or len(data.get('username').strip())<4:
#             return {'message':'username shuold be between 4 and 60 characters'},400
#         if len(data.get('password').strip())>80 or len(data.get('password').strip())<4:
#             return {'message':'password shuold be between 4 and 80 characters'},400
#         if data.get('role').strip() not in ['customer','service_professional']:
#             return {'message':'invalid role'},400
#         user=User.query.filter_by(username=data.get('username')).first()
#         if user:
#             return {'message':'user already exists'},400
#         else:
#             new_user=User(username=data.get('username').strip(),password=data.get('password').strip(),
#                           role=data.get('role').strip(),
#                           is_approved=False if data.get('role').strip()=='service_professional' else True)
#             db.session.add(new_user)
#             db.session.commit()
#             return {'message':'user created successfully'},201
        
class SignupApiSp(Resource):
    def post(self):
        data=request.get_json() 
        if not (data.get('email') or data.get('password') or data.get('role')):
            return {'message':'invalid data'},400
        if len(data.get('email').strip())>60 or len(data.get('email').strip())<3:
            return {'message':'username shuold be between 4 and 60 characters'},400
        if len(data.get('password').strip())>80 or len(data.get('password').strip())<4:
            return {'message':'password shuold be between 4 and 80 characters'},400
        # if data.get('role').strip() not in ['service_professional']:
        #     return {'message':'invalid role'},400
        service=data.get('service')
        
        service=HouseholdServices.query.filter_by(service_name=service).first()
        if not service:
            return {"message": "Service not found"}, 400  # Prevent AttributeError
        user=User.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message':'user already exists'},400
        else:
            new_user=User(email=data.get('email').strip(),username=data.get('username').strip(),password=data.get('password').strip(),
                          address=data.get('address'),pincode=data.get('pincode'),
                          service_id=service.id,is_approved=False,role='service_professional')
            db.session.add(new_user)
            db.session.commit()
            return {'message':'service professional created successfully'},201
        
class SignupApiCu(Resource):
    def post(self):
        data=request.get_json()
        if not (data.get('email') or data.get('password') or data.get('role')):
            return {'message':'invalid data'},400
        if len(data.get('email').strip())>60 or len(data.get('email').strip())<2:
            return {'message':'username shuold be between 4 and 60 characters'},400
        if len(data.get('password').strip())>80 or len(data.get('password').strip())<4:
            return {'message':'password shuold be between 4 and 80 characters'},400
        # if data.get('role').strip() not in ['customer']:
        #     return {'message':'invalid role'},400
        user=User.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message':'user already exists'},400
        else:
            new_user=User(email=data.get('email').strip(),password=data.get('password').strip(),username=data.get('username').strip(),
                          address=data.get('address'),pincode=data.get('pincode'),
                          role='customer')
            db.session.add(new_user)
            db.session.commit()
            return {'message':'customer created successfully'},201

class LogoutApi(Resource):
    @jwt_required()
    def post(self):
        return {'message':'logout successful'},200
    
class AdminDashboardApi(Resource):
    @jwt_required()
    def get(self):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        users=User.query.all()
        services=HouseholdServices.query.all()
        requests=HouseholdServiceRequest.query.all()
        unapproved_sp=User.query.filter_by(role='service_professional',is_approved=False).all()
        return ({
            'users':[user.convert_to_json() for user in users],
            'services':[service.convert_to_json() for service in services],
            'requests':[request.convert_to_json() for request in requests],
            'unapproved_sp':[unapproved.convert_to_json() for unapproved in unapproved_sp]
        })
    
class ApproveSpApi(Resource):
    @jwt_required()
    def put(self,sp_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        sp=User.query.filter_by(id=sp_id).first()
        if not sp:
            return {'message':'service professional not found'},404
        sp.is_approved=True
        db.session.commit()
        return {'message':'service professional approved successfully'},200
    #creating resource api class to view the details of the service professional by admin
    @jwt_required()
    def get(self,sp_id):
        current_user=json.loads(get_jwt_identity())
        if current_user.get('role')!='admin':
            return {'message':'unauthorized'},403
        sp=User.query.filter_by(id=sp_id).first()
        if not sp:
            return {'message':'service professional not found'},404
        return sp.convert_to_json()


