from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
import json

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    context = {'questions': latest_question_list}

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question':question, 'error_msg': f"선택이 없습니다. id={request.POST.get('choice')}"})
    else:
        #selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question':question})

def asdf(request):
    return HttpResponse("<h1>뭘봐</h1>")


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    # reverse_lazy -> name기반 url 만드는
    success_url = reverse_lazy('user-list')
    template_name = 'registration/signup.html'