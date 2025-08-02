#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test version of LinkedIn Automation Tool
Works with built-in Python modules only
"""

import json
import random
import time
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

# Mock schedule module for testing
class MockSchedule:
    def __init__(self):
        self.jobs = []
    
    def every(self, interval):
        return MockJob(interval)
    
    def run_pending(self):
        print(f"🔄 Verificando {len(self.jobs)} tarefas agendadas...")
        
class MockJob:
    def __init__(self, interval):
        self.interval = interval
        
    def minutes(self):
        return MockJob(f"{self.interval} minutes")
        
    def do(self, func):
        print(f"✅ Tarefa agendada: {func.__name__} a cada {self.interval}")
        return self

# Usar mock se schedule não disponível
try:
    import schedule
except ImportError:
    schedule = MockSchedule()

# Mock requests para teste
class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {"id": "test123", "localizedFirstName": "Test", "localizedLastName": "User"}
    
    def json(self):
        return self._json_data
    
    @property
    def text(self):
        return json.dumps(self._json_data)

class MockRequests:
    def __init__(self):
        self.Session = MockSession
    
    def get(self, url, **kwargs):
        print(f"📡 [MOCK] GET {url}")
        return MockResponse()
    
    def post(self, url, **kwargs):
        print(f"📡 [MOCK] POST {url}")
        if "ugcPosts" in url:
            return MockResponse(201, {"id": "post_123"})
        return MockResponse()

class MockSession:
    def __init__(self):
        pass
        
    def mount(self, prefix, adapter):
        pass
        
    def get(self, url, **kwargs):
        print(f"📡 [MOCK] Session GET {url}")
        return MockResponse()
        
    def post(self, url, **kwargs):
        print(f"📡 [MOCK] Session POST {url}")
        if "ugcPosts" in url:
            return MockResponse(201, {"id": "post_123"})
        return MockResponse()

# Usar mock se requests não disponível
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    requests = MockRequests()
    HTTPAdapter = object
    class Retry:
        def __init__(self, **kwargs):
            pass

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    """Configuração para LinkedIn API"""
    access_token: str
    person_id: str

class ContentDatabase:
    """Banco de dados de conteúdo sobre cibersegurança"""
    
    def __init__(self):
        self.security_topics = {
            "segurança_da_informação": [
                "🔐 A segurança da informação é fundamental no mundo digital atual. Proteger dados confidenciais não é apenas uma responsabilidade técnica, mas um compromisso com a confiança dos clientes. #SegurançaDaInformação #DataProtection",
                "🛡️ Implementar políticas de segurança robustas é como construir uma fortaleza digital. Cada camada de proteção adiciona valor à defesa contra ameaças cibernéticas. #CyberSecurity #InfoSec"
            ],
            "forense_computacional": [
                "🔍 A forense computacional é a arte de encontrar evidências digitais onde outros veem apenas bits e bytes. Cada arquivo deletado conta uma história. #ForenseComputacional #DigitalForensics",
                "💻 Na investigação forense digital, a preservação da cadeia de custódia é fundamental. Um erro pode invalidar toda a evidência coletada. #DigitalInvestigation #Forensics"
            ],
            "cibersegurança": [
                "🚨 Os ataques cibernéticos evoluem constantemente. Nossa defesa deve ser igualmente dinâmica e adaptável. #CyberSecurity #ThreatDetection",
                "🔧 Implementar Zero Trust não é apenas instalar ferramentas, é mudar a mentalidade: 'nunca confie, sempre verifique'. #ZeroTrust #Security"
            ]
        }

    def get_random_content(self, topic: str = None) -> str:
        """Obtém conteúdo aleatório baseado no tópico especificado"""
        if topic and topic in self.security_topics:
            return random.choice(self.security_topics[topic])
        
        # Se não especificado, escolhe qualquer tópico
        all_content = []
        for topic_content in self.security_topics.values():
            all_content.extend(topic_content)
        
        return random.choice(all_content)

class LinkedInAutomationTest:
    """Versão de teste da automação do LinkedIn"""
    
    def __init__(self):
        self.config = {
            "linkedin_access_token": "TEST_TOKEN",
            "linkedin_person_id": "urn:li:person:TEST_ID",
            "post_interval_minutes": 60,
            "topics": ["segurança_da_informação", "forense_computacional", "cibersegurança"]
        }
        self.content_db = ContentDatabase()
        self.post_history = []
        
        # Configurar sessão mock
        if hasattr(requests, 'Session'):
            self.session = requests.Session()
        else:
            self.session = MockSession()
    
    def create_post(self, content: str) -> bool:
        """Simula criação de uma publicação no LinkedIn"""
        if not content:
            logger.error("Conteúdo vazio fornecido para publicação")
            return False
        
        print(f"\n📝 SIMULANDO POST NO LINKEDIN:")
        print(f"┌─ Conteúdo: {content[:100]}...")
        print(f"└─ Status: ✅ Post criado com sucesso (MODO TESTE)")
        
        # Simular resposta da API
        self.post_history.append({
            'timestamp': datetime.now().isoformat(),
            'content': content[:100] + "..." if len(content) > 100 else content,
            'status': 'success'
        })
        
        return True
    
    def run_single_post(self):
        """Executa uma única publicação de teste"""
        try:
            # Escolher tópico aleatório
            topics = self.config.get('topics', list(self.content_db.security_topics.keys()))
            topic = random.choice(topics)
            
            logger.info(f"📋 Tópico selecionado: {topic}")
            
            # Gerar conteúdo
            content = self.content_db.get_random_content(topic)
            
            # Criar publicação
            success = self.create_post(content)
            
            if success:
                logger.info(f"✅ Post sobre '{topic}' publicado com sucesso!")
            else:
                logger.error("❌ Falha ao publicar post")
                
        except Exception as e:
            logger.error(f"❌ Erro durante execução de post: {e}")
    
    def test_content_generation(self):
        """Testa geração de conteúdo para todos os tópicos"""
        print("\n🧪 TESTANDO GERAÇÃO DE CONTEÚDO")
        print("=" * 50)
        
        for topic in self.content_db.security_topics.keys():
            content = self.content_db.get_random_content(topic)
            print(f"\n📌 {topic.upper()}:")
            print(f"   {content}")
    
    def start_automation_test(self):
        """Inicia teste da automação"""
        logger.info("🚀 Iniciando teste de automação...")
        
        # Testar geração de conteúdo
        self.test_content_generation()
        
        # Simular alguns posts
        print(f"\n🔄 SIMULANDO POSTS AUTOMÁTICOS")
        print("=" * 50)
        
        for i in range(3):
            print(f"\n⏰ Post {i+1}/3:")
            self.run_single_post()
            time.sleep(1)  # Pequena pausa para visualização
        
        # Mostrar estatísticas
        print(f"\n📊 ESTATÍSTICAS FINAIS")
        print("=" * 30)
        print(f"Total de posts: {len(self.post_history)}")
        print(f"Posts com sucesso: {sum(1 for p in self.post_history if p['status'] == 'success')}")
        
        logger.info("✅ Teste de automação concluído!")

def main():
    """Função principal de teste"""
    print("🧪 LinkedIn Automation Tool - MODO TESTE")
    print("=" * 50)
    print("Este é um teste da automação sem conexão real com LinkedIn\n")
    
    # Verificar se é modo de teste
    print("📋 Informações do sistema:")
    print(f"   Python: Disponível ✅")
    print(f"   Requests: {'Disponível' if 'MockRequests' not in str(type(requests)) else 'Mock (sem conexão)'}")
    print(f"   Schedule: {'Disponível' if 'MockSchedule' not in str(type(schedule)) else 'Mock'}")
    
    # Criar e executar teste
    automation = LinkedInAutomationTest()
    
    try:
        automation.start_automation_test()
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
    
    print(f"\n🎉 Teste concluído! Para usar com LinkedIn real:")
    print("   1. Instale dependências: pip install requests schedule")
    print("   2. Configure LinkedIn API no config.json")
    print("   3. Execute: python linkedin_automation.py")

if __name__ == "__main__":
    main()