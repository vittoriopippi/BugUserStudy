from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("scoreboard", views.scoreboard, name="scoreboard"),
    path("post_answer", views.post_answer, name="post_answer"),
    path("import_images", views.import_images, name="import_images"),
    path("generate_questions", views.generate_questions, name="generate_questions"),
    path("dump_answers", views.dump_answers, name="dump_answers"),
]