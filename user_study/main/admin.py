from django.contrib import admin
from main import models

admin.site.register(models.Competitor)
admin.site.register(models.Prompt)
admin.site.register(models.SampleImage)
admin.site.register(models.Player)
admin.site.register(models.Answer)
admin.site.register(models.Question)

