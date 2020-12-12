from django.conf import settings
from django.urls import path, re_path, include
from common import views
from rest_framework import routers
from rest_framework.authtoken import views as rest_views
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = 'Reservations network API'
API_DESCRIPTION = 'A Web API for reservations.'
schema_view = get_schema_view(title=API_TITLE)

router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet, basename='account')
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'laundry', views.LaundryViewSet, basename='laundry')

urlpatterns = [
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('token-auth/', rest_views.obtain_auth_token),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += [
        path('schema/', schema_view),
        path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
    ]
