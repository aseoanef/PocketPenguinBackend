import hashlib
import json
import secrets
import bcrypt
from django.http import JsonResponse
from .models import Shop_list, Family, User, ProductsinLists, Chat, Products
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError


# funcion para conseguir el user a partir del API session token
def __get_request_user(request):
	header_token = request.headers.get('sessionToken', None)
	if header_token is None:
		return None
	try:
		db_session = User.objects.get(user_token=header_token)
		return db_session
	except User.DoesNotExist:
		return None

#Vista principal para la gestión de listas de compras
@csrf_exempt
def listasCompra(request):
	if request.method == 'POST':
		try:
			#Intentar cargar el JSON del cuerpo de la solicitud
			body_json = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)
		#Obtener el token de sesión desde los encabezados
		sessionToken = request.headers.get('sessionToken')
		#Verificar la existencia del token de sesión
		if sessionToken is None:
			return JsonResponse({"error": 'Authentication not valid'}, status=401)
		u = User.objects.get(user_token=sessionToken)  # controlar si usuario no existe

		try:
			#Obtener  el nombre de la nueva lista desde el cuerpo del JSON
			json_newListName = body_json.get('newListName')

		except KeyError:
			return JsonResponse({"error": "Missing parameter in request"}, status=400)
		#Crear y guardar una nueva lista de compras
		shop_list = Shop_list()
		shop_list.list_name = json_newListName
		shop_list.family = u.family
		shop_list.save()
		return JsonResponse({"uploaded": True}, status=201)
	elif request.method == 'GET':
		# Obtener el token de sesión desde los encabezados
		sessionToken = request.headers.get('sessionToken')
		# Verificar la existencia del token de sesión
		if sessionToken is None:
			return JsonResponse({"error": 'Authentication not valid'}, status=401)
		#Obtener el usuario correspondiente al token de sesión
		u = User.objects.get(user_token=sessionToken)  # controlar si el usuario no existe


		#Obtener todas las listas de compras de la familia del usuario
		all_lists = Shop_list.objects.filter(family=u.family)
		# Convertir las listas  a formato JSON
		json_response = [shop_list.to_json() for shop_list in all_lists]
		return JsonResponse(json_response, safe=False, status=200)

	else:
		return JsonResponse({'error': 'HTTP method unsupported'}, status=405)


