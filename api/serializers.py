from rest_framework import fields, serializers
from .models import Question, Quiz, CustomUser, QuizResult
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','user_type')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question', 'option', 'correct_index', 'image', 'domain')

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('uuid', 'image')

class QuizSerializer(serializers.ModelSerializer):

    # questions = serializers.SerializerMethodField('get_questions')

    class Meta:
        model = Quiz
        fields = ('quiz_id', 'name', 'start_time', 'length_of_quiz_seconds', 'domain')

    # def get_questions(self, obj):
    #     questions = QuestionSerializer(obj.questions.filter(domain=obj.domain), many=True).data
    #     return questions

class ScheduleQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('name', 'start_time', 'length_of_quiz_seconds', 'domain')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ('question_id', 'quiz_id', 'user_id', 'answer')