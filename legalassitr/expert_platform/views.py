from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Expert, Message, User
from django.shortcuts import get_object_or_404
from .serializers import ExpertSerializer, MessageSerializer
from .doc_select import select_expert_for_document
from doc_store.models import Document


class ExpertListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class ExpertDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class SubmitForExpertReview(APIView):
    def post(self, request):
        doc_id = request.data.get("doc_id")
        expert_id = request.data.get("expert_id",None)

        if doc_id is None:
            return Response({"message":f"Document with id: {doc_id} does not exist"},status = status.HTTP_404_NOT_FOUND)
        
        if expert_id is None:
            selected_expert = select_expert_for_document(doc_id)
        else:
            selected_expert = Expert.objects.get(pk=expert_id)
        
        document = Document.objects.get(pk=doc_id)
        selected_expert.assigned_docs.add(document)

        return Response({
            "message":f"Document with id: {doc_id} assigned to expert with id: {expert_id}",
            "doc_id": doc_id,
            "expert_id": expert_id,
        }, status = status.HTTP_201_CREATED)
        
    def get(self, request):
        doc_id = request.data.get("doc_id")
        if doc_id is None:
            return Response({"message":f"Document with id: {doc_id} does not exist"},status = status.HTTP_404_NOT_FOUND)
        try:
            document = Document.objects.get(pk=doc_id)
            doc_status = document.status
            return Response({
                "message":f"Document with id: {doc_id} has status: {doc_status}",
                "doc_id": doc_id,
                "doc_status":doc_status,
            }, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":f"Document with id: {doc_id} does not exist"},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SendMessage(APIView):
    def post(self, request):
        sender_id = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')
        message_content = request.data.get('message')

        sender = get_object_or_404(User, pk=sender_id)
        receiver = get_object_or_404(User, pk=receiver_id)

        message = Message.objects.create(sender=sender, receiver=receiver, content=message_content)
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetMessages(APIView):
    def get(self, request, sender_id, receiver_id):
        sender = get_object_or_404(User, pk=sender_id)
        receiver = get_object_or_404(User, pk=receiver_id)
        
        messages = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        serializer = MessageSerializer(messages, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
