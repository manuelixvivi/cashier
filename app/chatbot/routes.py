"""
Chatbot Routes
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.core.response import APIResponse
from app.chatbot.ai_router import AIRouter

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """Process chatbot message"""
    data = request.get_json()
    text = data.get('message', '')
    force_mode = data.get('mode')  # online, offline, hybrid

    if not text:
        return APIResponse.error(
            message='Message is required',
            error_code='VALIDATION_ERROR'
        )

    router = AIRouter()
    result = router.process(text, force_mode=force_mode)

    return APIResponse.success(data=result)


@chatbot_bp.route('/mode', methods=['GET'])
@jwt_required()
def get_mode():
    """Get current AI mode"""
    import os
    router = AIRouter()
    return APIResponse.success(data={
        'mode': os.getenv('AI_MODE', 'offline'),
        'online_available': router.is_online_available()
    })
