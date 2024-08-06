import json

# Encabezados CORS globales
CORS_HEADERS = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
}

# Arreglo global para almacenar los datos de los vehículos
vehicles = [
    {
        'id': '1',
        'marca': 'Toyota',
        'modelo': 'Corolla',
        'velocidadMaxima': 180,
        'tipo': 'Sedán'
    },
    {
        'id': '2',
        'marca': 'Ford',
        'modelo': 'Mustang',
        'velocidadMaxima': 250,
        'tipo': 'Deportivo'
    },
    {
        'id': '3',
        'marca': 'Chevrolet',
        'modelo': 'Tahoe',
        'velocidadMaxima': 200,
        'tipo': 'SUV'
    },
    {
        'id': '4',
        'marca': 'Tesla',
        'modelo': 'Model S',
        'velocidadMaxima': 250,
        'tipo': 'Eléctrico'
    }
]

# Contador global para el número total de vehículos
vehicle_counter = len(vehicles)

def lambda_handler(event, context):
    # Obtener el método HTTP de la solicitud
    http_method = event.get('httpMethod')

    if http_method == 'POST':
        return create_vehicle(event)
    elif http_method == 'GET':
        return get_vehicles(event)
    elif http_method == 'PUT':
        return update_vehicle(event)
    elif http_method == 'DELETE':
        return delete_vehicle(event)
    else:
        return {
            'statusCode': 405,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Method Not Allowed'}, ensure_ascii=False)
        }

def create_vehicle(event):
    global vehicles, vehicle_counter
    body = json.loads(event.get('body', '{}'))

    # Validar los datos
    required_fields = ['marca', 'modelo', 'velocidadMaxima', 'tipo']
    if not all(field in body for field in required_fields):
        return {
            'statusCode': 400,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Missing required fields'}, ensure_ascii=False)
        }

    # Generar un nuevo ID
    new_id = str(vehicle_counter + 1)

    # Crear el nuevo vehículo con el ID generado
    new_vehicle = {
        'id': new_id,
        'marca': body['marca'],
        'modelo': body['modelo'],
        'velocidadMaxima': body['velocidadMaxima'],
        'tipo': body['tipo']
    }

    # Agregar el nuevo vehículo
    vehicles.append(new_vehicle)
    vehicle_counter += 1  # Incrementar el contador

    return {
        'statusCode': 201,
        'headers': CORS_HEADERS,
        'body': json.dumps({'message': 'Vehicle created successfully'}, ensure_ascii=False)
    }

def get_vehicles(event):
    global vehicles
    return {
        'statusCode': 200,
        'headers': CORS_HEADERS,
        'body': json.dumps(vehicles, ensure_ascii=False)
    }

def update_vehicle(event):
    global vehicles
    body = json.loads(event.get('body', '{}'))
    vehicle_id = body.get('id')

    # Buscar el vehículo por ID
    vehicle = next((v for v in vehicles if v.get('id') == vehicle_id), None)
    if not vehicle:
        return {
            'statusCode': 404,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Vehicle not found'}, ensure_ascii=False)
        }

    # Actualizar el vehículo
    for key, value in body.items():
        if key != 'id':
            vehicle[key] = value
    return {
        'statusCode': 200,
        'headers': CORS_HEADERS,
        'body': json.dumps({'message': 'Vehicle updated successfully'}, ensure_ascii=False)
    }

def delete_vehicle(event):
    global vehicles, vehicle_counter
    body = json.loads(event.get('body', '{}'))
    vehicle_id = body.get('id')

    # Buscar y eliminar el vehículo por ID
    vehicles = [v for v in vehicles if v.get('id') != vehicle_id]

    # Actualizar el contador
    vehicle_counter = len(vehicles)

    return {
        'statusCode': 200,
        'headers': CORS_HEADERS,
        'body': json.dumps({'message': 'Vehicle deleted successfully'}, ensure_ascii=False)
    }
