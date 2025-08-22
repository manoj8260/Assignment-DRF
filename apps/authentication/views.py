from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.serializers import (
    UserRegistrationSerializer,
    UserAuthenticationSerializer,
    UserLogoutSerilaizers
)


# User Registration View
class UserRegisterView(GenericAPIView):
    """
    Handles user registration.
    Accepts email, first_name, last_name, password, and user_type.
    """
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """Create a new user and return the user data with a message."""
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

     
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            return Response(
                {
                    'data': user,
                    'message': 'Hi, thanks for signing up!'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)



# User Login / Authentication View
class UserAuthenticateView(GenericAPIView):
    """
    Handles user login.
    Accepts email and password.
    Returns JWT access and refresh tokens and user details.
    """
    serializer_class = UserAuthenticationSerializer

    def post(self, request):
        """Authenticate user and return JWT tokens."""
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'message': "Login successfully",
                'user_details': serializer.data
            }
        )

# User Logout view
class UserLogoutView(GenericAPIView):
    """
    Handles user logout by blacklisting the refresh token.
    """
    serializer_class = UserLogoutSerilaizers

    def post(self, request):
        """Blacklist the refresh token to log out the user."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'message': 'Logout successfully!'
                }
            )
        return Response(serializer.error_messages)
