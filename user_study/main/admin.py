from django.contrib import admin
from main import models

@admin.action(description="Enable selected competitors")
def enable_competitors(modeladmin, request, queryset):
    queryset.update(available=True)

@admin.action(description="Disable selected competitors")
def disable_competitors(modeladmin, request, queryset):
    queryset.update(available=False)

class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'winner', 'available', 'images_count', 'questions_count', 'images_sizes')
    list_filter = ('winner', 'available')
    actions = [enable_competitors, disable_competitors]

    def images_count(self, obj):
        return models.SampleImage.objects.filter(competitor=obj).count()
    images_count.short_description = 'Images'

    def questions_count(self, obj):
        a_count = models.Question.objects.filter(sample_a__competitor=obj).count()
        b_count = models.Question.objects.filter(sample_b__competitor=obj).count()
        return a_count + b_count
    questions_count.short_description = 'Questions'
    
    def images_sizes(self, obj):
        return models.SampleImage.objects.filter(competitor=obj).first().width
    images_sizes.short_description = 'Sizes'

class SampleImageAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'prompt', 'img', 'exclude_from_study')
    list_filter = ('competitor', 'prompt', 'exclude_from_study')

class PromptAdmin(admin.ModelAdmin):
    list_display = ('eng_text', 'ita_text')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('sample_a', 'sample_b', 'is_control')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('date', 'player', 'winner', 'question')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'accuracy', 'answers_count', 'correct_control_answers', 'time_delta', 'finished')

    def answers_count(self, obj):
        return models.Answer.objects.filter(player=obj).count()
    answers_count.short_description = 'Answers'

    def correct_control_answers(self, obj):
        return models.Answer.objects.filter(player=obj, question__is_control=True, winner__competitor__winner=True).count()
    correct_control_answers.short_description = 'Correct control answers'


admin.site.register(models.Competitor, CompetitorAdmin)
admin.site.register(models.SampleImage, SampleImageAdmin)
admin.site.register(models.Prompt, PromptAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.Player, PlayerAdmin)


