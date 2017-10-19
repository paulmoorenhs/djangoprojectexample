# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
print "\n".join(sys.path)
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from myapp.models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last 5 published questions (not including those set to be
        published in the future)
        """

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'myapp/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myapp/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "you didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return anHttpResponseRedirect after successfully dealing
        # with POST data.This prevents data from being posted twice if a
        # user hits the back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))
