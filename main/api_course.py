# fetch_courses.py
from django.core.management.base import BaseCommand
import requests
from .models import FacultyCourse 

class Command(BaseCommand):
    help = 'Fetch faculty courses from external API and store in DB'

    def handle(self, *args, **kwargs):
        url = "https://bgnuerp.online/api/get_faculty_courses"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                count = 0
                for item in data:
                    obj, created = FacultyCourse.objects.update_or_create(
                        offer_id=item['offer_id'],
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
                self.stdout.write(self.style.SUCCESS(f"✅ {count} new courses fetched and saved."))
            else:
                self.stderr.write("❌ Failed to fetch data from API.")
        except Exception as e:
            self.stderr.write(f"❌ Error: {str(e)}")
