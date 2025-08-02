# 🤖 LinkedIn Automation Tool - Cibersegurança

Ferramenta de automação para publicações automáticas no LinkedIn focada em conteúdo de segurança da informação, forense computacional, forense digital, cibersegurança e golpes digitais.

## 🎯 Características

- ✅ **Postagens Automáticas**: Publicações a cada 60 minutos (configurável)
- 🔄 **Rotação de Conteúdo**: 5 categorias de segurança cibernética
- 🎲 **Randomização**: Delays aleatórios para comportamento natural
- 📊 **Monitoramento**: Logs detalhados e estatísticas
- ⚙️ **Configurável**: Horários de trabalho, limites diários, tópicos
- 🛡️ **Seguro**: Rate limiting e tratamento de erros robusto
- 🔗 **OAuth 2.0**: Autenticação segura com LinkedIn

## 📋 Conteúdo Incluído

### Tópicos de Segurança:

1. **Segurança da Informação** - Políticas, gestão de riscos, classificação de dados
2. **Forense Computacional** - Investigação digital, análise de malware, cadeia de custódia
3. **Forense Digital** - Recuperação de dados, análise de metadados, forense em nuvem
4. **Cibersegurança** - Zero Trust, DevSecOps, threat hunting, SOC
5. **Golpes Digitais** - Phishing, deepfakes, fraudes mobile, ataques API

### Tipos de Post:
- 💡 Dicas de segurança
- 📊 Insights da indústria
- 🔍 Análises técnicas
- ⚠️ Alertas de ameaças
- 🎓 Conteúdo educacional

## 🚀 Instalação Rápida

### 1. Clone ou baixe os arquivos

```bash
git clone <repository-url>
cd linkedin-automation
```

### 2. Instale dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o launcher

```bash
python run_automation.py
```

O launcher irá guiá-lo através do processo de configuração!

## 📁 Estrutura do Projeto

```
linkedin-automation/
├── 📜 linkedin_automation.py      # Script principal
├── 🚀 run_automation.py          # Launcher com menu
├── 🔑 linkedin_token_helper.py   # Auxiliar para OAuth
├── 📋 requirements.txt           # Dependências Python
├── ⚙️ config_example.json       # Exemplo de configuração
├── 📖 setup_guide.md            # Guia detalhado
└── 📄 README.md                 # Este arquivo
```

## ⚙️ Configuração

### Configuração Automática (Recomendada)

```bash
python run_automation.py
# Escolha opção 2: "Configurar token LinkedIn"
```

### Configuração Manual

