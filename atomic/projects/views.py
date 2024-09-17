from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from revisions.serializers import RevisionSerializer
from .models import Project
from .serializers import ProjectSerializer
from atomic.modules import get_user_from_jwt_token


class ProjectsView(APIView):
    def get(self, request, uuid=None):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        if uuid:
            try:
                project = Project.objects.get(uuid=uuid)
            except ObjectDoesNotExist:
                return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

            if project.creator.company != user.company:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        projects = Project.objects.filter(creator__company=user.company)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        project_data = request.data.copy()
        serializer = ProjectSerializer(data=project_data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            project = Project.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if project.creator != user:
            return Response({'v': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Project updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            project = Project.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if project.creator != user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        project.delete()
        return Response({'message': 'Project deleted successfully'}, status=status.HTTP_200_OK)


class ProjectRevisionsView(APIView):
    def get(self, request, uuid):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            project = Project.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if project.creator.company != user.company:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        revisions = project.revision_set.all()
        serializer = RevisionSerializer(revisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            project = Project.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if project.creator.company != user.company:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        file = request.FILES.get('file')

        if not file:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        file_extension = file.name.split('.')[-1]

        validated_data = {
            'file_extension': file_extension,
            'file_s3_key': file,
            'attempt': project.revision_set.count() + 1,
        }

        context = {
            'request': request,
            'project': project.uuid,
            'user': user.uuid,
        }

        serializer = RevisionSerializer(data=validated_data, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
