from django.contrib import admin
from .models import *

admin.site.register(BlogTags)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Replay)

# Register your models here.
