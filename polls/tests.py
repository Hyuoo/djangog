from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

class QuestionListTest(APITestCase):
    '''
    시리얼라이저는 그냥 장고 테스트.
    API는 레스트 테스트.
    '''
    def setUp(self):
        self.question_data = {'question_text':'tt'}
        # 메서드 안에서는 reverse? 밖에선 lezy?
        self.url = reverse('question-list')

    def test_create_question(self):
        user = User.objects.create(username='testuser', password='testpwoord')
        # 로그인을 한 상태로 만드는
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.question_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertLess((timezone.now()-question.pub_date).total_seconds(), 1)

    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_questions(self):
        question = Question.objects.create(question_text='question1')
        question1 = Question.objects.create(question_text='question1')
        choice = Choice.objects.create(question=question, choice_text='choice1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        '''
        response.data
        [OrderedDict([('id', 1), ('question_text', 'question1'), ('pub_date', '2023-04-30T17:25:02.257836Z'), ('choices', [OrderedDict([('choice_text', 'choice1'), ('votes_count', 0)])])]), OrderedDict([('id', 2), ('question_text', 'question1'), ('pub_date', '2023-04-30T17:25:02.258835Z'), ('choices', [])])]
        '''
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)
        
class VoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testonly")
        self.question = Question.objects.create(question_text="abc",owner=self.user)
        self.choice = Choice.objects.create(question=self.question, choice_text="1")
        
    
    def test_vote_serializer(self):
        data = {
            'question':self.question.id,
            'choice':self.choice.id,
            'voter':self.user.id
            }
        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()

        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)
    
    def test_vote_serializer_with_duplicate_vote(self):
        choice1 = Choice.objects.create(question=self.question, choice_text="2")

        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)
        
        data = {
            'question':self.question.id,
            'choice':choice1.id,
            'voter':self.user.id
            }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_vote_serializer_with_unmatched_question_and_choice(self):
        question1 = Question.objects.create(question_text="abc",owner=self.user)
        choice1 = Choice.objects.create(question=question1, choice_text="2")
        data = {
            'question':self.question.id,
            'choice':choice1.id,
            'voter':self.user.id
            }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        

class QuestionSerializerTestCase(TestCase):
    # test_어쩌고만 실행된다.
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data = {"question_text":"asdf"})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data = {"question_text":""})
        self.assertEqual(serializer.is_valid(), False)

        