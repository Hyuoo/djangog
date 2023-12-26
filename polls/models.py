from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
# 모델 생성
# 모델을 테이블에 쓰기 위해 migration"을 만듦
# 모델에 맞는 테이블을 만ㄷ름
'''
간단한 설문에 답을 하는 페이지

Q : 휴가때 어디 놀러갈래?
Domain : 산, 강, 바다, 호캉스 ..
'''

'''
CREATE TABLE IF NOT EXISTS "polls_choice" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED
    );
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
'''
# class명은 상관없고 models.Model을 상속해야 함.
class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="질문")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)

    @admin.display(boolean=True, description="최근생성(하루기준)")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=2)

    # repr는 안되넹
    def __str__(self):
        if self.was_published_recently():
            new_badge = "NEW!! "
        else:
            new_badge = ""
        return f"{new_badge}제목: {self.question_text}, 날짜: {self.pub_date}"

'''
CREATE TABLE IF NOT EXISTS "polls_question" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "question_text" varchar(200) NOT NULL,
    "pub_date" datetime NOT NULL,
    "owner_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
    );
CREATE INDEX "polls_question_owner_id_0adad947" ON "polls_question" ("owner_id");
'''
# 질문 내용
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.question.question_text}]{self.choice_text}"

'''
CREATE TABLE IF NOT EXISTS "polls_vote" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "choice_id" bigint NOT NULL REFERENCES "polls_choice" ("id") DEFERRABLE INITIALLY DEFERRED,
    "question_id" bigint NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED,
    "voter_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "unique_voter_for_questions" UNIQUE ("question_id", "voter_id")
    );
CREATE INDEX "polls_vote_choice_id_17e8b17c" ON "polls_vote" ("choice_id");
CREATE INDEX "polls_vote_question_id_5ba63147" ON "polls_vote" ("question_id");
CREATE INDEX "polls_vote_voter_id_ef4603fe" ON "polls_vote" ("voter_id");
'''
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    # 얜 왜 메타가 생겼냥
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question','voter'], name='unique_voter_for_questions')
        ]