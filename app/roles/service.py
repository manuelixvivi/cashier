"""
Role Service
"""

from app.roles.model import Role
from app.roles.repository import RoleRepository
from app.core.exceptions import NotFoundException, ConflictException


class RoleService:
    """Role management service"""

    @classmethod
    def create_role(cls, data):
        """Create new role"""
        if RoleRepository.find_by_name(data['name']):
            raise ConflictException('Role already exists')

        role = Role(
            name=data['name'],
            permissions=data.get('permissions', []),
            description=data.get('description', '')
        )
        RoleRepository.create(role)
        return role.to_dict()

    @classmethod
    def get_role(cls, role_id):
        """Get role by ID"""
        role = RoleRepository.find_by_id(role_id)
        if not role:
            raise NotFoundException('Role not found')
        return role.to_dict()

    @classmethod
    def list_roles(cls):
        """List all roles"""
        roles = RoleRepository.list_all()
        return [r.to_dict() for r in roles]

    @classmethod
    def update_role(cls, role_id, data):
        """Update role"""
        role = RoleRepository.find_by_id(role_id)
        if not role:
            raise NotFoundException('Role not found')

        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'permissions' in data:
            update_data['permissions'] = data['permissions']
        if 'description' in data:
            update_data['description'] = data['description']

        RoleRepository.update(role_id, update_data)
        return cls.get_role(role_id)

    @classmethod
    def delete_role(cls, role_id):
        """Delete role"""
        role = RoleRepository.find_by_id(role_id)
        if not role:
            raise NotFoundException('Role not found')

        RoleRepository.delete(role_id)
        return True
