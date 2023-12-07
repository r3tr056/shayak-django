import json

from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Document, DocumentContent
from .serializers import DocumentContentSerializer, DocumentSerializer
from .tasks import compress_document, convert_to_pdf, convert_to_word
from .search.search import rank_documents

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        compress_document(instance)

class DocumentContentViewSet(viewsets.ModelViewSet):
    queryset = DocumentContent.objects.all()
    serializer_class = DocumentContentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class DocumentSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        query = request.data.get('query', '')
        documents = DocumentContent.objects.filter(content__icontains=query)
        # Rank the obtained documents
        ranked_docs = rank_documents(query, documents)
        serializer = DocumentContentSerializer(rank_documents, many=True)
        return Response(serializer.data)
    
