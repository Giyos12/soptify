from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='teacher').exists():
                return True
            else:
                return False
        else:
            return False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='student').exists():
                return True
            else:
                return False
        else:
            return False
