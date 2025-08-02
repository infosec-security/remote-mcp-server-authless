# 🤖 Guia de Configuração - LinkedIn Automation Tool

Este guia irá te ajudar a configurar e usar a automação de posts do LinkedIn focada em cibersegurança.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Conta do LinkedIn
- Aplicação LinkedIn Developer (será criada no processo)

## 🚀 Instalação

### 1. Clone ou baixe os arquivos

Certifique-se de ter os seguintes arquivos:
- `linkedin_automation.py` (script principal)
- `requirements.txt` (dependências)
- `config_example.json` (exemplo de configuração)

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🔧 Configuração do LinkedIn API

### Passo 1: Criar Aplicação LinkedIn

1. Acesse o [LinkedIn Developer Portal](https://developer.linkedin.com/)
2. Faça login com sua conta LinkedIn
3. Clique em "Create App"
4. Preencha as informações:
   - **App name**: "Minha Automação LinkedIn"
   - **LinkedIn Page**: Selecione sua página/perfil
   - **Description**: "Automação de posts sobre cibersegurança"
   - **App logo**: Upload de uma imagem (opcional)
   - **App website**: Seu site ou LinkedIn (se não tiver site)

### Passo 2: Solicitar Produtos

Na página da sua aplicação:

1. Vá para a aba "Products"
2. Solicite acesso aos seguintes produtos:
   - **Share on LinkedIn** (aprovação automática)
   - **Sign In with LinkedIn using OpenID Connect** (aprovação automática)

### Passo 3: Verificar Página LinkedIn

1. Na aba "Settings" da aplicação
2. Role até "LinkedIn Pages"
3. Clique em "Verify" na sua página
4. Siga as instruções para verificação

### Passo 4: Obter Credenciais

1. Na aba "Auth" da aplicação, anote:
   - **Client ID**
   - **Client Secret**

### Passo 5: Gerar Access Token

#### Método 1: Usando LinkedIn Developer Portal (Recomendado para teste)

1. Na aba "Auth" da aplicação
2. Role até "OAuth 2.0 settings"
3. Adicione uma URL de redirecionamento: `http://localhost:8080/callback`
4. Clique em "Update"
5. Use o "LinkedIn Token Generator" na própria página

#### Método 2: Fluxo OAuth Manual

1. Substitua `SEU_CLIENT_ID` pelo seu Client ID na URL abaixo:
```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=SEU_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=w_member_social%20r_liteprofile
```

2. Acesse a URL no navegador e autorize a aplicação
3. Copie o código da URL de retorno
4. Use o código para obter o access token via API

### Passo 6: Obter Person ID

Com o access token, faça uma requisição GET para:
```
https://api.linkedin.com/v2/me
```

No retorno, use o valor do campo `id` precedido de `urn:li:person:`.

## ⚙️ Configuração do Script

### 1. Copiar arquivo de configuração

```bash
cp config_example.json config.json
```

### 2. Editar config.json

Abra o arquivo `config.json` e configure:

```json
{
  "linkedin_access_token": "SEU_ACCESS_TOKEN_AQUI",
  "linkedin_person_id": "urn:li:person:SEU_PERSON_ID",
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
  "working_hours_only": false,
  "working_hours_start": 9,
  "working_hours_end": 18
}
```

### Parâmetros de Configuração:

- **linkedin_access_token**: Token de acesso obtido no LinkedIn
- **linkedin_person_id**: ID da pessoa no formato `urn:li:person:XXXXX`
- **post_interval_minutes**: Intervalo entre posts (60 = a cada hora)
- **random_delay_minutes**: Delay aleatório adicional (0-15 minutos)
- **topics**: Tópicos que serão alternados nos posts
- **max_posts_per_day**: Limite máximo de posts por dia
- **working_hours_only**: Se true, posta apenas em horário comercial
- **working_hours_start/end**: Horário comercial (24h format)

## 🎯 Executando a Automação

### Teste de Conexão

Primeiro, teste se tudo está funcionando:

```bash
python linkedin_automation.py
```

O script irá:
1. Testar a conexão com LinkedIn
2. Mostrar suas configurações
3. Perguntar se deseja iniciar a automação

### Execução Contínua

Para executar em background (Linux/Mac):

```bash
nohup python linkedin_automation.py &
```

Para Windows, use o Task Scheduler ou execute em um terminal dedicado.

## 📊 Monitoramento

### Logs

O script gera logs em:
- **Console**: Output em tempo real
- **Arquivo**: `linkedin_automation.log`

### Estatísticas

Durante a execução, você pode verificar:
- Total de posts realizados
- Posts do dia atual
- Taxa de sucesso
- Último post realizado

## 🛡️ Recursos de Segurança

### Proteções Implementadas:

1. **Rate Limiting**: Respeita limites da API LinkedIn
2. **Retry Logic**: Retentatimas automáticas em caso de falha
3. **Error Handling**: Tratamento robusto de erros
4. **Randomização**: Delays aleatórios para comportamento natural
5. **Logging**: Registro completo de atividades

### Limites da API LinkedIn:

- **Posts por hora**: Máximo 25
- **Posts por dia**: Máximo 100
- **Requests por hora**: Máximo 500

## 🎨 Personalizando Conteúdo

### Adicionando Novos Tópicos

No arquivo `linkedin_automation.py`, localize a classe `ContentDatabase` e adicione novos tópicos ao dicionário `security_topics`.

### Criando Conteúdo Personalizado

```python
"meu_topico": [
    "📝 Seu conteúdo personalizado aqui #HashTag",
    "🔥 Outro post interessante sobre o tema #Security"
]
```

### Integrando IA (OpenAI)

Para usar geração de conteúdo via IA:

1. Obtenha uma chave da API OpenAI
2. Configure no `config.json`:
```json
{
  "openai_api_key": "sua_chave_openai",
  "use_ai_content": true
}
```

## 🚨 Troubleshooting

### Erro de Autenticação
- Verifique se o access token está correto
- Confirme se os produtos LinkedIn foram aprovados
- Teste o token manualmente via API

### Falhas de Post
- Verifique limite de posts da API
- Confirme se o conteúdo não viola políticas LinkedIn
- Analise os logs para erro específico

### Problemas de Conexão
- Verifique conexão com internet
- Confirme se não há firewall bloqueando
- Teste conectividade com LinkedIn API

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique os logs em `linkedin_automation.log`
2. Consulte a documentação da LinkedIn API
3. Revise as configurações do arquivo `config.json`

## ⚖️ Considerações Legais

- Use apenas em sua própria conta LinkedIn
- Respeite os termos de uso do LinkedIn
- Não faça spam ou posts excessivos
- Mantenha o conteúdo relevante e de qualidade

## 📈 Otimizações Recomendadas

1. **Horários de Pico**: Configure para postar quando sua audiência está online
2. **Conteúdo Variado**: Alterne entre dicas, insights e novidades
3. **Hashtags Relevantes**: Use hashtags específicas do seu nicho
4. **Interação**: Monitor respostas e engajamento dos posts

---

✅ **Configuração concluída!** Sua automação LinkedIn está pronta para funcionar.