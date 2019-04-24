# -*- coding: utf-8 -*-
"""
ProgramEnrollment Views
"""
from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework.views import APIView


class ProgramEnrollmentsView(APIView):
    """
    POST view for ProgramEnrollments
    """

    def get(self, request, *args, **kwargs):
        return HttpResponse('result')