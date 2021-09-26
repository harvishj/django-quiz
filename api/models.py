from enum import unique
from api.managers import CustomUserManager
from django.db import models
from django.db.models.deletion import CASCADE
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
import jwt
import datetime
import QuizApp.settings as settings
from django.utils.translation import ugettext_lazy as _



# Create your models here.
class CustomUser(AbstractUser):
    email = None
    username = models.CharField(db_index=True, max_length=100, unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20)

    is_staff = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'user_type']

    objects = CustomUserManager()

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 1 hour into the future.
        """
        dt = datetime.now() + datetime.timedelta(hours=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def __str__(self):
        return self.username

class Quiz(models.Model):
    '''
    The quiz model contains details of all the quizzes that are created by the admin
    '''
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    start_time = models.DateTimeField(default=None)
    length_of_quiz_seconds = models.IntegerField(default=0, null=False)
    domain = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.quiz_id

class Question(models.Model):
    '''
    Question model contains all the questions created by admin
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=200)
    option = models.JSONField()
    correct_index = models.IntegerField(null=False, default=-1)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    domain = models.CharField(max_length=50, default=None)

class QuizQuestion(models.Model):
    '''
    This table is used to keep track of questions in the quiz
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey(Quiz, on_delete=CASCADE)
    question_id = models.ForeignKey(Question, on_delete=CASCADE)

    class Meta:
        unique_together = ('quiz_id', 'question_id')

class QuizResult(models.Model):
    '''
    This table stores the result of the quizzes
    '''
    quiz_id = models.ForeignKey("Quiz", on_delete=CASCADE)
    question_id = models.ForeignKey("Question", on_delete=CASCADE)
    user_id = models.ForeignKey("CustomUser", on_delete=CASCADE)
    answer = models.IntegerField(null=False, default=-1)
    
    class Meta:
        unique_together = (("quiz_id", "question_id", "user_id", "answer"),)

