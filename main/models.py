from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL 

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_classes'
    )
    students = models.ManyToManyField(
        User, related_name='joined_classes', blank=True
    )
    course = models.ForeignKey('FacultyCourse', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


class Assignment(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dead_line = models.DateTimeField(null=True,blank=True)
    
    max_marks = models.FloatField(default=10)
    min_words = models.PositiveIntegerField(default=30)
    required_keywords = models.JSONField(default=list, blank=True, help_text="List of keywords required in the submission.")

    def __str__(self):
        return f"{self.title} - {self.classroom.name}"

    class Meta:
        ordering = ['-created_at']


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submitted_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    teacher_marks = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"


# Note: The above code assumes that the User model is defined in the settings.AUTH_USER_MODEL.

class FacultyCourse(models.Model):
    offer_id = models.CharField(max_length=50, unique=True)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=255)
    program_name = models.CharField(max_length=255)
    shift_name = models.CharField(max_length=100)
    enc_offer_id = models.TextField() 

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    classroom_id = models.CharField(max_length=36, null=True, blank=True)  # UUID as string
    assignment_id = models.CharField(max_length=36, null=True, blank=True)  # UUID as string
    type = models.CharField(max_length=50, default='new_assignment')

    class Meta:
        ordering = ['-sent_time']

    def __str__(self):
        return f"{self.title} for {self.user.username}"