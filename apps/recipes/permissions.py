from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSellerOrReadOnly(BasePermission):
    """
    - Customers (read-only): can list and retrieve recipes.
    - Sellers: can create, update, and delete.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated  
        return request.user.is_authenticated and request.user.user_type == "seller"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user



class IsCustomerOrReadOnly(BasePermission):
    """
    - Everyone can READ (GET).
    - Customers can CREATE (POST).
    - Customers can UPDATE/DELETE their own ratings.
    - Sellers cannot modify.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.user_type == "customer"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

