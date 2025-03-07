from flask import Flask
from applications.models import db,User
import os
from flask_restful import Api ,Resource
from applications.api import cache
from applications.workers import celery
from applications.tasks import *
from applications.auth_api import AuthApi,SignupApiSp,SignupApiCu 
from applications.service_api import ServiceApi
from applications.request_api_cu import CustomerDashboardAPI,CancelServiceRequestAPI,CloseServiceRequestAPI,EditServiceRequestAPI,ServiceHistoryAPI,CreateServiceRequestAPI,ServiceDetailsAPI,FetchServiceRequestAPI,CustomerSearchAPI
from applications.request_api_sp import RequestApiSp
from applications.requests_adm import ServiceRequestAPI,AdminSearchAPI,ExportDataAPI,BlockUserAPI
from flask_jwt_extended import JWTManager
from datetime import timedelta
import time

base_dir = os.path.abspath(os.path.dirname(__file__))   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-mad2'
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300



db.init_app(app)
cache.init_app(app)
api=Api(app)
jwt=JWTManager(app)


# celery=workers.celery
celery.conf.update(
        broker_url='redis://localhost:6379',
        result_backend='redis://localhost:6379'
    )
# celery.autodiscover_tasks(['tasks'])
# celery.Task = workers.ContextTask

app.app_context().push() 

def create_admin():
    admin_user=User.query.filter_by(role='admin').first()
    if not admin_user:
        admin_user=User(email='admin@gmail.com',username='admin',password='1234',role='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("admin created")


@app.route('/test_cache')
@cache.cached(timeout=10)
def test_cache():
    time.sleep(10)
    return "testing is working"


api.add_resource(AuthApi,'/api/login','/api/sp','/api/sp/<int:sp_id>')
api.add_resource(SignupApiSp,'/api/signupsp')
api.add_resource(SignupApiCu,'/api/signupcu')
api.add_resource(ServiceApi,'/api/services','/api/services/<int:service_id>') 
api.add_resource(AdminSearchAPI, "/api/admin_dashboard/search")
api.add_resource(BlockUserAPI, '/api/admin_dashboard/block_user/<int:user_id>')
api.add_resource(ExportDataAPI,'/api/admin_dashboard/export_data/<int:sp_id>')
api.add_resource(ServiceRequestAPI, '/api/requests')
api.add_resource(CustomerDashboardAPI, '/api/customer_dashboard')
api.add_resource(ServiceDetailsAPI, '/api/service_details/<int:service_id>')
api.add_resource(FetchServiceRequestAPI, '/api/customer_dashboard/service_request/<int:service_request_id>')
api.add_resource(CreateServiceRequestAPI, '/api/customer_dashboard/create_service_request/<int:service_id>')
api.add_resource(EditServiceRequestAPI, '/api/customer_dashboard/edit_service_request/<int:service_request_id>')
api.add_resource(CancelServiceRequestAPI, '/api/customer_dashboard/cancel_service_request/<int:service_request_id>')
api.add_resource(CloseServiceRequestAPI, '/api/customer_dashboard/close_request/<int:service_request_id>')
api.add_resource(CustomerSearchAPI, '/api/customer_dashboard/search')
api.add_resource(ServiceHistoryAPI, '/api/customer_dashboard/service_history')
api.add_resource(RequestApiSp,'/api/requests_sp','/api/requests_sp/<int:service_request_id>')


if __name__ == '__main__':  
    db.create_all()
    create_admin()
    app.run(debug=True)


