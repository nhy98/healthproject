import logging
from functools import wraps
from flask import request, jsonify
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as rq
from src.config.Constants import Auth, ErrorCode, ErrorMessage
from src.models.UserModel import UserModel


def verify_access_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Verify access token and get user info from token
        Created by: NHYEN
        Created date: 11/08/2021
        """
        access_token = request.headers.get('Authorization')
        if not access_token:
            return jsonify(code=ErrorCode.Unauthorized, message=ErrorMessage.Unauthorized, data=[]), 401

        access_token = access_token.replace("Bearer", "").strip()

        local_user = __verify_access_token(access_token)
        if not local_user:
            return jsonify(code=ErrorCode.Unauthorized, message=ErrorMessage.Unauthorized, data=[]), 401

        return func(local_user, *args, **kwargs)

    return wrapper


def verify_info_empty(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Verify access token and check user info
        Created by: NHYEN
        Created date: 11/08/2021
        """
        access_token = request.headers.get('Authorization')
        if not access_token:
            return jsonify(code=ErrorCode.Unauthorized, message=ErrorMessage.Unauthorized, data=[]), 401

        access_token = access_token.replace("Bearer", "").strip()

        local_user = __verify_access_token(access_token)
        if not local_user:
            return jsonify(code=ErrorCode.Unauthorized, message=ErrorMessage.Unauthorized, data=[]), 401
        if not local_user.name or not local_user.mobile or not local_user.occupation:
            return jsonify(code=ErrorCode.NotFilledInformation, message=ErrorMessage.NotFilledInformation, data=[]), 400

        return func(local_user, *args, **kwargs)

    return wrapper


def __verify_access_token(access_token):
    try:
        # google
        try:
            id_info = id_token.verify_oauth2_token(access_token, rq.Request(), Auth.CLIENT_ID)
        except:
            id_info = None
        if id_info and id_info['iss'] == Auth.GOOGLE_ISS:
            email = id_info['email']
            local_user = UserModel.get_by_email(email)
            return local_user

        # facebook
        fb_param = {'client_id': Auth.FACEBOOK_CLIENT_ID, 'client_secret': Auth.FACEBOOK_SECRET,
                    'grant_type': 'client_credentials'}
        fb_res = requests.get(Auth.FACEBOOK_TOKEN_ENDPOINT, params=fb_param, timeout=10)
        app_access_token = fb_res.json()['access_token'] if fb_res.status_code == 200 else None
        fb_verify_res = requests.get(Auth.FACEBOOK_VERIFY,
                                     params={'input_token': access_token, 'access_token': app_access_token}, timeout=10)
        if fb_verify_res.status_code == 200 and fb_verify_res.json()['data']['is_valid']:
            fb_user_id = fb_verify_res.json()['data']['user_id']
            local_user = UserModel.get_by_fb_user(fb_user_id)
            return local_user
    except Exception as e:
        logging.exception(f"Verify token exception: {e}")
        return {}
