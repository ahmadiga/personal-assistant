from absence.models import Leave


def count_pending(request):
    leaves = Leave.objects.filter(status='PE').count()
    return {
        'count_pending': leaves,
    }
