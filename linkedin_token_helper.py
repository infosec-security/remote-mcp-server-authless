#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Token Helper
Script auxiliar para obter access tokens do LinkedIn
"""

import json
import requests
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser
import time

class CallbackHandler(BaseHTTPRequestHandler):
    """Handler para receber o callback OAuth"""
    
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse da query string
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            
            if 'code' in query_components:
                self.server.auth_code = query_components['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                success_html = """
                <html>
                <head><title>Autorização Concluída</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #0077B5;">✅ Autorização Realizada com Sucesso!</h1>
                    <p>Você pode fechar esta janela e retornar ao terminal.</p>
                    <p>O código de autorização foi capturado automaticamente.</p>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
            else:
                error = query_components.get('error', ['Erro desconhecido'])[0]
                self.server.auth_code = None
                self.server.auth_error = error
                
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                error_html = f"""
                <html>
                <head><title>Erro na Autorização</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #d32f2f;">❌ Erro na Autorização</h1>
                    <p>Erro: {error}</p>
                    <p>Tente novamente ou verifique suas configurações.</p>
                </body>
                </html>
                """
                self.wfile.write(error_html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suprimir logs HTTP
        return

class LinkedInTokenHelper:
    """Classe para auxiliar na obtenção de tokens LinkedIn"""
    
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = "http://localhost:8080/callback"
        
    def load_credentials(self):
        """Carrega credenciais do arquivo ou solicita input"""
        try:
            with open('linkedin_credentials.json', 'r') as f:
                creds = json.load(f)
                self.client_id = creds.get('client_id')
                self.client_secret = creds.get('client_secret')
                
                if self.client_id and self.client_secret:
                    print(f"✅ Credenciais carregadas: Client ID = {self.client_id[:10]}...")
                    return True
        except FileNotFoundError:
            pass
            
        print("📝 Credenciais não encontradas. Vamos configurá-las:")
        print("\n1. Acesse: https://developer.linkedin.com/")
        print("2. Crie uma aplicação ou use uma existente")
        print("3. Na aba 'Auth', encontre suas credenciais\n")
        
        self.client_id = input("Digite seu Client ID: ").strip()
        self.client_secret = input("Digite seu Client Secret: ").strip()
        
        # Salvar credenciais
        creds = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        with open('linkedin_credentials.json', 'w') as f:
            json.dump(creds, f, indent=2)
            
        print("✅ Credenciais salvas em 'linkedin_credentials.json'")
        return True
    
    def get_authorization_url(self):
        """Gera URL de autorização"""
        scopes = [
            'w_member_social',  # Escrever posts
            'r_liteprofile'     # Ler perfil básico
        ]
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(scopes),
            'state': 'linkedin_automation_2024'
        }
        
        base_url = 'https://www.linkedin.com/oauth/v2/authorization'
        auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        return auth_url
    
    def start_callback_server(self):
        """Inicia servidor para receber callback"""
        server = HTTPServer(('localhost', 8080), CallbackHandler)
        server.auth_code = None
        server.auth_error = None
        
        print("🌐 Servidor de callback iniciado em http://localhost:8080")
        
        # Iniciar servidor em thread separada
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server
    
    def exchange_code_for_token(self, auth_code):
        """Troca código de autorização por access token"""
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(url, data=data, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data
            else:
                print(f"❌ Erro ao obter token: {response.status_code}")
                print(f"Resposta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def get_user_info(self, access_token):
        """Obtém informações do usuário autenticado"""
        url = 'https://api.linkedin.com/v2/me'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Erro ao obter dados do usuário: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    def run_oauth_flow(self):
        """Executa fluxo OAuth completo"""
        print("🚀 Iniciando processo de autorização LinkedIn...")
        print("=" * 60)
        
        # Carregar credenciais
        if not self.load_credentials():
            return None
        
        # Iniciar servidor callback
        server = self.start_callback_server()
        
        # Gerar URL de autorização
        auth_url = self.get_authorization_url()
        
        print(f"\n📱 Abrindo navegador para autorização...")
        print(f"Se não abrir automaticamente, acesse: {auth_url}")
        
        # Abrir navegador
        webbrowser.open(auth_url)
        
        # Aguardar callback
        print("\n⏳ Aguardando autorização... (você tem 5 minutos)")
        
        start_time = time.time()
        timeout = 300  # 5 minutos
        
        while time.time() - start_time < timeout:
            if hasattr(server, 'auth_code') and server.auth_code:
                print("✅ Código de autorização recebido!")
                break
            elif hasattr(server, 'auth_error') and server.auth_error:
                print(f"❌ Erro na autorização: {server.auth_error}")
                server.shutdown()
                return None
            
            time.sleep(1)
        else:
            print("⏰ Timeout: autorização não recebida em 5 minutos")
            server.shutdown()
            return None
        
        auth_code = server.auth_code
        server.shutdown()
        
        # Trocar código por token
        print("🔄 Trocando código por access token...")
        token_data = self.exchange_code_for_token(auth_code)
        
        if not token_data:
            return None
        
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 0)
        
        print(f"✅ Access token obtido! (válido por {expires_in} segundos)")
        
        # Obter informações do usuário
        print("👤 Obtendo informações do usuário...")
        user_info = self.get_user_info(access_token)
        
        if user_info:
            person_id = f"urn:li:person:{user_info['id']}"
            first_name = user_info.get('localizedFirstName', 'N/A')
            last_name = user_info.get('localizedLastName', 'N/A')
            
            print(f"📋 Usuário: {first_name} {last_name}")
            print(f"🆔 Person ID: {person_id}")
            
            # Salvar configuração
            config = {
                "linkedin_access_token": access_token,
                "linkedin_person_id": person_id,
                "post_interval_minutes": 60,
                "random_delay_minutes": 15,
                "topics": [
                    "segurança_da_informação",
                    "forense_computacional",
                    "forense_digital",
                    "cibersegurança",
                    "golpes_digitais"
                ],
                "max_posts_per_day": 24,
                "working_hours_only": False,
                "working_hours_start": 9,
                "working_hours_end": 18,
                "post_immediately": False
            }
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("💾 Configuração salva em 'config.json'")
            print("\n🎉 Processo concluído com sucesso!")
            print("Agora você pode executar: python linkedin_automation.py")
            
            return {
                'access_token': access_token,
                'person_id': person_id,
                'user_info': user_info
            }
        
        return None

def main():
    """Função principal"""
    print("🔑 LinkedIn Token Helper")
    print("=" * 30)
    print("Este script irá te ajudar a obter um access token do LinkedIn\n")
    
    helper = LinkedInTokenHelper()
    result = helper.run_oauth_flow()
    
    if result:
        print("\n✅ Sucesso! Você já pode usar a automação do LinkedIn.")
    else:
        print("\n❌ Falha ao obter token. Tente novamente.")

if __name__ == "__main__":
    main()