from django.urls import path
from users.views import (CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInformationView,
                        LoginView, LoginRefreshView, LogoutView, ProfileView, ForgotPasswordView,
                        ResetPasswordView)



urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('login/refresh', LoginRefreshView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),  
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('user/<str:id>/profile/', ProfileView.as_view()),
]
