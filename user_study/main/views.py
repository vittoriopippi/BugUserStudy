from django.shortcuts import render, redirect
import csv
import os
from django.http import JsonResponse, HttpResponse
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from main.models import Competitor, Prompt, SampleImage, Player, Answer, Question
from itertools import combinations
from pathlib import Path
import random
from datetime import timedelta, datetime
from django.conf import settings


def login(request):
    if request.POST:
        entered_username = request.POST['username']
        if entered_username is None or len(entered_username) == 0:
            return redirect('login')
        player = Player.objects.create(name=entered_username)
        request.session['player_id'] = player.pk
        return redirect('index')

    times = []
    for player in Player.objects.all():
        time_elps = player.time_delta()
        if time_elps is not None:
            times.append(time_elps.total_seconds())
    avg_time = sorted(times)[len(times) // 2] if len(times) > 0 else 'N/A'
    if avg_time != 'N/A':
        avg_time = str(timedelta(seconds=avg_time)).split('.')[0]
    return render(request, 'main/login.html', {'avg_time': avg_time})

def index(request):
    player_id = request.session.get('player_id')
    if player_id is None or not Player.objects.filter(pk=player_id).exists():
        return redirect('login')

    player = Player.objects.get(pk=player_id)
    answered_questions = Answer.objects.all().filter(player=player, question__is_control=False).count() 
    if answered_questions >= settings.QUESTIONS_PER_PLAYER:
        return redirect('login')

    control_questions = Question.objects.all().filter(is_control=True).order_by('pk')
    control_questions_answered = Answer.objects.all().filter(player=player, question__is_control=True)
    for question in control_questions_answered:
        control_questions = control_questions.exclude(pk=question.question.pk)
    control_questions = list(control_questions)

    other_questions = list(Question.objects.all().filter(is_control=False))
    random.shuffle(other_questions)
    questions = control_questions + other_questions[:settings.QUESTIONS_PER_PLAYER - answered_questions]

    first_question = questions[0]
    context = {
        'player': player,
        'first_question': first_question,
        'questions': questions,
        'total_questions': len(control_questions) + settings.QUESTIONS_PER_PLAYER,
        'answered_questions': answered_questions,
        }
    return render(request, 'main/index.html', context)

def scoreboard(request):
    players = Player.objects.all().filter(visible=True).order_by('-accuracy')
    context = {
        'players': players,
        }
    return render(request, 'main/scoreboard.html', context)

@csrf_exempt
def post_answer(request):
    if request.POST:
        player_id = request.POST['player_id']
        if player_id is None or not Player.objects.filter(pk=player_id).exists():
            return HttpResponse('ERROR')
        player = Player.objects.get(pk=player_id)
        question_id = request.POST['question_id']
        if question_id is None or not Question.objects.filter(pk=question_id).exists():
            return HttpResponse('ERROR')
        question = Question.objects.get(pk=request.POST['question_id'])
        winner = question.sample_a if request.POST['answer'] == 'img_a' else question.sample_b
        Answer.objects.create(player=player, winner=winner, question=question)
        player.accuracy = player._accuracy()
        player.save()

        answered_questions = Answer.objects.all().filter(player=player, question__is_control=False).count() 
        remaining_questions = settings.QUESTIONS_PER_PLAYER - answered_questions
        return JsonResponse({'status': 'OK', 'remaining_questions': remaining_questions})
    return HttpResponse('ERROR')

@staff_member_required
def import_images(request):
    Competitor.objects.all().delete()
    # if linux server
    if os.name == 'nt':
        root = Path(r'D:\Work\Projects\BugUserStudy\images')
    else:
        root = Path('/home/vpippi/BugUserStudy/images')

    for img_path in root.rglob('*'):
        if not img_path.is_file() and not img_path.suffix in ('.png', '.jpg'):
            continue
        img_path = Path(img_path)
        competitor_name = img_path.parent.parent.name
        prompt_text = img_path.parent.name.replace('_', ' ')
        competitor, _ = Competitor.objects.get_or_create(name=competitor_name)
        prompt, _ = Prompt.objects.get_or_create(eng_text=prompt_text)
        with img_path.open(mode='rb') as f:
            SampleImage.objects.create(competitor=competitor, prompt=prompt, img=File(f, name=img_path.name))
    return HttpResponse(f'Imported {len(SampleImage.objects.all())} images')

@staff_member_required 
def generate_questions(request):
    Question.objects.all().filter(is_control=False).delete()
    competitors = Competitor.objects.all().filter(available=True)
    prompts = Prompt.objects.all()
    for competitor_a, competitor_b in combinations(competitors, 2):
        for prompt in prompts:
            for _ in range(settings.QUESTIONS_PER_PAIR):
                sample_a = SampleImage.objects.all().filter(competitor=competitor_a, prompt=prompt, exclude_from_study=False).order_by("?").first()
                sample_b = SampleImage.objects.all().filter(competitor=competitor_b, prompt=prompt, exclude_from_study=False).order_by("?").first()
                sample_a, sample_b = (sample_a, sample_b) if random.random() > 0.5 else (sample_b, sample_a)
                Question.objects.create(sample_a=sample_a, sample_b=sample_b, is_control=False)
    return HttpResponse(f'Generated {len(Question.objects.all())} questions')

@staff_member_required 
def dump_answers(request):
    now = datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="dump_{now_str}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["player", "is_control", "img_a", "img_b", "competitor_a", "competitor_b", "prompt", "winner"])
    for answer in Answer.objects.all():
        writer.writerow([
            answer.player.name,
            answer.question.is_control,
            answer.question.sample_a.img.url,
            answer.question.sample_b.img.url,
            answer.question.sample_a.competitor.name,
            answer.question.sample_b.competitor.name,
            answer.question.sample_a.prompt.eng_text,
            answer.winner.competitor.name
        ])
    return response

@staff_member_required
def update_accuracy(request):
    for player in Player.objects.all():
        player.accuracy = player._accuracy()
        player.save()
    return redirect('scoreboard')
