""" Program Enrollments API v1 URLs. """
from django.conf import settings
from django.conf.urls import url

from lms.djangoapps.program_enrollments.api.v1.views import ProgramEnrollmentsView


app_name = 'lms.djangoapps.program_enrollments'

urlpatterns = [
    url(
        r'^programs/{program_key}/enrollments/$'.format(program_key=r'.*'),
        ProgramEnrollmentsView.as_view(),
        name='course_grades'
    ),
]
