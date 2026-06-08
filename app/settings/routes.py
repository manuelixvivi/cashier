"""
Settings Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from config.settings import SettingsManager

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/', methods=['GET'])
@jwt_required()
def get_settings():
    result = SettingsManager.get_all()
    return APIResponse.success(data=result)


@settings_bp.route('/<key>', methods=['GET'])
@jwt_required()
def get_setting(key):
    result = SettingsManager.get(key)
    return APIResponse.success(data={'key': key, 'value': result})


@settings_bp.route('/<key>', methods=['PUT'])
@jwt_required()
def update_setting(key):
    data = request.get_json()
    SettingsManager.set(key, data.get('value'), data.get('description'))
    return APIResponse.success(data={'key': key, 'value': data.get('value')})


@settings_bp.route('/init', methods=['POST'])
@jwt_required()
def init_defaults():
    SettingsManager.initialize_defaults()
    return APIResponse.success(message='Default settings initialized')
