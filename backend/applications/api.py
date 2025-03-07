from flask import  request,current_app as app
from flask_restful import Resource, reqparse, marshal_with,Api
from applications.models import *
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token
import json
from flask_caching import Cache
import time

cache=Cache()

# @app.route('/test_cache')
# @cache.cached(timeout=10)
# def test_cache():
#     time.sleep(10)
#     return "testing is working"



