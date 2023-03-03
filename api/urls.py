from django.urls import path
from api import users

app_name = 'api'
urlpatterns = [
    path('login/callback/', users.google_oauth2_callback),
    path('login/', users.login),
    path('logout/', users.logout),
    # path('auth/login/', users.my_login),
    # path('auth/logout/', users.my_logout),
    # path('user/get/', users.get),
    # path('user/createQuestion/', users.create_question),
    # path('user/createQuestion/<int:id>/', users.update_question),
    # path('user/vote/', users.vote),
    # path('question/get/', questions.get),
    # path('question/search/', questions.search),
    # path('<int:id>/result/', results.get)
]