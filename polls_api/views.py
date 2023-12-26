#from rest_framework.decorators import api_view
#from rest_framework.response import Response
#from rest_framework import status, mixins
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsVoter
#from rest_framework.views import APIView
from polls.models import Question
#from django.contrib.auth.models import User
from polls_api.serializers import *
from django.shortcuts import get_object_or_404

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)
    
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save(voter=self.request.user)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)

# @api_view(['GET', 'POST'])
# def question_list(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        #return super().perform_create(serializer)
    
    # def get(self, request, *args, **kwargs):
    #     # questions = Question.objects.all()
    #     # serializer = QuestionSerializer(questions, many=True)
    #     # return Response(serializer.data)
    #     return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     # serializer = QuestionSerializer(data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return self.create(request, *args, **kwargs)

# @api_view(['GET', 'PUT', 'DELETE'])
# def question_detail(request, id):
#     question = get_object_or_404(Question, pk=id)

#     if request.method=='GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method=='DELETE':
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # def get(self, request, *args, **kwargs):
    #     # question = get_object_or_404(Question, pk=id)
    #     # serializer = QuestionSerializer(question)
    #     # return Response(serializer.data)
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     # question = get_object_or_404(Question, pk=id)
    #     # serializer = QuestionSerializer(question, data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data, status=status.HTTP_200_OK)
    #     # else:
    #     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return self.update(request, *args, **kwargs)
        
    # def delete(self, request, *args, **kwargs):
    #     # question = get_object_or_404(Question, pk=id)
    #     # question.delete()
    #     # return Response(status=status.HTTP_204_NO_CONTENT)
    #     return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSearializer