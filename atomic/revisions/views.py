from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Revision
from projects.models import Project
from .serializers import RevisionSerializer
from atomic.modules import get_user_from_jwt_token


class RevisionsView(APIView):
    def get(self, request, uuid=None):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        if uuid:
            try:
                revision = Revision.objects.get(uuid=uuid)
            except ObjectDoesNotExist:
                return Response({'detail': 'Revision not found'}, status=status.HTTP_404_NOT_FOUND)

            if revision.user.company != user.company:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = RevisionSerializer(revision)
            return Response(serializer.data, status=status.HTTP_200_OK)

        revisions = Revision.objects.filter(user=user)
        serializer = RevisionSerializer(revisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            project_uuid = request.data['project']
            project = Project.objects.get(uuid=project_uuid)

            if project.creator.company != user.compnay:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        revision_data = request.data.copy()
        revision_data['user'] = user.uuid
        serializer = RevisionSerializer(data=revision_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Revision created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            revision = Revision.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Revision not found'}, status=status.HTTP_404_NOT_FOUND)

        if revision.user.company != user.company:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        revision.delete()
        return Response({'message': 'Revision deleted successfully'}, status=status.HTTP_200_OK)
