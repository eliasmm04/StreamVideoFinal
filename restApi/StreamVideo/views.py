from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Peliculas
from .models import Favoritos
from .models import Series
from .models import Plataformas
from .models import Users
from .models import Actor 
from .models import Favoritos
import json,jwt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import  datetime
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST


# get favoritos peliculas
def devolver_peliculas_favoritas(request, usuario_id):
    if request.method == 'GET':
        if usuario_id is None: 
            return JsonResponse({'error': 'No hay id de Usuario'}, status=405)
        
        # Filtra los favoritos del usuario actual
        favoritos = Favoritos.objects.filter(userid=usuario_id)
        
        # Lista para almacenar los resultados
        lista_favorito = []
        
        # Itera sobre los favoritos y obtén las películas asociadas
        for favorito in favoritos:
            pelicula = favorito.peliculaid
            diccionario = {
                'id': pelicula.id,
                'nombre': pelicula.nombre,
                'genero': pelicula.genero,
                # Agrega más campos según tu modelo Pelicula
            }
            lista_favorito.append(diccionario)
        
        # Devuelve la respuesta en formato JSON
        return JsonResponse(lista_favorito, safe=False)

    # Si el método no es GET, devuelve un error de método no permitido
    return JsonResponse({'error': 'Method not allowed'}, status=405)
#He borrado el get de series ya que pertenecía a la rama de elías

# get favoritos series
def devolver_series_favoritas(request, usuario_id):
    if request.method == 'GET':
        if usuario_id is None: 
            return JsonResponse({'error': 'No hay id de Usuario'}, status=405)
        
        # Filtra los favoritos del usuario actual
        favoritos = Favoritos.objects.filter(userid=usuario_id)
        
        # Lista para almacenar los resultados
        lista_favorito = []
        
        # Itera sobre los favoritos y obtén las películas asociadas
        for favorito in favoritos:
            serie = favorito.peliculaid
            diccionario = {
                'id': serie.id,
                'nombre': serie.nombre,
                'genero': serie.genero,
                # Agrega más campos según tu modelo Pelicula
            }
            lista_favorito.append(diccionario)
        
        # Devuelve la respuesta en formato JSON
        return JsonResponse(lista_favorito, safe=False)

    # Si el método no es GET, devuelve un error de método no permitido
    return JsonResponse({'error': 'Method not allowed'}, status=405)
#He borrado el get de series ya que pertenecía a la rama de elías

#Put Favoritos
@csrf_exempt
def favoritosview(request, favoritoid):
    if request.method == 'PUT':
        session_token = request.headers.get('SesionToken')
        usuario = Users.objects.filter(sessiontoken=session_token).first()
        if not usuario:
            # Si el usuario no está autenticado, devolver un error de autorización
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        try:
            favoritos = Favoritos.objects.get(pk=favoritoid)
            data = json.loads(request.body)
            favoritos.esfavorito = data.get('Favorita?', favoritos.esfavorito)
            favoritos.save()
            if favoritos.esfavorito == 1:
                return JsonResponse({'message': 'Puesta como favorita'}, status=200)
            else:
                return JsonResponse({'message': 'Retirada de favoritos'}, status=200)
        except Favoritos.DoesNotExist:
            return JsonResponse({'error': 'Fav no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

#Logout 
@csrf_exempt
def logout(request, user_id):
    # Comprobación de token. El error_response guarda la información que le proporciona el return del verify_token
	error_response, payload = verify_token(request)
	#Si existe el error se visualizará por pantalla
	if error_response:
		return error_response

	#Si el método introducido no es un PATCH, saltará el error
	if request.method != 'PATCH':
		return JsonResponse({'error': 'Método no permitido'}, status=405)

	try:
		#Cogemos todos los objetos del modelo Users que coincidan con el filtrado introducido
		user = Users.objects.get(pk=user_id)
		user.sessiontoken = None  # o user.session_token =
		#Guardamos el objeto sessiontoken con el valor Nulo y luego guardamos los cambios con user.save()
		user.save()
		return JsonResponse({'message': 'Sesión cerrada exitosamente'}, status=200)
	except Users.DoesNotExist:
		return JsonResponse({'error': 'Faltan parametros o son incorrectos'}, status=400)
	except Exception as e:
		return JsonResponse({'error':'Unauthorized'},status=401)