1. **Criar aplicação LinkedIn**:
   - Acesse [LinkedIn Developer Portal](https://developer.linkedin.com/)
   - Crie nova aplicação
   - Solicite produtos: "Share on LinkedIn" e "Sign In with LinkedIn"

2. **Copiar configuração**:
   ```bash
   cp config_example.json config.json
   ```

3. **Editar config.json** com suas credenciais

### Parâmetros de Configuração

```json
{
  "linkedin_access_token": "SEU_TOKEN_AQUI",
  "linkedin_person_id": "urn:li:person:SEU_ID",
  "post_interval_minutes": 60,        // Intervalo entre posts
  "random_delay_minutes": 15,         // Delay aleatório adicional
  "topics": [...],                    // Tópicos a rotacionar
  "max_posts_per_day": 24,           // Limite diário
  "working_hours_only": false,        // Apenas horário comercial
  "working_hours_start": 9,           // Início do expediente
  "working_hours_end": 18            // Fim do expediente
}
```

## 🎯 Uso

### Via Launcher (Recomendado)

```bash
python run_automation.py
```

Menu interativo com opções:
1. 🚀 Iniciar automação
2. 🔧 Configurar token LinkedIn  
3. 📊 Testar conexão
4. 📋 Verificar configuração
5. 📖 Abrir documentação
6. ❌ Sair

### Via Script Direto

```bash
python linkedin_automation.py
```

### Execução em Background

**Linux/Mac:**
```bash
nohup python linkedin_automation.py &
```

**Windows:**
- Use Task Scheduler
- Ou execute em terminal dedicado

## 📊 Monitoramento

### Logs

- **Console**: Output em tempo real
- **Arquivo**: `linkedin_automation.log`

### Estatísticas Disponíveis

- Total de posts realizados
- Posts do dia atual  
- Taxa de sucesso
- Último post realizado
- Histórico de posts

### Exemplo de Log

```
2024-01-15 14:30:15 - INFO - Automação iniciada! Posts a cada 60 minutos
2024-01-15 14:30:15 - INFO - Pressione Ctrl+C para parar
2024-01-15 15:30:20 - INFO - Aguardando 487 segundos antes de postar...
2024-01-15 15:38:27 - INFO - Publicação criada com sucesso no LinkedIn!
2024-01-15 15:38:27 - INFO - Post sobre 'cibersegurança' publicado com sucesso!
```

## 🛡️ Recursos de Segurança

### Proteções Implementadas

- ✅ **Rate Limiting**: Respeita limites da API LinkedIn
- ✅ **Retry Logic**: Retentatimas automáticas em falhas
- ✅ **Error Handling**: Tratamento robusto de erros
- ✅ **Randomização**: Delays aleatórios (comportamento natural)
- ✅ **Logging**: Registro completo de atividades
- ✅ **Validation**: Validação de configurações
- ✅ **Timeout**: Timeouts em requisições HTTP

### Limites da API LinkedIn

- **Posts por hora**: Máximo 25
- **Posts por dia**: Máximo 100  
- **Requests por hora**: Máximo 500

O sistema automaticamente respeita estes limites.

## 🎨 Personalização

### Adicionando Conteúdo

1. **Edite `linkedin_automation.py`**
2. **Localize a classe `ContentDatabase`**
3. **Adicione novos tópicos**:

```python
"meu_topico": [
    "📝 Seu conteúdo aqui #HashTag",
    "🔥 Outro post interessante #Security"
]
```

### Modificando Intervalos

```json
{
  "post_interval_minutes": 120,    // Posts a cada 2 horas
  "random_delay_minutes": 30       // Delay até 30 minutos
}
```

### Horário de Trabalho

```json
{
  "working_hours_only": true,
  "working_hours_start": 8,
  "working_hours_end": 17
}
```

## 🔧 Solução de Problemas

### Erro de Autenticação

```
❌ Erro de autenticação: 401
```

**Soluções:**
- Verifique se o access token está correto
- Confirme se os produtos LinkedIn foram aprovados
- Gere novo token se necessário

### Falhas de Post

```
❌ Erro ao criar publicação: 429 - Rate limit exceeded
```

**Soluções:**
- Aguarde alguns minutos
- Reduza frequência de posts
- Verifique limite diário

### Problemas de Conexão

```
❌ Erro de conexão ao criar publicação
```

**Soluções:**
- Verifique conexão com internet
- Confirme se não há firewall bloqueando
- Teste conectividade: `python -c "import requests; print(requests.get('https://api.linkedin.com').status_code)"`

### Dependências em Falta

```
❌ Pacotes Python necessários não encontrados
```

**Solução:**
```bash
pip install -r requirements.txt
```

## 📈 Otimizações Recomendadas

### 1. Horários de Pico
Configure para postar quando sua audiência está online:
- Segunda a sexta: 8h-18h
- Terça/quarta/quinta: melhores dias
- Evite fins de semana para conteúdo B2B

### 2. Frequência Ideal
- **Inicial**: 1 post por hora
- **Crescimento**: 1 post a cada 2-3 horas  
- **Estabilidade**: 3-5 posts por dia

### 3. Variação de Conteúdo
- Alterne entre dicas práticas e insights
- Use hashtags específicas (#InfoSec, #CyberSecurity)
- Inclua emojis para maior engajamento

### 4. Monitoramento
- Acompanhe métricas de engajamento
- Ajuste horários baseado na audiência
- Responda comentários para aumentar alcance

## ⚖️ Considerações Legais

- ✅ Use apenas em sua própria conta LinkedIn
- ✅ Respeite os [Termos de Uso do LinkedIn](https://www.linkedin.com/legal/user-agreement)
- ✅ Não faça spam ou posts excessivos
- ✅ Mantenha conteúdo relevante e de qualidade
- ✅ Não use para contas de terceiros sem autorização

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Adicione testes se necessário
5. Submeta um Pull Request

### Áreas para Contribuição

- 🎨 Novos templates de conteúdo
- 🤖 Integração com IA (OpenAI, Claude)
- 📊 Dashboard de métricas
- 🔗 Integração com outras redes sociais
- 🛡️ Melhorias de segurança

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 📞 Suporte

Para problemas ou dúvidas:

1. 📖 Consulte o [Setup Guide](setup_guide.md)
2. 📋 Verifique os logs em `linkedin_automation.log`
3. 🔍 Revise configurações em `config.json`
4. 🐛 Abra uma issue no repositório

## 🎉 Próximas Funcionalidades

- [ ] Dashboard web para monitoramento
- [ ] Integração com OpenAI para geração de conteúdo
- [ ] Análise de sentimento dos posts
- [ ] Agendamento de posts específicos
- [ ] Integração com outras plataformas (Twitter, Instagram)
- [ ] Sistema de templates personalizáveis
- [ ] Métricas de engajamento
- [ ] Backup automático de configurações

---

**🚀 Desenvolvido para profissionais de cibersegurança que querem manter presença ativa no LinkedIn!**

⭐ Se este projeto foi útil, considere dar uma estrela no repositório! 
