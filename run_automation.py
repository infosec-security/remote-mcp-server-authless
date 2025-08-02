#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher Script para LinkedIn Automation
Script simples para iniciar a automação
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    required_packages = ['requests', 'schedule']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Pacotes Python necessários não encontrados:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Instale com: pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """Verifica se o arquivo de configuração existe e está válido"""
    if not os.path.exists('config.json'):
        print("❌ Arquivo config.json não encontrado")
        print("📝 Execute primeiro: python linkedin_token_helper.py")
        print("📄 Ou copie config_example.json para config.json e edite")
        return False
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_fields = ['linkedin_access_token', 'linkedin_person_id']
        for field in required_fields:
            if field not in config:
                print(f"❌ Campo '{field}' não encontrado em config.json")
                return False
            
            if config[field] in ['SEU_ACCESS_TOKEN_AQUI', 'SEU_PERSON_ID_AQUI', '']:
                print(f"❌ Campo '{field}' precisa ser configurado em config.json")
                return False
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Erro ao ler config.json - arquivo JSON inválido")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar configuração: {e}")
        return False

def show_menu():
    """Mostra menu de opções"""
    print("🤖 LinkedIn Automation Launcher")
    print("=" * 40)
    print("1. 🚀 Iniciar automação")
    print("2. 🔧 Configurar token LinkedIn")
    print("3. 📊 Testar conexão")
    print("4. 📋 Verificar configuração")
    print("5. 📖 Abrir documentação")
    print("6. ❌ Sair")
    print()

def test_connection():
    """Testa conexão com LinkedIn"""
    try:
        from linkedin_automation import LinkedInAutomation
        
        automation = LinkedInAutomation()
        success = automation.test_connection()
        
        if success:
            print("✅ Conexão com LinkedIn OK!")
            
            # Mostrar estatísticas se houver histórico
            stats = automation.get_stats()
            if stats['total_posts'] > 0:
                print(f"📊 Estatísticas:")
                print(f"   Total de posts: {stats['total_posts']}")
                print(f"   Posts hoje: {stats['today_posts']}")
                print(f"   Taxa de sucesso: {stats['success_rate']:.1f}%")
        else:
            print("❌ Falha na conexão com LinkedIn")
            print("Verifique suas credenciais em config.json")
            
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")

def show_config():
    """Mostra configuração atual"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 Configuração atual:")
        print(f"   Intervalo entre posts: {config.get('post_interval_minutes', 60)} minutos")
        print(f"   Delay aleatório: {config.get('random_delay_minutes', 0)} minutos")
        print(f"   Máximo posts/dia: {config.get('max_posts_per_day', 24)}")
        print(f"   Apenas horário comercial: {config.get('working_hours_only', False)}")
        
        if config.get('working_hours_only'):
            start = config.get('working_hours_start', 9)
            end = config.get('working_hours_end', 18)
            print(f"   Horário de trabalho: {start}h às {end}h")
        
        topics = config.get('topics', [])
        print(f"   Tópicos: {', '.join(topics)}")
        
    except Exception as e:
        print(f"❌ Erro ao ler configuração: {e}")

def open_documentation():
    """Abre documentação"""
    if os.path.exists('setup_guide.md'):
        print("📖 Abrindo documentação...")
        
        # Tentar abrir com diferentes programas
        if sys.platform.startswith('win'):
            os.startfile('setup_guide.md')
        elif sys.platform.startswith('darwin'):  # macOS
            subprocess.run(['open', 'setup_guide.md'])
        else:  # Linux
            subprocess.run(['xdg-open', 'setup_guide.md'])
    else:
        print("❌ Arquivo setup_guide.md não encontrado")

def run_automation():
    """Executa a automação"""
    print("🚀 Iniciando automação LinkedIn...")
    print("=" * 40)
    
    try:
        from linkedin_automation import LinkedInAutomation
        
        automation = LinkedInAutomation()
        automation.start_automation()
        
    except KeyboardInterrupt:
        print("\n⏹️ Automação interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar automação: {e}")

def configure_token():
    """Configura token LinkedIn"""
    print("🔧 Configurando token LinkedIn...")
    
    try:
        import linkedin_token_helper
        linkedin_token_helper.main()
    except ImportError:
        print("❌ linkedin_token_helper.py não encontrado")
    except Exception as e:
        print(f"❌ Erro ao configurar token: {e}")

def main():
    """Função principal"""
    while True:
        print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        show_menu()
        
        try:
            choice = input("Escolha uma opção (1-6): ").strip()
            
            if choice == '1':
                if not check_requirements():
                    continue
                if not check_config():
                    continue
                run_automation()
                
            elif choice == '2':
                if not check_requirements():
                    continue
                configure_token()
                
            elif choice == '3':
                if not check_requirements():
                    continue
                if not check_config():
                    continue
                test_connection()
                
            elif choice == '4':
                if not check_config():
                    continue
                show_config()
                
            elif choice == '5':
                open_documentation()
                
            elif choice == '6':
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida. Escolha entre 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()