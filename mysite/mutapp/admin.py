from django.contrib import admin

# Register your models here.
from .models import Covid19metadata, SampleMutlist, MutSamplelist

admin.site.register(Covid19metadata)
admin.site.register(SampleMutlist)
admin.site.register(MutSamplelist)