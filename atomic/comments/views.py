from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atomic.modules import get_user_from_jwt_token
from comments.serializers import CommentSerializer
from revisions.models import Revision


class CommentsView(APIView):

    def post(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            revision_uuid = request.data['revision']
            revision = Revision.objects.get(uuid=revision_uuid)

            if revision.user.company != user.company:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            return Response({'detail': 'Revision not found'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'detail': 'Revision not found'}, status=status.HTTP_404_NOT_FOUND)

        comment_data = request.data.copy()
        comment_data['user'] = user.uuid

        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
