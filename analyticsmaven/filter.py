import django_filters
from .models import JobManagement

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = JobManagement
        fields = ('credit',)
