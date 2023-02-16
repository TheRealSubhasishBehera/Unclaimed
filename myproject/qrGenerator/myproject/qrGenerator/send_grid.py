from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from rest_framework import generics, status
from rest_framework.response import Response
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class SendEmailView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        # Get the email data from the request data
        to = request.data.get('to')
        subject = request.data.get('subject')
        message = request.data.get('message')

        # Validate the email addresses
        try:
            validate_email(to)
        except ValidationError:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate with Google
        credentials = Credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=['https://www.googleapis.com/auth/gmail.send'])
        service = build('gmail', 'v1', credentials=credentials)

        # Build the email message
        email_message = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [to])
        email_message.attach_alternative(message, "text/html")
        message_bytes = email_message.message().as_bytes()

        try:
            message = service.users().messages().send(userId="me", body={'raw': message_bytes.decode('utf-8')}).execute()
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_201_CREATED)
        except HttpError as error:
            print(f'An error occurred: {error}')
            return Response({'error': 'An error occurred while sending the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
