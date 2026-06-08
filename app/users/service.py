"""
User Service
"""

from app.auth.repository import UserRepository
from app.users.repository import UserProfileRepository
from app.core.exceptions import NotFoundException


class UserService:
    """User management service"""

    @classmethod
    def get_user(cls, user_id):
        """Get user with profile"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundException('User not found')

        result = user.to_dict()
        profile = UserProfileRepository.find_by_user_id(user_id)
        if profile:
            result['profile'] = profile.to_dict()

        return result

    @classmethod
    def list_users(cls, page=1, per_page=20, role=None, is_active=None):
        """List users with filters"""
        filters = {}
        if role:
            filters['role'] = role
        if is_active is not None:
            filters['is_active'] = is_active

        skip = (page - 1) * per_page
        users, total = UserRepository.list_all(skip=skip, limit=per_page, filters=filters)

        total_pages = (total + per_page - 1) // per_page

        return {
            'users': [u.to_dict() for u in users],
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }

    @classmethod
    def update_user(cls, user_id, data):
        """Update user"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundException('User not found')

        update_data = {}
        allowed_fields = ['email', 'full_name', 'role', 'is_active']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]

        UserRepository.update(user_id, update_data)

        if 'profile' in data:
            UserProfileRepository.upsert(user_id, data['profile'])

        return cls.get_user(user_id)

    @classmethod
    def deactivate_user(cls, user_id):
        """Deactivate user"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundException('User not found')

        UserRepository.update(user_id, {'is_active': False})
        return True