# Vista para manejar operaciones relacionadas con usuarios (GET, POST, PUT, DELETE)
@csrf_exempt
def user(request):
	# Manejar la solicitud GET para obtener información del usuario
	if request.method == 'GET':
		# Obtener el token de sesión de los encabezados de la solicitud
		sessionToken = request.headers.get('sessionToken')
		if sessionToken is None:
			return JsonResponse({"error": 'Authentication not valid'}, status=401)

		# Buscar al usuario en la base de datos por el token de sesión
		try:
			user = User.objects.get(user_token=sessionToken)
			user_info = {
				'username': user.username,
				'e_mail': user.e_mail,
				'password': user.encrypted_password,
				'family': user.family.pk,
				'user_token': user.user_token,
				'imageUrl': user.imageUrl
			}
			return JsonResponse(user_info, status=200)
		except User.DoesNotExist:
			return JsonResponse({'error': 'User not found for the given token: {sessionToken}'}, status=404)

	# Manejar la solicitud DELETE para eliminar un usuario
	elif request.method == 'DELETE':
		sessionToken = request.headers.get('sessionToken')
		if sessionToken is None:
			return JsonResponse({"error": 'Authentication not valid'}, status=401)

		# Buscar al usuario en la base de datos y eliminarlo
		try:
			user = User.objects.get(user_token=sessionToken)
			user.delete()
			return JsonResponse({'success': True, 'message': 'User deleted successfully'}, status=200)
		except User.DoesNotExist:
			return JsonResponse({'error': 'User not found'}, status=404)

	# Manejar la solicitud POST para registrar un nuevo usuario
	elif request.method == 'POST':
		try:
			# Intentar cargar el cuerpo JSON de la solicitud
			body_json = json.loads(request.body)

			# Obtener datos del JSON
			username = body_json.get('username')
			e_mail = body_json.get('email')
			password = body_json.get('password')

			# Crear una nueva familia
			family = Family()
			family_hash = secrets.token_hex(16)  # Genera una cadena aleatoria de 32 caracteres (16 bytes)
			family.family_hash = hashlib.sha256(family_hash.encode('utf-8')).hexdigest()
			family.save()

			# Verificar si se proporciona un nombre de usuario
			if not username or not e_mail or not password:
				return JsonResponse({'error': 'Missing required fields'}, status=400)
			elif "@" not in e_mail or len(e_mail) < 7:
				return JsonResponse({'error':'Invalid email'},status=400)
			# Hashear la contraseña y guardar el nuevo usuario en la base de datos
			try:
				salted_and_hashed_pass = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
				new_user = User(username=username, e_mail=e_mail, encrypted_password=salted_and_hashed_pass, family=family)
				new_user.save()
				return JsonResponse({'success': True, 'user': new_user.to_json()}, status=201)

			# Manejar el caso en que ya exista un usuario con el mismo nombre
			except IntegrityError:
				return JsonResponse({'error': 'User with this username already exists'}, status=409)

		# Manejar el caso de un formato JSON inválido en el cuerpo de la solicitud
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
			# Manejar la solicitud PUT para actualizar la información del usuario
	elif request.method == 'PUT':#curl -X PUT -H "Content-Type: application/json" -H "sessionToken"--data {\"newName\":\"abduscan\" localhost:8000/user/
		sessionToken = request.headers.get('sessionToken')
		if sessionToken is None:
			return JsonResponse({"error": 'Authentication not valid'}, status=401)
		# Buscar al usuario en la base de datos por el token de sesión
		user = User.objects.get(user_token=sessionToken)

		# Intentar cargar el cuerpo JSON de la solicitud
		body_json = json.loads(request.body)

		# Actualizar nombre de usuario si se proporciona un nuevo nombre
		username = body_json.get('newName')
		if username is not None:
			user.username = username
			user.save()

		# Actualizar código de familia si se proporciona un nuevo código
		family_code = body_json.get('newFamilyCode')
		if family_code is not None:
			try:
				family = Family.objects.get(family_hash=family_code)
				user.family = family
				user.save()
			except Family.DoesNotExist:
				return JsonResponse({'error': 'Family not found for the given family code: {family_code}'},
									status=404)

		# Actualizar URL de la imagen si se proporciona una nueva URL
		imageUrl = body_json.get('newProfilePicture')
		if imageUrl is not None:
			user.imageUrl = imageUrl
			user.save()

		return JsonResponse({'message': 'User updated successfully'}, status=200)
	else:
		# Devolver una respuesta si el método no es PUT, POST, GET, o DELETE
		return JsonResponse({'error': 'Method Not Allowed'}, status=405)


# Vista para obtener información detallada o eliminar una lista de compras
@csrf_exempt
def sessions(request):
	if request.method != 'POST':  # curl -X POST -H "Content-Type: application/json" --data {\"email\":\"anxo@gmail.com\",\"password\":\"blablabla\"} localhost:8000/session/
		return JsonResponse({"error": "Método HTTP no soportado"}, status=405)
	body_json = json.loads(request.body)
	try:
		json_password = body_json['password']
		json_email = body_json['email']
	except KeyError:
		return JsonResponse({"error": "Falta un parámetro en el body request"}, status=400)
	try:
		db_user = User.objects.get(e_mail=json_email)
	except User.DoesNotExist:
		return JsonResponse({"error": "El usuario no se encuentra en nuestro sistema"}, status=404)
	if bcrypt.checkpw(json_password.encode('utf8'), db_user.encrypted_password.encode('utf8')):
		# random_family = secrets.token_hex(10)
		random_token = secrets.token_hex(10)
		# session = User(username=db_user,user_token=random_token,family=random_family)
		db_user.user_token = random_token
		db_user.save()
		return JsonResponse({"sessionToken": random_token}, status=201)
	elif not bcrypt.checkpw(json_password.encode('utf8'), db_user.encrypted_password.encode('utf8')):
		return JsonResponse({"error": "Password not valid"}, status=401)
	else:
		return JsonResponse({"error": "Contraseña inválida"}, status=401)




