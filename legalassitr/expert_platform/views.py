from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Expert, Message, User
from django.shortcuts import get_object_or_404
from .serializers import ExpertSerializer, MessageSerializer, SubmitForExpertReviewSerializer

from doc_store.models import Document

class ExpertListCreateAPIView(generics.ListAPIView):
    """ Expert Registeration and List All Experts on the platform """
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpertDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return super().destroy()


class SubmitForExpertReview(APIView):
    def post(self, request):
        serializer = SubmitForExpertReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doc_id = serializer.validated_data['doc_id']
        selected_expert = serializer.validated_data['expert_id']

        document = Document.objects.get(pk=doc_id)
        selected_expert.assigned_docs.add(document)

        return Response({
            "message":f"Document with id: {doc_id} assigned to expert with id: {selected_expert}",
            "doc_id": doc_id,
            "expert_id": selected_expert,
        }, status = status.HTTP_201_CREATED)
        
    def get(self, request):
        serializer = SubmitForExpertReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doc_id = serializer.validated_data['doc_id']
        document = Document.objects.get(pk=doc_id)
        doc_status = document.status

        return Response({
            "message":f"Document with id: {doc_id} has status: {doc_status}",
            "doc_id": doc_id,
            "doc_status":doc_status,
        }, status = status.HTTP_200_OK)
        