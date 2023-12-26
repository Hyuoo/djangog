from rest_framework import serializers
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator


class VoteSerializer(serializers.ModelSerializer):
    # voter = serializers.ReadOnlyField(source='voter.username')

    def validate(self, attrs):
        if attrs['choice'].question_id != attrs['question'].id:
            raise serializers.ValidationError("Question의 inValid한 Choice..")
        return attrs
    
    class Meta:
        model = Vote
        fields = ['id', 'question', 'choice', 'voter']
        validators = [
            UniqueTogetherValidator(
                queryset = Vote.objects.all(),
                fields = ['question','voter']
            )
        ]

class ChoiceSerializer(serializers.ModelSerializer):
    # Method에 의해 필드값 정의
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['choice_text', 'votes_count']
    
    def get_votes_count(self, obj):
        return obj.vote_set.count()

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'owner', 'choices']

class UserSerializer(serializers.ModelSerializer):
    # question을 갖고오는건 User테이블에서만 할 수 가 없 다
    # questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #queryset=Question.objects.all())
    # questions = serializers.StringRelatedField(many=True, read_only=True)
    # questions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pub_date')
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="question-detail")

    class Meta:
        model = User
        fields = ['id', 'username', 'questions']

class RegisterSearializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_check = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username','password','password_check']