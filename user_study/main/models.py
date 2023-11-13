from django.db import models
from pathlib import Path
import random


class Competitor(models.Model):
    name = models.CharField(max_length=100)
    winner = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Prompt(models.Model):
    eng_text = models.CharField(max_length=100, unique=True)
    ita_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.eng_text
    
def content_file_name(instance, filename):
    filename = Path(filename)
    prompt = instance.prompt.eng_text.replace(' ', '_')
    rand_id = '%06x' % random.randrange(16**6)
    return Path() / instance.competitor.name / prompt / f'{rand_id}{filename.suffix}'

class SampleImage(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=content_file_name)

class Player(models.Model):
    name = models.CharField(max_length=100)
    accuracy = models.FloatField(default=0)

    def _accuracy(self):
        answers_count = Answer.objects.filter(player=self).filter(winner__competitor__winner=True, question__is_control=False).count()
        questions_count = Question.objects.filter(is_control=False).count()
        if questions_count == 0:
            return 0
        return answers_count / questions_count * 100

    def username(self):
        return self.name.replace('_', ' ') + f'#{self.pk:03d}'

class Question(models.Model):
    sample_a = models.ForeignKey(SampleImage, on_delete=models.CASCADE, related_name='sample_a')
    sample_b = models.ForeignKey(SampleImage, on_delete=models.CASCADE, related_name='sample_b')
    is_control = models.BooleanField(default=False)

class Answer(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    winner = models.ForeignKey(SampleImage, on_delete=models.CASCADE, related_name='winner', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)