from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ClassRoom, Assignment, Submission
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'roll_number', 'age', 'profile_picture']
class ClassRoomSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    students = UserSerializer(read_only=True, many=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'code', 'created_by', 'students']



class AssignmentSerializer(serializers.ModelSerializer):
    classroom = serializers.StringRelatedField(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(), write_only=True, source='classroom'
    )

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'file', 'created_at',
            'max_marks', 'min_words', 'required_keywords',
            'classroom', 'classroom_id','dead_line',
        ]



class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment = serializers.StringRelatedField(read_only=True)
    assignment_id = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all(), write_only=True, source='assignment'
    )
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'assignment_id', 'student', 'submitted_file',
            'submitted_at', 'marks', 'feedback','teacher_marks'
        ]
        #read_only_fields = ['submitted_at', 'marks', 'feedback']



# serializers.py
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'sent_time', 'read', 'classroom_id', 'assignment_id', 'type']