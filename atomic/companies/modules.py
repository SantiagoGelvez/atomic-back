from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from companies.models import Company
from companies.serializers import CompanySerializer


def create_company_from_request(request):
    """
    Create company from request
    :param request:
    :return:
    Data or error, status
    """
    if request.data.get('company_name') is None:
        return {'detail': 'Name is required'}, status.HTTP_400_BAD_REQUEST

    try:
        name = request.data['company_name'].strip()
        company = Company.objects.get(name__iexact=name)
        return {'detail': f'Company {company.name} already exists'}, status.HTTP_400_BAD_REQUEST
    except ObjectDoesNotExist:
        pass

    company_data = {
        'name': request.data.get('company_name'),
        'description': request.data.get('description'),
        'website': request.data.get('website')
    }

    serializer = CompanySerializer(data=company_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return serializer.errors, status.HTTP_400_BAD_REQUEST
