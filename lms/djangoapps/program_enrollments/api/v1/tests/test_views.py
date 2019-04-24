"""
Unit tests for ProgramEnrollment views.
"""
from __future__ import unicode_literals

from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from lms.djangoapps.program_enrollments.models import ProgramEnrollment


class ProgramEnrollmentViewTests(APITestCase):
    """
    Tests for the ProgramEnrollment view.
    """

    def test_post(self):
        program_key = uuid4()
        curriculum_uuid = uuid4()
        self.url = reverse('programs_api:v1:program_enrollments', args=[program_key])

        response = self.client.post(self.url, {
            'external_user_key': 'abc',
            'status': 'pending',
            'curriculum_uuid': curriculum_uuid
        })

        enrollment =ProgramEnrollment.objects.first()
        actual_status = enrollment.status
        actual_program_uuid = enrollment.program_uuid
        actual_curriculum_uuid = enrollment.curriculum_uuid
        actual_external_user_key = enrollment.external_user_key

        self.assertEqual(response.status_code, 201)
        self.assertEqual(actual_status, 'pending')
        self.assertEqual(actual_program_uuid, program_key)
        self.assertEqual(actual_curriculum_uuid, curriculum_uuid)
        self.assertEqual(actual_external_user_key, 'abc')
