"""
URL configuration for chatapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chat.views import room, home, login_view, group_create, PrintView, RoomViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register("room", RoomViewSet, basename="room")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("room/<uuid:room_id>/<int:pk>/", room, name="chat_room"),
    path("room/<int:pk>/", room, name="chat_room"),
    path("group/<int:pk>/", group_create, name="group_create"),
    path("<int:pk>/", home, name="home"),
    path("login", login_view),
    path("print", PrintView.as_view(), name="print"),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


