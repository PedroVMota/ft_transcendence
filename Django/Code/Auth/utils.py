
from django.http import JsonResponse
import base64
import json
import hmac
import hashlib
import time
import os
from functools import wraps

# Obter o SECRET_KEY do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")

def authenticate_jwt(request):
    """Verifica o token JWT no cabeçalho Authorization e autentica o usuário"""
    token = request.headers.get("Authorization")

    if not token:
        return None  # Não encontrou token

    # Verifica e decodifica o JWT
    payload = verify_jwt(token)

    if not payload:
        return None  # Token inválido ou expirado
    
    # Se o token for válido, podemos retornar o payload (usuário autenticado)
    return payload

def base64_url_encode(data):
    """Codifica dados para o formato Base64 URL-safe, removendo o preenchimento '='"""
    encoded = base64.urlsafe_b64encode(data.encode()).decode()
    return encoded.rstrip("=")

def base64_url_decode(data):
    """Decodifica dados do formato Base64 URL-safe, adicionando preenchimento '=' se necessário"""
    padding = "=" * (4 - len(data) % 4)
    data = data + padding
    return base64.urlsafe_b64decode(data).decode()

def create_jwt(payload):
    """Cria o JWT com o cabeçalho e payload"""
    # Cabeçalho
    header = {
        "alg": "HS256",  # Algoritmo de assinatura
        "typ": "JWT"
    }

    # Codificação do header
    encoded_header = base64_url_encode(json.dumps(header))

    # Codificação do payload
    payload['exp'] = int(time.time()) + 3600  # Define o tempo de expiração (1 hora)
    encoded_payload = base64_url_encode(json.dumps(payload))

    # Criação da assinatura
    signature = hmac.new(SECRET_KEY.encode(), f"{encoded_header}.{encoded_payload}".encode(), hashlib.sha256).digest()
    encoded_signature = base64_url_encode(signature.decode('latin1'))

    # Token JWT completo
    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    return jwt_token

def verify_jwt(jwt_token):
    """Verifica se o JWT é válido e se não foi alterado"""
    try:
        # Divide o token nas três partes (Header, Payload, Signature)
        header_b64, payload_b64, signature_b64 = jwt_token.split(".")

        # Decodifica o cabeçalho e o payload
        header = json.loads(base64_url_decode(header_b64))
        payload = json.loads(base64_url_decode(payload_b64))

        # Verifica a expiração do token
        if payload["exp"] < time.time():
            return None  # Token expirado

        # Reconstrução da assinatura para verificação
        signature = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        expected_signature = base64_url_encode(signature.decode('latin1'))

        # Verifica se a assinatura é válida
        if expected_signature != signature_b64:
            return None  # Token inválido

        return payload  # Retorna o payload se o token for válido
    except Exception as e:
        print(f"Erro na verificação do JWT: {e}")
        return None

# Decorador para proteger views com JWT
def jwt_required(view_func):
    """Decorador para proteger views com JWT."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Pegando o token JWT do cabeçalho Authorization
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'Token not provided'}, status=401)
        
        # Verificando se o JWT é válido
        payload = verify_jwt(token)
        
        if not payload:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        
        # Caso o token seja válido, adicionamos as informações do payload ao request.user
        request.user = payload
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
