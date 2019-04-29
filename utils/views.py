from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import base64
import tempfile
# from django.shortcuts import render

# Create your views here.
class FileBase64Upload(GenericAPIView):
    def post(self, request):
        base64_string = request.data['file']
        base64_string = base64_string.replace('data:image/png;base64,', '')
        file_obj = base64.b64decode(base64_string)
        return Response({
            'status': 'success'
        }, status=status.HTTP_201_CREATED)
