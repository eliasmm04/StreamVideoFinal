from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Peliculas

from .models import Comentariospeliculas
from .models import Comentariosseries
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


# Función para devolver detalles de una película por su ID
def devolver_peliculas_por_id(request, id_solicitado):
	# Obtener la película con el ID solicitado desde la base de datos
	pelicula=Peliculas.objects.get(id=id_solicitado)
	# Obtener todos los comentarios asociados a esta película
	comentarios=pelicula.comentariospeliculas_set.all()
	# Lista para almacenar los comentarios en formato JSON
	lista_comentarios=[]
	# Iterar sobre cada comentario y crear un diccionario con su información
	for fila_comentario_sql in comentarios:
		diccionario={}
		diccionario['id']= fila_comentario_sql.id
		diccionario['comentario']=fila_comentario_sql.comentario
		lista_comentarios.append(diccionario)
		# Construir el objeto JSON de respuesta con los detalles de la película y sus comentarios
	resultado={
		'id':pelicula.id,
		'nombre':pelicula.nombre,
		'año':pelicula.año,
		'comentarios':lista_comentarios
	}
	# Devolver la respuesta en formato JSON
	return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False})

def devolver_series_por_id(request, id_solicitado):
        serie=Series.objects.get(id=id_solicitado)
        comentarios=serie.comentariosseries_set.all()
        lista_comentarios=[]
        for fila_comentario_sql in comentarios:
                diccionario={}
                diccionario['id']= fila_comentario_sql.id
                diccionario['comentario']=fila_comentario_sql.comentario
                lista_comentarios.append(diccionario)
        resultado={
                'id':serie.id,
                'nombre':serie.nombre,
                'año':serie.año,
                'comentarios':lista_comentarios
        }
        return JsonResponse(resultado, json_dumps_params={'ensure_ascii':False})
# crear comentarios sobre películas
@csrf_exempt
def crear_comentarios_peliculas(request, peliculaId):
    if request.method == 'POST':
	# Verificar el token de sesión para autenticar al usuario
        session_token = request.headers.get('SesionToken')
        usuario = Users.objects.filter(sessiontoken=session_token).first()
        if not usuario:
	    # Si el usuario no está autenticado, devolver un error de autorización
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
	    # Decodificar la solicitud JSON y obtener el nuevo comentario
        json_peticion = json.loads(request.body)
        nuevo_comentario = json_peticion.get('nuevo comentario')

        if not nuevo_comentario:
		# Si no se proporciona un nuevo comentario, devolver un error
            return JsonResponse({'error': 'falta el nuevo comentario en la solicitud'}, status=400)
	# Obtener la película asociada al ID proporcionado
        pelicula = Peliculas.objects.get(id=peliculaId)
	# Crear un nuevo objeto de comentario asociado a esta película y guardarlo en la base de datos
        comentario = Comentariospeliculas(comentario=nuevo_comentario, peliculaid=pelicula)
        comentario.save()
	# Obtener todos los comentarios actualizados asociados a esta película
        comentarios_actualizados = Comentariospeliculas.objects.filter(peliculaid=pelicula)
	# Crear una lista de comentarios en formato JSON
        comentarios_json = [{'id': comentario.id, 'comentario': comentario.comentario} for comentario in comentarios_actualizados]
	# Devolver una respuesta de éxito junto con los comentarios actualizados en formato JSON
        return JsonResponse({'status': 'ok', 'comentarios': comentarios_json}, status=201)

    except json.JSONDecodeError:
	    # Manejar errores de decodificación JSON
        return JsonResponse({'error': 'Error al decodificar el Json'}, status=400)
    except Peliculas.DoesNotExist:
	    # Manejar errores cuando la película no existe
        return JsonResponse({'error': 'La pelicula no existe'}, status=404)
    except Exception as e:
	    # Manejar otros errores internos del servidor
        return JsonResponse({'error': str(e)}, status=500)

# Vista para crear comentarios sobre series
@csrf_exempt
def crear_comentarios_series(request, serieId):
    if request.method == 'POST':
        # Verificar el token de sesión para autenticar al usuario
        session_token = request.headers.get('SesionToken')
        usuario = Users.objects.filter(sessiontoken=session_token).first()
        if not usuario:
            # Si el usuario no está autenticado, devolver un error de autorización
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        # Decodificar la solicitud JSON y obtener el nuevo comentario
        json_peticion = json.loads(request.body)
        nuevo_comentario = json_peticion.get('nuevo comentario')

        if not nuevo_comentario:
            # Si no se proporciona un nuevo comentario, devolver un error
            return JsonResponse({'error': 'falta el nuevo comentario en la solicitud'}, status=400)

        # Obtener la serie asociada al ID proporcionado
        serie = Series.objects.get(id=serieId)
        # Crear un nuevo objeto de comentario asociado a esta serie y guardarlo en la base de datos
        comentario = Comentariosseries(comentario=nuevo_comentario, serieid=serie)
        comentario.save()

        # Obtener todos los comentarios actualizados asociados a esta serie
        comentarios_actualizados = Comentariosseries.objects.filter(serieid=serie)

        # Crear una lista de comentarios en formato JSON
        comentarios_json = [{'id': comentario.id, 'comentario': comentario.comentario} for comentario in comentarios_actualizados]

        # Devolver una respuesta de éxito junto con los comentarios actualizados en formato JSON
        return JsonResponse({'status': 'ok', 'comentarios': comentarios_json}, status=201)

    except json.JSONDecodeError:
        # Manejar errores de decodificación JSON
        return JsonResponse({'error': 'Error al decodificar el Json'}, status=400)
    except Series.DoesNotExist:
        # Manejar errores cuando la serie no existe
        return JsonResponse({'error': 'La serie no existe'}, status=404)
    except Exception as e:
        # Manejar otros errores internos del servidor
        return JsonResponse({'error': str(e)}, status=500)

