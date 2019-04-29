from rest_framework.routers import DefaultRouter
from .views import ActViewSets

ACT_ROUTER = DefaultRouter()
ACT_ROUTER.register(r'', ActViewSets)
