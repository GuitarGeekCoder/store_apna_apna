from django.urls import path,include
from .router import router
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('apna/', include(router.urls)),
    path('token/refresh/' ,jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
