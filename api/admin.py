from django.contrib import admin
from .models import *
# from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizResult)
