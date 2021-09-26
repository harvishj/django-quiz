from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
  
urlpatterns = [
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('createaccount/', views.CreateAccount.as_view(), name ='createaccount'),
    path('allquestions/', views.AllQuestions.as_view(), name ='allquestions'),
    path('schedulequiz/', views.ScheduleQuiz.as_view(), name ='schedulequiz'),
    path('scheduledquizzes/', views.ScheduledQuizzes.as_view(), name ='scheduledquizzes'),
    path('attemptquiz/', views.AttemptQuiz.as_view(), name ='attemptquiz'),
    path('quiz/', views.QuizView.as_view(), name ='quiz'),
    path('results/', views.Results.as_view(), name ='results'),
    path('addquestion/', views.AddQuestion.as_view(), name ='addquestion'),
]

urlpatterns = format_suffix_patterns(urlpatterns)