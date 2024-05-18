"""
URL configuration for caltrack project.

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
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from counter import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Using path for the home URL pattern
    path('streamlit_app/', views.streamlit_app, name='streamlit_app'),
    # path('update_search_bar/', views.update_search_bar, name='update_search_bar'),
    path('update_search_bar/', views.update_search_bar, name='update_search_bar'),
    path('', include('counter.urls')),  # Including URL patterns from counter.urls
]