#obtener la informacion de una lista
@csrf_exempt
def list_info(request, list_pk):
	if request.method == "GET": #curl -X GET -H "Content-Type:application/json" -H "sessionToken:blablabla" http://localhost:8000/lists/2/
		# Obtener el usuario autorizado a partir del token de sesión
		autorized_user = __get_request_user(request)
		try:
			# checkear que tiene permiso para la lista que se solicita
			shop_list = Shop_list.objects.filter(family=autorized_user.family, pk=list_pk)
		except shop_list.DoesNotExist:
			return JsonResponse({"error": "List was not found"}, status=404)
		# Obtener la lista autorizada por su clave primaria
		selected_list = Shop_list.objects.get(family=autorized_user.family, pk=list_pk)
		json_response = Shop_list.to_json(selected_list)
		return JsonResponse(json_response, safe=False, status=200)
	# delete de la lista checkeando permisos
	elif request.method == "DELETE":
		autorized_user = __get_request_user(request)
		try:
			shop_list = Shop_list.objects.filter(family=autorized_user.family, pk=list_pk)
		except shop_list.DoesNotExist:
			return JsonResponse({"error": "List was not found"}, status=404)
		# Eliminar la lista
		shop_list.delete()
		return JsonResponse({"list deleted": True}, status=201)



# Vista para obtener información sobre productos o filtrarlos por nombre
@csrf_exempt
def products(request):
	if request.method == "GET":
		# checkea si tiene nombre en el header y filtrar en caso positivo
		if request.headers.get("product.name") != None:
			item_name = request.headers.get("product.name")
			try:
				all_rows = Products.objects.filter(name=item_name)
			except all_rows.DoesNotExist:
				return JsonResponse({"error": "Product was not found"}, status=404)
			json_response = []
			for row in all_rows:
				json_response.append(row.to_json())
		# si no tiene nombre en el header devuelve todos
		else:
			all_rows = Products.objects.all()
			json_response = []
			for row in all_rows:
				json_response.append(row.to_json())
		return JsonResponse(json_response, safe=False)
	else:
		return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)


# Vista para obtener los chats a partir del token de user
@csrf_exempt
def chat(request):
	# Get the authorized user based on the API session token
	autorized_user = __get_request_user(request)
	# Get the family associated with the authorized user
	family = autorized_user.family
	if request.method == "GET":  ##curl -X GET -H "sessionToken:blablabla" http://localhost:8000/chat/
		all_rows = Chat.objects.filter(family=Family.objects.get(pk=family.pk))
		json_response = []
		for row in all_rows:
			json_response.append(row.to_json())
		return JsonResponse(json_response, safe=False)
	elif request.method == "POST":  ##curl -X POST -H "Content-Type: application/json" -H "sessionToken:blablabla" --data {\"content\":\"Yourmessage\",\"user_token\":\"blablabla\"} localhost:8000/chat
		body_json = json.loads(request.body)
		try:
			# Extract content from the JSON body
			json_content = body_json.get('content', " ")
			if json_content is None:
				return JsonResponse({"error": "Missing parameter in request"}, status=400)
		except KeyError:
			return JsonResponse({"error": "Missing parameter in request"}, status=400)
		# Check if the user is authenticated
		if autorized_user is None:
			return JsonResponse({"error": "You did not provide a valid session token"}, status=401)
		# Create a new chat message and save it to the database
		newmessage = Chat(
			user=autorized_user,
			message=json_content,
			family=family)
		newmessage.save()
		return JsonResponse({"ok": True}, status=201)


