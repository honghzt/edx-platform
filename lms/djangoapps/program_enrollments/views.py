# -*- coding: utf-8 -*-
"""
ProgramEnrollment Views
"""
from __future__ import unicode_literals

from django.http import Http404

from common.djangoapps.course_modes.models import CourseMode
from common.djangoapps.student.models import CourseEnrollment
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_202_ACCEPTED,
    HTTP_207_MULTI_STATUS,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from openedx.core.djangoapps.catalog.utils import get_programs
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

from program_enrollments.constants import ResponseStatuses
from program_enrollments.models import ProgramEnrollment, ProgramCourseEnrollment
from program_enrollments.serializers import ProgramCourseEnrollmentRequestSerializer
from program_enrollments.utils import get_user_by_organization, ProviderDoesNotExistException


# from django.shortcuts import render

# Create your views here.


class ProgramSpecificViewMixin(object):
    """
    A mixin for views that operate on or within a specific program.
    """

    @property
    def program(self):       
        """
        The program specified by the `program_key` URL parameter.
        """
        if self._program is None:
            program = get_programs(self.kwargs['program_key'])
            if program is None:
                raise Http404()
            self._program = program
        return self._program


class ProgramCourseSpecificViewMixin(ProgramSpecificViewMixin):
    """
    A mixin for views that operate on or within a specific course in a program
    """

    def check_existance_and_membership(self):
        """ 
        Attempting to look up the course and program will trigger 404 responses if:
        - The program does not exist
        - The course run (course_key) does not exist
        - The course run is not part of the program
        """
        self.course  # pylint: disable=pointless-statement

    @property
    def course(self):
        """
        The course specified by the `course_id` URL parameter.
        """
        if self._course is None:
            try:
                course = CourseOverview.get_from_id(self.kwargs['course_id'])
            except CourseOverview.DoesNotExist:
                raise Http404()
            if course not in self.program["courses"]:
                raise Http404()
            self._course = course
        return self._course


class ProgramCourseEnrollmentView(APIView, ProgramCourseSpecificViewMixin):
    """
    A view for enrolling students in a course through a program, 
    modifying program course enrollments, and listing program course 
    enrollments

    Path: /api/v1/programs/{program_key}/courses/{course_id}/enrollments

    Accepts: [POST]

    ------------------------------------------------------------------------------------
    POST 
    ------------------------------------------------------------------------------------

    Returns:
     * 200: Returns a map of students and their enrollment status.
     * 207: Not all students enrolled. Returns resulting enrollment status.
     * 401: User is not authenticated
     * 403: User lacks read access organization of specified program.
     * 404: Program does not exist, or course does not exist in program
     * 422: Invalid request, unable to enroll students.
    """
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Enroll a list of students in a course in a program
        """
        self.check_existance_and_membership()
        results = {}
        seen_student_keys = set()
        enrollments = []

        for enrollment in request.data:
            if 'student_key' not in enrollment:
                return Response('student key required', HTTP_422_UNPROCESSABLE_ENTITY) 
            student_key = enrollment['student_key']
            if student_key in seen_student_keys:
                results[student_key] = ResponseStatuses.DUPLICATED
                continue
            enrollment_serializer = ProgramCourseEnrollmentRequestSerializer(enrollment)
            if enrollment_serializer.is_valid():
                enrollments.append(enrollment)
            elif enrollment_serializer.has_invalid_status():
                results[student_key] = ResponseStatuses.INVALID_STATUS
            else:
                return Response('invalid enrollment record', HTTP_422_UNPROCESSABLE_ENTITY)

        program_enrollments = self.get_existing_program_enrollments(enrollments)
        for enrollment in enrollments:
            results[student_key] = self.enroll_learner_in_course(enrollment, program_enrollments)
        
        enrolled_students = sum([1 for k, v in results.items() if v not in ResponseStatuses.ERROR_STATUSES])
        if not enrolled_students:
            return Response(results, HTTP_422_UNPROCESSABLE_ENTITY)
        if enrolled_students != len(results):
            return Response(results, HTTP_207_MULTI_STATUS)
        else:
            return Response(results)

    def enroll_learner_in_course(enrollment, program_enrollments):
        student_key = enrollment['student_key']
        try:
            program_enrollment = program_enrollments[student_key]
        except KeyError:
            return ResponseStatuses.NOT_IN_PROGRAM
        if program_enrollment.get_program_course_enrollment(self.course):
            return ResponseStatuses.CONFLICT                    

        status = enrollment['status']
        course_enrollment = None
        if program_enrollment.user:
            course_enrollment = CourseEnrollment.enroll(
                program_enrollment.user,
                self.course,
                mode=CourseMode.MASTERS,
                check_access=True,
            )
            if status = ResponseStatuses.INACTIVE:
                course_enrollment.deactivate()

        ProgramCourseEnrollment.objects.create(
            program_enrollment=program_enrollment,
            course_enrollment=course_enrollment,
            course_key=self.course,
            status=status,
        )
        return status


    def get_existing_program_enrollments(self, enrollments):
        external_user_keys = enrollments.map(lambda e: e['student_key'])
        existing_enrollments = ProgramEnrollment.objects.filter(external_user_key__in=external_user_keys)
        existing_enrollments = existing_enrollments.select_related('program_course_enrollment')
        return existing_enrollments.in_bulk(enrollments, field_name)

            
            
            
            