def devolver_peliculas(request):
	lista=Peliculas.objects.all()
	respuesta_final=[]
	for fila_sql in lista:
		diccionario={}
		diccionario['id']= fila_sql.id
		diccionario['nombre']=fila_sql.nombre
		diccionario['genero']=fila_sql.genero
		diccionario['año']=fila_sql.año
		diccionario['plataformaid']=fila_sql.plataformaid.id
		diccionario['descripcion']=fila_sql.descripcion
		diccionario['urlimagen']=fila_sql.urlimagen
		diccionario['actorid']=fila_sql.actorid.id
		diccionario['duracion']=fila_sql.duracion
		diccionario['valoracion']=fila_sql.valoracion
		diccionario['comentarioid']=fila_sql.comentarioid.id
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)


def devolver_series(request):
	lista=Series.objects.all()
	respuesta_final=[]
	for fila_sql in lista:
		diccionario={}
		diccionario['id']= fila_sql.id
		diccionario['nombre']=fila_sql.nombre
		diccionario['genero']=fila_sql.genero
		diccionario['año']=fila_sql.año
		diccionario['numerotemporadas']=fila_sql.numtemporadas
		diccionario['plataformaid']=fila_sql.plataformaid.id
		diccionario['descripcion']=fila_sql.descripcion
		diccionario['urlimagen']=fila_sql.urlimagen
		diccionario['actorid']=fila_sql.actorid.id
		diccionario['valoracion']=fila_sql.valoracion
		diccionario['comentarioid']=fila_sql.comentarioid.id
		respuesta_final.append(diccionario)
	return JsonResponse(respuesta_final, safe=False)





SECRET_KEY = 'claveTremendamentesegura.'
""" 
Crea un token JWT (JSON Web Token) para el usuario dado.
Returns:
        str: Token JWT generado.

"""
def crear_token(user_id):
	payload = {
		'id': user_id,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
		'iat': datetime.datetime.utcnow()
	}
	token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
	return token

"""
    Verifica un token JWT incluido en la solicitud HTTP.

    Returns:
      		Una tupla con dos elementos:
            - JsonResponse o None: Si hay un error, devuelve una respuesta JSON con un mensaje de error.
            - dict or None: Si el token es válido, devuelve el payload decodificado.
"""

def verify_token(request):
	token = request.META.get('HTTP_AUTHORIZATION',None)
	if not token:
		return JsonResponse({'message':'Token is missing!'}, status=401), None

	try:
		if token.startswith('Bearer '):
			token = token.split(' ')[1]
		payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
		return None, payload
	except jwt.ExpiredSignatureError:
		return JsonResponse({'message':'Token has expired'}, status=401), None
	except jwt.InvalidTokenError:
		return JsonResponse({'message':'Invalid token!'}, status=401), None

# login
# cuando inicias sesion la primera vez lo hace perfectamente y cuando cierras tambien lo hace correctamente pero cuando inicias sesion por segunda vez te sale el error de contraseña incorrecta aún poniendo la contraseña bien

@csrf_exempt
def login(request):

	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			user = Users.objects.get(nombre=data['nombre'])
			if check_password(data['contraseña'], user.contraseña):
				token = crear_token(user.id)
				sessiontoken=crear_token(user.id)
				user.sessiontoken=sessiontoken
				user.save()
				return JsonResponse( {'iduser':user.id , 'token':token}, status=200)
			else:
				return JsonResponse({'error': 'Contrasenia incorrecta'}, status=401)
		except Users.DoesNotExist:
			return JsonResponse({'error':'Usuario no encontrado'}, status=404)



@csrf_exempt
def register(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body.decode('utf-8'))
			usuario=Users()
			usuario.nombre=data['nombre']
			usuario.contraseña=data['contraseña']
			usuario.apellidos=data['apellidos']
			usuario.email=data['email']

            		# Verificar si los campos requeridos están presentes en los datos recibidos
			required_fields = ['nombre', 'contraseña', 'apellidos', 'email']
			for field in required_fields:
				if field not in data:
					return JsonResponse({'error': 'Faltan parámetros en la solicitud'}, status=400)

            # Verificar si ya existe un usuario con el mismo nombre o email
			if Users.objects.filter(nombre=data['nombre']).exists() or Users.objects.filter(email=data['email']).exists():
				return JsonResponse({'error': 'Ya existe un usuario con ese nombre o email'}, status=409)


            # Crear el nuevo usuario
			new_user = Users(
				nombre=data['nombre'],
				contraseña=data['contraseña'],
				apellidos=data['apellidos'],
				email=data['email'],
			)
			new_user.save()
			return JsonResponse({'message': 'Usuario registrado exitosamente'}, status=201)
		except Exception as e:
			return JsonResponse({'error':str(e)}, status=400)