# Vista para obtener y agregar productos a una lista de compras específica
@csrf_exempt
def productsinList(request, list_pk):
	if request.method == "GET": #curl -X GET -H "Content-Type:application/json" -H "sessionToken:blablabla" http://localhost:8000/lists/2/
		# Obtener el usuario autorizado a partir del token de sesión
		autorized_user = __get_request_user(request)
		try:
			# checkear que el usuario autorizado a partir del token de sesión
			shop_list = Shop_list.objects.filter(family=autorized_user.family, pk=list_pk)
		except shop_list.DoesNotExist:
			return JsonResponse({"error": "List was not found"}, status=404)
		# Obtener la clave primaria
		for row in shop_list:
			shop_list.pk = row.to_json().get("id")
		# Obtener todos los elementos de la lista
		all_rows = ProductsinLists.objects.filter(list=Shop_list.objects.get(pk=shop_list.pk))
		json_response = []
		for row in all_rows:
			json_response.append(row.to_json())
		return JsonResponse(json_response, safe=False)
	elif request.method == "POST":  ##curl -X POST -H "Content-Type: application/json" -H "sessionToken:blablabla" --data {\"name\":\"tomate\",\"price\":1} localhost:8000/lists/2/items/
		#Obtener el usuario autorizado a partir del token de sesión
		autorized_user = __get_request_user(request)
		try:
			#Intentar cargar el JSON del cuerpo de la solicitud
			body_json = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Invalid JSON'}, status=400)
		try:
			# Obtener la lista de compras a las que se agregarán los productos
			shop_list = Shop_list.objects.get(family=autorized_user.family, pk=list_pk)
		except shop_list.DoesNotExist:
			return JsonResponse({"error": "List was not found"}, status=404)
		try:
			# Obtener el nombre y el precio del producto desde le cuerpo del JSON
			json_nombre = body_json.get('name')
			json_precio = body_json.get('price')
		except KeyError:
			return JsonResponse({"error": "Missing parameter in request"}, status=400)
		# Crear y guardar un nuevo elemento en la lista de compras
		iteminlist = ProductsinLists(
			product=Products.objects.get(name=json_nombre, price=json_precio),
			list=shop_list,
			quantity=1,
		)
		iteminlist.save()

		return JsonResponse({"product added": True}, status=201)
	else:
		return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

@csrf_exempt
def edit_item(request, list_id, item_id):
	if request.method == 'PUT': #curl -X PUT -H "Content-Type: application/json" -H "sessionToken: miau" -d '{\"quantity\": 5,\ "bought\": true}' http://localhost:8000/lists/1/items/
		try:
			body_json = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid Json"}, status=400)

		authorized_user = __get_request_user(request)
		if not authorized_user:
			return JsonResponse({"error": "Authentication not valid"}, status=401)

		try:
			shop_list = Shop_list.objects.get(family=authorized_user.family, pk=list_id)
		except Shop_list.DoesNotExist:
			return JsonResponse({"error": "List not found"}, status=404)

		try:
			productsinList = ProductsinLists.objects.get(list=list_id, product=item_id)
		except ProductsinLists.DoesNotExist:
			return JsonResponse({"error": "Item not found in the list"}, status=404)

		try:
			json_new_quantity = body_json.get('quantity')
			if json_new_quantity is not None and productsinList.quantity != json_new_quantity:
				productsinList.quantity = json_new_quantity
		except KeyError:
			return JsonResponse({"error": "Missing 'quantity' parameter in request"}, status=400)

		try:
			json_new_bought = body_json.get('bought')
			if json_new_bought is not None and productsinList.bought != json_new_bought:
				productsinList.bought = json_new_bought
		except KeyError:
			return JsonResponse({"error": "Missing 'bought' parameter in request"}, status=400)

		productsinList.save()
		return JsonResponse({"message": "Item updated successfully"}, status=200)
	else:
		return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)