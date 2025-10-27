from django.contrib import admin
from django.urls import include, path
from users.router import router as users_api_route
from house.router import router as house_api_route
from task.router import router as task_api_route
from django.conf import settings
from oauth2_provider.views.base import AuthorizationView
from oauth2_provider.views import TokenView
from django.conf.urls.static import static

# Define auth-related URL patterns
auth_api_urlpatterns = [
    path('', include('rest_framework_social_oauth2.urls')),  # Includes convert-token, revoke-token, etc.
]

if settings.DEBUG:
    auth_api_urlpatterns.append(path('verify/', include('rest_framework.urls')))

# Define API URL patterns with a single 'api/' prefix
api_urlpatterns = [
    path('auth/', include(auth_api_urlpatterns)),  # /api/auth/ endpoints
    path('accounts/', include(users_api_route.urls)),  # /api/accounts/ endpoints
    path('house/',include(house_api_route.urls)),
    path('task/',include(task_api_route.urls)),
]

# Root URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),  # Centralize API routes under /api/
    path('authorize/', AuthorizationView.as_view(), name='authorize'),  # Keep manual definition if needed
    path('token/', TokenView.as_view(), name='token'),  # Keep manual definition if needed
]
# Serve media files during development

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEADIA_ROOT)


