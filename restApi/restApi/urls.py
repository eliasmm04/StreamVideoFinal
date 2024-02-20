"""restApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from StreamVideo import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('peliculasPorNombre', views.peliculas_nombre),
    path('seriesPorNombre', views.series_nombre),
    path('actoresPorNombre', views.actores_nombre),
    path('plataformas_nombre/<str:plataformas_name>', views.plataformas_nombre)
    path('series/<int:id_solicitado>' , views.devolver_series_por_id),
    path('peliculas/<int:id_solicitado>' , views.devolver_peliculas_por_id),
    path('series/<int:serieId>/comentarios' , views.crear_comentarios_series),
    path('peliculas/<int:peliculaId>/comentarios' , views.crear_comentarios_peliculas),
    path('peliculas' , views.devolver_peliculas),
    path('series' , views.devolver_series),
    path('register', views.register),
    path('login', views.login),
]
