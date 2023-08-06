# Create your views here.
import copy

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.decorators import schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.schemas import SchemaGenerator
from rest_framework import generics, status
from django.http import HttpRequest
from framework.response import RspError, RspStruct

from myadmin.models import User
from framework.serializer import IdSerializer
from rest_framework.exceptions import APIException
from framework.views import notauth, api_view, CurdViewSet, action
from framework.route import Route
from framework.serializer import ParamsSerializer, IdsSerializer

from rest_framework.schemas import ManualSchema, AutoSchema
import coreapi
import coreschema
from drf_yasg.utils import swagger_auto_schema





