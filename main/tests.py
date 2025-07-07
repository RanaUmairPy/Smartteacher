from .models import Submission

sub = Submission.objects.filter(
    assignment__classroom__students__id=1,
    status='submitted'
)
print(sub)