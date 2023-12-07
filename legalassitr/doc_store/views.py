import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.responses import Response

from .models import Document

class DocumentViewSet():

    def put(self, request):
        doc_id = request.data.get("doc_id", None)
        if doc_id is not None:
            content = request.data.get("content", None)
            doc = Document.objects.get(pk=self.doc_id)
            doc.content = content
            doc.save()
        return Response({'message': 'Error occured while updating content'})

# class RollbackDocumentChanges(APIView):
#     def post(self, request):
#         data = json.loads(request)
#         content = data.get('content', None)
#         is_expert = data.get('is_expert', False)

#         if is_expert:
#             return Response({'success':  True})

#         return Response({'success': False, 'message': 'Normal users cannot rollback changes to document'})