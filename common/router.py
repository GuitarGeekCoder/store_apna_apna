from rest_framework.routers import DefaultRouter
from account.views import AuthenticationViewSet,GetUserProfileViewSet
from order.views import Orders
from wallet.views import Payment
router = DefaultRouter()
router.register(r"auth", AuthenticationViewSet, basename='authentication')
router.register(r"user",GetUserProfileViewSet,basename="getuser")
router.register(r"order",Orders,basename="orders")
router.register(r"payment",Payment,basename="payment")