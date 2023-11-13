from django.contrib import admin
from main import models

class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'winner', 'available', 'images_count')
    list_filter = ('winner', 'available')

    def images_count(self, obj):
        return models.SampleImage.objects.filter(competitor=obj).count()
    images_count.short_description = 'Images'

class SampleImageAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'prompt', 'img')

class PromptAdmin(admin.ModelAdmin):
    list_display = ('eng_text', 'ita_text')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('sample_a', 'sample_b', 'is_control')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('date', 'player', 'winner', 'question')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'accuracy', 'answers_count')

    def answers_count(self, obj):
        return models.Answer.objects.filter(player=obj).count()
    answers_count.short_description = 'Answers'


admin.site.register(models.Competitor, CompetitorAdmin)
admin.site.register(models.SampleImage, SampleImageAdmin)
admin.site.register(models.Prompt, PromptAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)


