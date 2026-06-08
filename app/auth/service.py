"""
Auth Service - Business logic layer
"""

from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from app.core.extensions import bcrypt
from app.core.exceptions import UnauthorizedException, ConflictException, ValidationException
from app.auth.model import User, RefreshToken
from app.auth.repository import UserRepository, RefreshTokenRepository


class AuthService:
    """Authentication service"""

    @classmethod
    def register(cls, data):
        """Register new user"""
        # Check if username exists
        if UserRepository.find_by_username(data['username']):
            raise ConflictException('Username already exists')

        # Check if email exists
        if UserRepository.find_by_email(data['email']):
            raise ConflictException('Email already exists')

        # Hash password
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            full_name=data.get('full_name', ''),
            role=data.get('role', 'cashier')
        )

        UserRepository.create(user)
        return user.to_dict()

    @classmethod
    def login(cls, username, password):
        """Authenticate user and generate tokens"""
        user = UserRepository.find_by_username(username)

        if not user:
            raise UnauthorizedException('Invalid username or password')

        if not user.is_active:
            raise UnauthorizedException('Account is deactivated')

        if not bcrypt.check_password_hash(user.password_hash, password):
            raise UnauthorizedException('Invalid username or password')

        # Update last login
        UserRepository.update_last_login(user._id)

        # Generate tokens
        access_token = create_access_token(
            identity=str(user._id),
            additional_claims={'role': user.role, 'username': user.username}
        )
        refresh_token_str = create_refresh_token(identity=str(user._id))

        # Store refresh token
        refresh_token = RefreshToken(
            user_id=user._id,
            token=refresh_token_str,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        RefreshTokenRepository.create(refresh_token)

        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token_str,
            'token_type': 'Bearer'
        }

    @classmethod
    def refresh_access_token(cls, refresh_token_str):
        """Refresh access token using refresh token"""
        token = RefreshTokenRepository.find_by_token(refresh_token_str)

        if not token or token.revoked:
            raise UnauthorizedException('Invalid refresh token')

        if token.expires_at < datetime.utcnow():
            raise UnauthorizedException('Refresh token expired')

        user = UserRepository.find_by_id(token.user_id)

        if not user or not user.is_active:
            raise UnauthorizedException('User not found or deactivated')

        # Generate new access token
        access_token = create_access_token(
            identity=str(user._id),
            additional_claims={'role': user.role, 'username': user.username}
        )

        return {
            'access_token': access_token,
            'token_type': 'Bearer'
        }

    @classmethod
    def logout(cls, refresh_token_str):
        """Logout user by revoking refresh token"""
        RefreshTokenRepository.revoke_token(refresh_token_str)
        return True

    @classmethod
    def logout_all(cls, user_id):
        """Logout user from all devices"""
        RefreshTokenRepository.revoke_all_user_tokens(user_id)
        return True

    @classmethod
    def change_password(cls, user_id, old_password, new_password):
        """Change user password"""
        user = UserRepository.find_by_id(user_id)

        if not user:
            raise UnauthorizedException('User not found')

        if not bcrypt.check_password_hash(user.password_hash, old_password):
            raise ValidationException('Old password is incorrect')

        new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        UserRepository.update(user_id, {'password_hash': new_password_hash})

        # Revoke all tokens
        RefreshTokenRepository.revoke_all_user_tokens(user_id)

        return True

    @classmethod
    def get_current_user(cls, user_id):
        """Get current user by ID"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise UnauthorizedException('User not found')
        return user.to_dict()
