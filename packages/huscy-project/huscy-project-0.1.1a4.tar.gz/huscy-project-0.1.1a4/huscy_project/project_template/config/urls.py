from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token

from huscy.appointments.urls import router as appointments_router
from huscy.bookings.urls import router as bookings_router
from huscy.rooms.urls import router as rooms_router
from huscy.users.urls import router as users_router
from huscy_project.views import health_check


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_check/', health_check),
    path('api-auth-token/', obtain_auth_token),
    path('api/appointments/', include(appointments_router.urls)),
    path('api/attributes/', include('huscy.attributes.urls')),
    path('api/bookings/', include(bookings_router.urls)),
    path('api/projects/', include('huscy.projects.urls')),
    path('api/', include('huscy.project_documents.urls')),
    path('api/', include('huscy.project_ethics.urls')),
    path('api/recruitment/', include('huscy.recruitment.urls')),
    path('api/rooms/', include(rooms_router.urls)),
    path('api/subjects/', include('huscy.subjects.urls')),
    path('api/users/', include(users_router.urls)),
]

if settings.DEBUG:
    urlpatterns.append(
        path('api-auth/', include('rest_framework.urls')),
    )
