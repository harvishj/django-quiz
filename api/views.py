from django.template.response import TemplateResponse
from api.models import Question, QuizResult

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import jwt
import QuizApp.settings as settings
from .models import CustomUser, QuizQuestion
from django.contrib.auth.hashers import make_password
import datetime
from django.utils import timezone

# Create your views here.
class CreateAccount(APIView):
    '''
    This view is used to create an account for the user. The acceptable user types are 'admin' and 'normal'
    '''
    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            CustomUser.objects.create(
                username=serializer.validated_data['username'],
                password=make_password(serializer.validated_data['password']),
                user_type=serializer.validated_data['user_type'],
            )
            return Response(serializer.validated_data, status=201)
        return Response(serializer.errors, status=400)


class ScheduledQuizzes(APIView):
    '''
    This view is used to view the scheduled quizzes. All the scheduled quizzes are returned. 
    '''
    def get(self, request):
        
            scheduled_quizzes = Quiz.objects.all()
            serializer = QuizSerializer(scheduled_quizzes, many=True)

            return Response(serializer.data)

class AllQuestions(APIView):
    '''
    This view is used to view all the questions in the database. Only the users with 'admin' in token can access this
    '''
    def get(self, request):
        token = request.headers['Authorization'][7:]
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = CustomUser.objects.get(id=payload['user_id'])
        if user.user_type == 'admin':
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        else:
            return Response({'Error 403': 'You do not have the authority to add a quiz'}, status=403)

class ScheduleQuiz(APIView):
    '''
    This view is used to actually schedule the quiz. The quiz is scheduled for the time specified in the request.
    '''
    def post(self, request):
        serializer = ScheduleQuizSerializer(data=request.data)
        if serializer.is_valid():
            token = request.headers['Authorization'][7:]
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if user.user_type == 'admin':
                print(request.data)
                serializer.save()
                print(serializer.validated_data)
                return Response(serializer.validated_data, status=201)
            else:
                return Response({'Error 403': 'You do not have the authority to add a quiz'}, status=403)
        return Response(serializer.errors, status=400)



class AttemptQuiz(APIView):
    '''
    This view is used to attempt the quiz. Both admin and normal users can attempt the quiz.
    '''
    def post(self, request):

        token = request.headers['Authorization'][7:]
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])

        quiz_id = request.data['quiz_id']
        quiz_obj = Quiz.objects.get(quiz_id=quiz_id)
        start_time = quiz_obj.start_time
        length = quiz_obj.length_of_quiz_seconds

        end_time = start_time + datetime.timedelta(seconds=length)
        now = timezone.now()

        if now > end_time:
            return Response({'Error': 'Quiz has already ended'}, status=400)
        elif now < start_time:
            return Response({'Error': 'Quiz has not yet started'}, status=400)

        user_id = request.data['user_id']
        questions = request.data['questions']

        for i in range(1,len(questions)+1):
            question_id = request.data['questions'][str(i)]['question_id']
            answer = request.data['questions'][str(i)]['answer']

            QuizResult.objects.create(
                quiz_id= Quiz.objects.get(quiz_id=quiz_id),
                user_id=CustomUser.objects.get(id=user_id),
                question_id=Question.objects.get(uuid=question_id),
                answer=answer,
            )
        
        return Response({'Success': 'Quiz has been submitted'}, status=201)

class QuizView(APIView):
    '''
    This view is used to view the quiz. Admin will also get the answers while normal users will not.
    The questions are selected randomly.
    '''
    def get(self, request):
        quiz_id = request.data['quiz_id']
        quiz_obj = Quiz.objects.get(quiz_id=quiz_id)

        token = request.headers['Authorization'][7:]
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = CustomUser.objects.get(id=payload['user_id'])

        if user.user_type == 'admin':
            serializer = QuizSerializer(quiz_obj)
            print(serializer.data)
            domain = request.data['domain']
            questions = Question.objects.filter(domain=domain).order_by('?')

            question_serializer = QuestionSerializer(questions, many=True)

            response = {}
            response.update(serializer.data)
            response.update({'questions': question_serializer.data})


            return Response(response, status=200)
            
        elif user.user_type == 'normal':
            now = timezone.now()
            start_time = quiz_obj.start_time
            end_time = start_time + datetime.timedelta(seconds=quiz_obj.length_of_quiz_seconds)
            serializer = QuizSerializer(quiz_obj)
            if now > end_time:
                return Response({'Error': 'Quiz has already ended'}, status=400)
            elif now < start_time:
                return Response({'Error': 'Quiz has not yet started'}, status=400)
            else:
                # print(type(serializer.data))

                questions = Question.objects.filter(domain=quiz_obj.domain).order_by('?').only('question', 'option', 'image', 'domain')
                question_serializer = QuestionSerializer(questions, many=True)
                
                response = {}
                response.update(serializer.data)
                response.update({'questions': question_serializer.data})

                for i in questions:
                    QuizQuestion.objects.create(
                        quiz_id= Quiz.objects.get(quiz_id=quiz_id),
                        question_id = i
                    )

                return Response(response, status=200)

        return Response({'Error': 'Internal Server error'}, status=500)


class Results(APIView):
    '''
    This view can be used to view the results of a quiz.
    '''
    def get(self, request):
        
        username = request.data['user_id']
        result = QuizResult.objects.filter(user_id=username)
        serializer = ResultSerializer(result, many=True)
        return Response(serializer.data)


class AddQuestion(APIView):
    '''
    This view is used to add a question to the database.
    Only accessible by admin
    '''
    def post(self, request):

        token = request.headers['Authorization'][7:]
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = CustomUser.objects.get(id=payload['user_id'])

        if user.user_type == 'admin':
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Question Added successfully'}, status=201)    
            else:
                return Response({'Error' : 'Internal Server error'})

        elif user.user_type == 'normal':
            return Response({'Error': 'You do not have the authority to add a question'}, status=403)

        else:
            return Response({'Error': 'Internal Server error'}, status=500)

