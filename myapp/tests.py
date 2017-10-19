# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

# Create your tests here.


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returned false for questions whose pub date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returned false for questions whose pub date
        is beyond 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        """
        was_published_recently() returned true for questions whose pub date
        is less than 1 day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        new_question = Question(pub_date=time)
        self.assertIs(new_question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returnd false for questions whose pub date
        is beyond 1 day.
        """
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the 
    given number of 'days' offset to now(negative for questions published 
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('myapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions with a pub date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_questions(self):
        """
        Questions with a pub date in the future aren't displayed on the
        index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        If both past and future questions exist, only past questions 
        should appear on the list.
        """
        create_question(question_text="Future question.", days=30)
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        multiple past questions exist, all past questions 
        should appear on the list.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-3)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail of a question with a pub date in the future return a 404.
        """
        future_question=create_question(question_text='Future question',days=5)
        url=reverse('myapp:detail',args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_questions(self):
        """
        The detail view of a question with a pub date in the past displays the 
        questions text.
        """
        past_question=create_question(question_text='Past question',days=-5)
        url=reverse('myapp:detail',args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response, past_question.)