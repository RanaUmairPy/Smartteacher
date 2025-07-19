from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
import requests
from .models import FacultyCourse,Assignment


admin.site.register(Assignment)
class FacultyCourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_title', 'program_name', 'shift_name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('2022/', self.admin_site.admin_view(self.fetch_courses_view), name='fetch_courses'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        # ✅ Inject the button HTML directly
        extra_context['title'] = "Faculty Courses"
        extra_context['custom_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def fetch_courses_view(self, request):
        try:
            response = requests.get("https://bgnuerp.online/api/get_faculty_courses")
            if response.status_code == 200:
                data = response.json()
                count = 0
                for item in data:
                   obj, created = FacultyCourse.objects.update_or_create(
                    offer_id=item['offer_id'],  # use this to prevent duplicates
                        defaults={
                                'course_code': item['course_code'],
                                'course_title': item['course_title'],
                                'program_name': item['program_name'],
                                'shift_name': item['shift_name'],
                                'enc_offer_id': item['enc_offer_id'],
                            }
                        )
                if created:
                        count += 1
                self.message_user(request, f"✅ {count} new courses fetched and stored.")
            else:
                self.message_user(request, "❌ API response error.", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"❌ Error: {e}", level=messages.ERROR)

        return redirect('admin:main_facultycourse_changelist')

admin.site.register(FacultyCourse, FacultyCourseAdmin)


# admin.py

from django.contrib import admin
from .models import ClassRoom, FacultyCourse
from .forms import ClassRoomAdminForm

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    form = ClassRoomAdminForm
    list_display = ['name', 'code', 'created_by', 'course']
    filter_horizontal = ['students']  # optional

