from rest_framework import serializers

class InvalidStatusMixin(object):

    def has_invalid_status(self):
        return 'status' in enrollee_serializer.errors and \
                enrollee_serializer.errors['status'][0].code == 'invalid_choice'


class ProgramCourseEnrollmentRequestSerializer(serializers.Serializer, InvalidStatusMixin):
    """
    Serializer for request to create a ProgramCourseEnrollment
    """
    STATUS_CHOICES = ['pending', 'enrolled']

    student_key = serializers.CharField(allow_blank=False)
    status = serializers.ChoiceField(allow_blank=False, choices=STATUS_CHOICES)


#potentially serialize program course enrollments
