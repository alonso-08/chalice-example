import json
from chalice import Chalice, Response
import boto3
import traceback
from chalicelib.model import ImageModel
app = Chalice(app_name='images-descriptor')

s3_client=boto3.client("s3")
bucket_name="images-chalice-bucket"
# Crear una instancia del cliente de DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-east-1')  # Reemplaza 'us-east-1' con tu región

@app.route('/images/{image_id}', methods=['GET'])
def get_image_by_id(image_id):
    # Nombre de la tabla en DynamoDB
    table_name = 'images'  # Reemplaza con el nombre de tu tabla

    # Define la clave principal del elemento que deseas obtener
    key = {
        'id': {'S': image_id}  # Asumiendo que 'id' es el nombre del campo de clave principal
    }

    try:
        # Realiza la operación GetItem
        response = dynamodb.get_item(
            TableName=table_name,
            Key=key
        )

        # Verifica si se encontró el elemento
        if 'Item' in response:
            item = response['Item']
            return Response(json.dumps(item), status_code=200, headers={'Content-Type': 'application/json'})
        else:
            return Response("El elemento no se encontró en la tabla.", status_code=404)
    except Exception as e:
        return Response(f"Error: {str(e)}", status_code=500)
    
@app.route('/images', methods=['GET'])
def get_images():
    try:
        response = dynamodb.scan(
            TableName="images",
            # Aquí puedes agregar filtros o condiciones si es necesario
        )

        # El resultado del escaneo se encuentra en la clave 'Items' de la respuesta
        items = response['Items']

        # Procesa los elementos para eliminar la anidación
        processed_items = []
        for item in items:
            processed_item = {}
            for key, value in item.items():
                processed_item[key] = value['S']
            processed_items.append(processed_item)

        # Devuelve la lista de elementos procesados como una respuesta JSON
        return Response(json.dumps(processed_items), status_code=200, headers={'Content-Type': 'application/json'})
    except Exception as e:
        return Response(f"Error al escanear la tabla: {str(e)}", status_code=500)







