#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Automation Tool for Cybersecurity Content
Criado para automatizar publicações no LinkedIn sobre segurança da informação
"""

import json
import random
import time
import schedule
import logging
import os
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    """Configuração para LinkedIn API"""
    access_token: str
    person_id: str  # LinkedIn person URN
    
@dataclass
class ContentConfig:
    """Configuração para geração de conteúdo"""
    openai_api_key: str = ""
    topics: List[str] = None
    use_ai: bool = False

class ContentDatabase:
    """Banco de dados de conteúdo sobre cibersegurança"""
    
    def __init__(self):
        self.security_topics = {
            "segurança_da_informação": [
                "🔐 A segurança da informação é fundamental no mundo digital atual. Proteger dados confidenciais não é apenas uma responsabilidade técnica, mas um compromisso com a confiança dos clientes. #SegurançaDaInformação #DataProtection",
                "🛡️ Implementar políticas de segurança robustas é como construir uma fortaleza digital. Cada camada de proteção adiciona valor à defesa contra ameaças cibernéticas. #CyberSecurity #InfoSec",
                "📊 A gestão de riscos em segurança da informação requer análise contínua e adaptação às novas ameaças. Estar preparado é a melhor defesa. #RiskManagement #Security",
                "🔒 A classificação adequada de dados é o primeiro passo para uma estratégia de segurança eficaz. Nem toda informação precisa do mesmo nível de proteção. #DataClassification #InformationSecurity",
                "🌐 Com o aumento do trabalho remoto, a segurança de endpoints tornou-se ainda mais crítica. Proteger cada dispositivo é proteger toda a rede. #EndpointSecurity #RemoteWork"
            ],
            "forense_computacional": [
                "🔍 A forense computacional é a arte de encontrar evidências digitais onde outros veem apenas bits e bytes. Cada arquivo deletado conta uma história. #ForenseComputacional #DigitalForensics",
                "💻 Na investigação forense digital, a preservação da cadeia de custódia é fundamental. Um erro pode invalidar toda a evidência coletada. #DigitalInvestigation #Forensics",
                "🕵️ A análise de malware revela as técnicas e motivações dos atacantes. Compreender o inimigo é essencial para fortalecer nossas defesas. #MalwareAnalysis #ThreatIntelligence",
                "📱 Com dispositivos móveis armazenando cada vez mais dados pessoais, a forense mobile tornou-se uma especialidade crucial. #MobileForensics #CyberInvestigation",
                "⚖️ A forense computacional não é apenas técnica, mas também jurídica. Entender as leis é tão importante quanto dominar as ferramentas. #LegalTech #DigitalEvidence"
            ],
            "forense_digital": [
                "🔬 A forense digital moderna combina técnicas tradicionais com inteligência artificial para análise mais eficiente de grandes volumes de dados. #DigitalForensics #AI",
                "💾 A recuperação de dados apagados é uma das habilidades mais valiosas em forense digital. O que parece perdido pode ser crucial para o caso. #DataRecovery #Forensics",
                "🌊 A forense em nuvem apresenta desafios únicos: jurisdição, acesso aos dados e preservação de evidências em ambientes distribuídos. #CloudForensics #CyberSecurity",
                "🔐 A criptografia pode proteger dados, mas também pode esconder evidências. A forense precisa equilibrar privacidade e justiça. #Encryption #DigitalRights",
                "📸 A análise de metadados pode revelar informações surpreendentes sobre arquivos digitais, desde localização até equipamento usado. #Metadata #OSINT"
            ],
            "cibersegurança": [
                "🚨 Os ataques cibernéticos evoluem constantemente. Nossa defesa deve ser igualmente dinâmica e adaptável. #CyberSecurity #ThreatDetection",
                "🔧 Implementar Zero Trust não é apenas instalar ferramentas, é mudar a mentalidade: 'nunca confie, sempre verifique'. #ZeroTrust #Security",
                "🌐 A segurança em DevOps (DevSecOps) integra proteção desde o desenvolvimento. Segurança não pode ser uma reflexão tardia. #DevSecOps #SecureCode",
                "📈 O SOC (Security Operations Center) é o coração da defesa cibernética moderna. Monitoramento 24/7 faz toda a diferença. #SOC #CyberDefense",
                "🎯 Threat hunting é a busca proativa por ameaças na rede. Não podemos apenas reagir, precisamos antecipar. #ThreatHunting #ProactiveSecurity"
            ],
            "golpes_digitais": [
                "⚠️ O phishing evoluiu: não são apenas emails suspeitos, mas mensagens sofisticadas que imitam perfeitamente empresas legítimas. #Phishing #SocialEngineering",
                "📱 Golpes via WhatsApp e SMS aumentaram 300% no último ano. A educação do usuário é nossa melhor defesa. #SMSFraud #DigitalScams",
                "💳 O skimming digital permite roubo de dados de cartão sem contato físico. A tecnologia que facilita também pode expor. #DigitalSkimming #FinancialSecurity",
                "🎭 Deepfakes estão sendo usados em golpes de romance e fraudes empresariais. A realidade digital precisa ser questionada. #Deepfakes #SocialEngineering",
                "🏦 Ataques a APIs bancárias cresceram exponentially. A segurança precisa acompanhar a inovação financeira. #APIlSecurity #FinTech"
            ]
        }
        
        self.tips_security = [
            "💡 Dica de Segurança: Use autenticação multifator sempre que possível. É um pequeno inconveniente que pode evitar grandes problemas.",
            "🔐 Lembre-se: uma senha forte tem pelo menos 12 caracteres, mistura letras, números e símbolos, e é única para cada conta.",
            "📲 Mantenha seus aplicativos sempre atualizados. Patches de segurança são sua primeira linha de defesa contra vulnerabilidades conhecidas.",
            "🔍 Antes de clicar em links, verifique o remetente e a URL. Quando em dúvida, acesse o site diretamente pelo navegador.",
            "💾 Backup regular dos dados importantes. O ransomware pode criptografar seus arquivos, mas não pode apagar seus backups seguros."
        ]
        
        self.industry_insights = [
            "📊 O mercado de cibersegurança deve atingir $267 bilhões até 2026. A demanda por profissionais qualificados nunca foi tão alta.",
            "🎓 Certificações como CISSP, CEH e CISA continuam sendo diferenciais importantes na carreira de segurança.",
            "🌍 Regulamentações como LGPD no Brasil e GDPR na Europa mudaram como empresas lidam com dados pessoais.",
            "🤖 IA está revolucionando tanto ataques quanto defesas cibernéticas. É uma corrida armamentista digital.",
            "☁️ Migração para nuvem trouxe novos desafios de segurança. Responsabilidade compartilhada requer compreensão clara."
        ]

    def get_random_content(self, topic: str = None) -> str:
        """Obtém conteúdo aleatório baseado no tópico especificado"""
        if topic and topic in self.security_topics:
            return random.choice(self.security_topics[topic])
        
        # Se não especificado, escolhe qualquer tópico
        all_content = []
        for topic_content in self.security_topics.values():
            all_content.extend(topic_content)
        all_content.extend(self.tips_security)
        all_content.extend(self.industry_insights)
        
        return random.choice(all_content)

class LinkedInAutomation:
    """Classe principal para automação do LinkedIn"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self._load_config(config_file)
        self.content_db = ContentDatabase()
        self.last_post_time = None
        self.post_history = []
        
        # Configurar sessão HTTP com retry
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Carrega configuração do arquivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_fields = ['linkedin_access_token', 'linkedin_person_id']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Campo obrigatório '{field}' não encontrado na configuração")
            
            return config
        except FileNotFoundError:
            logger.error(f"Arquivo de configuração {config_file} não encontrado")
            return self._create_default_config(config_file)
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON do arquivo {config_file}")
            raise
            
    def _create_default_config(self, config_file: str) -> Dict[str, Any]:
        """Cria arquivo de configuração padrão"""
        default_config = {
            "linkedin_access_token": "SEU_ACCESS_TOKEN_AQUI",
            "linkedin_person_id": "SEU_PERSON_ID_AQUI",
            "post_interval_minutes": 60,
            "random_delay_minutes": 15,
            "topics": [
                "segurança_da_informação",
                "forense_computacional", 
                "forense_digital",
                "cibersegurança",
                "golpes_digitais"
            ],
            "openai_api_key": "",
            "use_ai_content": False,
            "max_posts_per_day": 24,
            "working_hours_only": False,
            "working_hours_start": 9,
            "working_hours_end": 18
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Arquivo de configuração padrão criado: {config_file}")
        logger.info("Por favor, edite o arquivo com suas credenciais do LinkedIn")
        return default_config
    
    def _generate_ai_content(self, topic: str) -> str:
        """Gera conteúdo usando OpenAI (se configurado)"""
        if not self.config.get('use_ai_content') or not self.config.get('openai_api_key'):
            return self.content_db.get_random_content(topic)
            
        try:
            # Aqui você integraria com OpenAI
            # Por enquanto, retorna conteúdo do banco de dados
            logger.info("Geração de conteúdo IA não implementada, usando banco de dados local")
            return self.content_db.get_random_content(topic)
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo IA: {e}")
            return self.content_db.get_random_content(topic)
    
    def create_post(self, content: str) -> bool:
        """Cria uma publicação no LinkedIn"""
        if not content:
            logger.error("Conteúdo vazio fornecido para publicação")
            return False
            
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            'Authorization': f'Bearer {self.config["linkedin_access_token"]}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        post_data = {
            "author": self.config["linkedin_person_id"],
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = self.session.post(url, headers=headers, json=post_data, timeout=30)
            
            if response.status_code == 201:
                logger.info("Publicação criada com sucesso no LinkedIn!")
                self.last_post_time = datetime.now()
                self.post_history.append({
                    'timestamp': self.last_post_time.isoformat(),
                    'content': content[:100] + "..." if len(content) > 100 else content,
                    'status': 'success'
                })
                return True
            else:
                logger.error(f"Erro ao criar publicação: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão ao criar publicação: {e}")
            return False
    
    def should_post_now(self) -> bool:
        """Verifica se deve postar agora baseado nas configurações"""
        now = datetime.now()
        
        # Verificar horário de trabalho
        if self.config.get('working_hours_only', False):
            start_hour = self.config.get('working_hours_start', 9)
            end_hour = self.config.get('working_hours_end', 18)
            
            if now.hour < start_hour or now.hour >= end_hour:
                return False
                
        # Verificar limite diário de posts
        today_posts = [p for p in self.post_history 
                      if datetime.fromisoformat(p['timestamp']).date() == now.date()]
        
        max_daily = self.config.get('max_posts_per_day', 24)
        if len(today_posts) >= max_daily:
            logger.info(f"Limite diário de {max_daily} posts atingido")
            return False
            
        return True
    
    def run_single_post(self):
        """Executa uma única publicação"""
        if not self.should_post_now():
            return
            
        try:
            # Escolher tópico aleatório
            topics = self.config.get('topics', list(self.content_db.security_topics.keys()))
            topic = random.choice(topics)
            
            # Gerar conteúdo
            content = self._generate_ai_content(topic)
            
            # Adicionar delay aleatório se configurado
            random_delay = self.config.get('random_delay_minutes', 0)
            if random_delay > 0:
                delay = random.randint(0, random_delay * 60)
                logger.info(f"Aguardando {delay} segundos antes de postar...")
                time.sleep(delay)
            
            # Criar publicação
            success = self.create_post(content)
            
            if success:
                logger.info(f"Post sobre '{topic}' publicado com sucesso!")
            else:
                logger.error("Falha ao publicar post")
                
        except Exception as e:
            logger.error(f"Erro durante execução de post: {e}")
    
    def start_automation(self):
        """Inicia a automação com agendamento"""
        interval = self.config.get('post_interval_minutes', 60)
        
        # Agendar posts regulares
        schedule.every(interval).minutes.do(self.run_single_post)
        
        logger.info(f"Automação iniciada! Posts a cada {interval} minutos")
        logger.info("Pressione Ctrl+C para parar")
        
        # Executar um post inicial (opcional)
        if self.config.get('post_immediately', False):
            logger.info("Executando post inicial...")
            self.run_single_post()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
        except KeyboardInterrupt:
            logger.info("Automação interrompida pelo usuário")
        except Exception as e:
            logger.error(f"Erro durante automação: {e}")
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API do LinkedIn"""
        url = "https://api.linkedin.com/v2/me"
        headers = {
            'Authorization': f'Bearer {self.config["linkedin_access_token"]}',
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Conexão OK! Usuário: {user_data.get('localizedFirstName', 'N/A')} {user_data.get('localizedLastName', 'N/A')}")
                return True
            else:
                logger.error(f"Erro de autenticação: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da automação"""
        total_posts = len(self.post_history)
        today_posts = len([p for p in self.post_history 
                          if datetime.fromisoformat(p['timestamp']).date() == datetime.now().date()])
        
        successful_posts = len([p for p in self.post_history if p['status'] == 'success'])
        
        return {
            'total_posts': total_posts,
            'today_posts': today_posts,
            'successful_posts': successful_posts,
            'success_rate': (successful_posts / total_posts * 100) if total_posts > 0 else 0,
            'last_post': self.last_post_time.isoformat() if self.last_post_time else None
        }

def main():
    """Função principal"""
    print("🤖 LinkedIn Automation Tool - Cibersegurança")
    print("=" * 50)
    
    # Criar instância da automação
    automation = LinkedInAutomation()
    
    # Testar conexão
    print("Testando conexão com LinkedIn...")
    if not automation.test_connection():
        print("❌ Falha na conexão. Verifique suas credenciais no arquivo config.json")
        return
    
    print("✅ Conexão estabelecida com sucesso!")
    
    # Mostrar configurações
    interval = automation.config.get('post_interval_minutes', 60)
    topics = automation.config.get('topics', [])
    print(f"\n📋 Configurações:")
    print(f"   Intervalo entre posts: {interval} minutos")
    print(f"   Tópicos: {', '.join(topics)}")
    
    # Perguntar se deseja continuar
    response = input("\n🚀 Iniciar automação? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        automation.start_automation()
    else:
        print("Automação cancelada.")

if __name__ == "__main__":
    main()