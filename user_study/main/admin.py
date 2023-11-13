from django.contrib import admin
from main import models

@admin.action(description="Enable selected competitors")
def enable_competitors(modeladmin, request, queryset):
    queryset.update(available=True)

@admin.action(description="Disable selected competitors")
def disable_competitors(modeladmin, request, queryset):
    queryset.update(available=False)

class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'winner', 'available', 'images_count')
    list_filter = ('winner', 'available')
    actions = [enable_competitors, disable_competitors]

    def images_count(self, obj):
        return models.SampleImage.objects.filter(competitor=obj).count()
    images_count.short_description = 'Images'

    def questions_count(self, obj):
        a_count = models.Question.objects.filter(sample_a__competitor=obj).count()
        b_count = models.Question.objects.filter(sample_b__competitor=obj).count()
        return a_count + b_count

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


