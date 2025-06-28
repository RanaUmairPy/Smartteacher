# forms.py

from django import forms
from .models import ClassRoom, FacultyCourse
from django.contrib.auth import get_user_model

User = get_user_model()

class ClassRoomAdminForm(forms.ModelForm):
    selected_course = forms.ModelChoiceField(
        queryset=FacultyCourse.objects.all(),
        label="Select Course"
    )
    selected_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select Teacher"
    )
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Add Students"
    )

    class Meta:
        model = ClassRoom
        fields = ['selected_course', 'selected_user', 'students']

    def save(self, commit=True):
        classroom = super().save(commit=False)

        # Set name and code from the selected course
        course = self.cleaned_data['selected_course']
        classroom.name = course.course_title
        classroom.code = course.course_code
        classroom.course = course

        # Set the teacher
        classroom.created_by = self.cleaned_data['selected_user']

        if commit:
            classroom.save()
            self.save_m2m()
            classroom.students.set(self.cleaned_data['students'])

        return classroom
