from django.contrib import admin
from .models import Summary, Question, Feedback

# Register your models here.
admin.site.register(Summary)
admin.site.register(Question)
admin.site.register(Feedback)