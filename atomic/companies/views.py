from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from atomic.modules import get_user_from_jwt_token
from companies.models import Company
from companies.modules import create_company_from_request
from companies.serializers import CompanySerializer


class CompaniesView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        return Response(CompanySerializer(companies, many=True).data)

    def post(self, request):
        response_company, payload = create_company_from_request(request)
        if payload:
            return Response(response_company, status=payload)
        return Response(response_company, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = get_user_from_jwt_token(request.COOKIES.get('jwt'))

        try:
            company = Company.objects.get(uuid=request.data['uuid'])
        except KeyError:
            return Response({'detail': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'detail': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        if company != user.company:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
