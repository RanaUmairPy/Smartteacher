# notifications.py
from django.conf import settings
from django.contrib.auth import get_user_model
from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError
from .models import Notification
from django.utils import timezone

# Initialize OneSignal client
onesignal_client = Client(
    app_id="63d0bf46-da85-4900-9f15-e024d9a47458",
    rest_api_key="os_v2_app_mpil6rw2qveqbhyv4asntjdulajb7ctihzwectvynhv43tdrv5jtrdye6rnsc6joo7insdn5ydnagisuqicdybgd3clexyzxsevjiby"
)

def send_assignment_notification(classroom, assignment):
    """
    Send a push notification to all students in the classroom and store it in the database.

    Args:
        classroom: ClassRoom instance
        assignment: Assignment instance
    """
    try:
        # Get all students in the classroom
        students = classroom.students.all()
        if not students.exists():
            print(f"[OneSignal] No students found in classroom {classroom.name}")
            return

        # Collect player IDs and store notifications
        player_ids = []
        User = get_user_model()
        for student in students:
            if hasattr(student, 'onesignal_player_id') and student.onesignal_player_id:
                player_ids.append(student.onesignal_player_id)
                # Store notification in the database
                Notification.objects.create(
                    user=student,
                    title="New Assignment Notification",
                    body=f"New assignment '{assignment.title}' added in {classroom.name}",
                    classroom_id=str(classroom.id),
                    assignment_id=str(assignment.id),
                    type="new_assignment",
                    sent_time=timezone.now()
                )
                print(f"[Database] Notification stored for {student.username}")
            else:
                print(f"[OneSignal] No valid player_id for student {student.username}")

        if not player_ids:
            print(f"[OneSignal] No valid player IDs found for classroom {classroom.name}")
            return

        # Create notification payload
        notification = {
            "app_id": "63d0bf46-da85-4900-9f15-e024d9a47458",
            "include_player_ids": player_ids,
            "headings": {"en": "New Assignment Notification"},
            "contents": {"en": f"New assignment '{assignment.title}' added in {classroom.name}"},
            "data": {
                "classroom_id": str(classroom.id),
                "assignment_id": str(assignment.id),
                "type": "new_assignment"
            },
            "ios_badge_type": "Increase",
            "ios_badge_count": 1
        }

        # Send the notification
        response = onesignal_client.send_notification(notification)
        print(f"[OneSignal] Notification sent successfully: {response}")

    except OneSignalHTTPError as e:
        print(f"[OneSignal] Failed to send notification: Status {e.status_code}, Response: {e}")
        print(f"[OneSignal] Response body: {e.http_response.json() if e.http_response else 'No response body'}")
    except Exception as e:
        print(f"[OneSignal] Error sending notification: {e}")