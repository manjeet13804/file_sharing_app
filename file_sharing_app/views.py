from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import File
from .serializers import UserSerializer, FileSerializer
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import ClientUserProfile
from .serializers import UserSerializer, ClientUserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='Ops').exists():
            file = serializer.save(user=user)
        else:
            raise PermissionDenied("Only Ops users can upload files.")

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        file = self.get_object()
        # Implement file download logic and return the file response.
        # You can generate a secure URL for file download here.



class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        user_profile = ClientUserProfile(user=user)
        user_profile.save()
        
        # Send email verification link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        verification_url = reverse('verify-email', args=[uid, token])
        verification_link = request.build_absolute_uri(verification_url)
        send_mail(
            'Email Verification',
            f'Click the following link to verify your email: {verification_link}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Sign up successful'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

class ClientUserProfileViewSet(viewsets.ModelViewSet):
    queryset = ClientUserProfile.objects.all()
    serializer_class = ClientUserProfileSerializer

    @action(detail=False, methods=['GET'])
    def list_uploaded_files(self, request):
        user = request.user
        if user.is_authenticated:
            # Implement logic to list uploaded files associated with the client user.
            # You can use the File model from the previous answer to do this.
            # Return the list of files.
        else:
            raise PermissionDenied("Authentication required.")

    @action(detail=True, methods=['GET'])
    def verify_email(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user_profile = ClientUserProfile.objects.get(user=user)
            user_profile.email_verified = True
            user_profile.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)
