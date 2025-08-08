# Power BI Embedded - Projeto de Integração

Este projeto demonstra como integrar relatórios do Power BI em aplicações web usando Power BI Embedded.

## 📋 Pré-requisitos

### Licenciamento Power BI
- **Power BI Pro** ou **Power BI Premium** por usuário
- Ou **Power BI Premium** por capacidade (recomendado para produção)

### Conta Microsoft Azure
- Assinatura ativa do Azure
- Permissões para criar recursos no Azure Active Directory

## 🚀 Configuração Inicial

### 1. Criar Aplicação no Azure Active Directory

1. Acesse o [Portal do Azure](https://portal.azure.com)
2. Navegue para **Azure Active Directory** > **App registrations**
3. Clique em **New registration**
4. Configure:
   - **Name**: Nome da sua aplicação (ex: "PowerBI-Embedded-App")
   - **Supported account types**: Accounts in this organizational directory only

### 2. Configurar Permissões da Aplicação

Após criar a aplicação, configure as permissões necessárias:

#### API Permissions
1. Clique em **API permissions**
2. Adicione as seguintes permissões do **Power BI Service**:
   - `Tenant.Read.All` (Application)
   - `Tenant.ReadWrite.All` (Application)

#### Grant Admin Consent
3. Clique em **Grant admin consent** para aprovar as permissões

### 3. Configurar Autenticação

#### Client Secret
1. Vá para **Certificates & secrets**
2. Clique em **New client secret**
3. Defina um nome e prazo de validade
4. **⚠️ IMPORTANTE**: Copie e guarde o **Value** do secret imediatamente (não será mostrado novamente)

#### IDs Necessários
Anote os seguintes valores da aplicação:
- **Application (client) ID**
- **Directory (tenant) ID**
- **Client Secret Value**

## ⚙️ Configuração no Power BI Admin Portal

### 1. Habilitar APIs de Serviço

1. Acesse [Power BI Admin Portal](https://app.powerbi.com/admin-portal/tenantSettings?language=pt-BR&experience=power-bi)
2. Vá para **Tenant settings** (Configurações de locatário)
3. Na seção **Developer settings**, habilite:
   - **Embed content in apps** (Inserir conteúdo em aplicativos)
   - **Allow service principals to use Power BI APIs** (Os principais serviços podem chamar APIs públicas do Fabric)

### 2. Configurar novo workspace

1. Em **Manage access**(gerenciar acesso), acesse:
   - **Add people or groups**
   - Adicione exatamente o nome do seu azure app (Display name em **Overview** do azupe app)

## 📁 Estrutura do Projeto

```
powerbi-embedded/
├── index.html          # Interface web para exibir o relatório
├── generate_token.py   # Script Python para gerar tokens de embed
└── README.md          # Este arquivo
```

## 📄 Arquivos do Projeto

### generate_token.py
Script Python responsável por:
- Obter access token do Azure AD
- Gerar embed token específico para o relatório
- Exibir o token no console para uso no HTML




### Configuração do generate_token.py

O script Python inclui as seguintes funcionalidades:

1. **Autenticação OAuth2**: Obtém access token usando credenciais do Azure AD
2. **Geração de Embed Token**: Cria token específico para o relatório
3. **Tratamento de Erros**: Valida respostas da API

**Parâmetros configuráveis no arquivo:**
- `TENANT_ID`: ID do diretório Azure AD
- `CLIENT_ID`: ID da aplicação registrada
- `CLIENT_SECRET`: Secret da aplicação
- `WORKSPACE_ID`: ID do workspace do Power BI
- `REPORT_ID`: ID do relatório a ser incorporado

## 📊 Como Obter os IDs Necessários

### Workspace ID
1. Acesse [Power BI Service](https://app.powerbi.com)
2. Navegue até seu workspace
3. O ID estará na URL: `https://app.powerbi.com/groups/{WORKSPACE_ID}`

### Report ID
1. No workspace, clique no relatório desejado
2. O ID estará na URL: `https://app.powerbi.com/reports/{REPORT_ID}`

## 🔐 Tokens e Autenticação

### Access Token
- Token usado para autenticar com a API do Power BI
- Válido por 1 hora
- Gerado usando Client ID, Client Secret e Tenant ID

### Embed Token
- Token específico para incorporar relatórios
- Válido por 1 hora (padrão)
- Gerado usando o Access Token

## 🚦 Como Usar

### 1. Configurar Credenciais

**Opção 1 - Diretamente no código:**
Edite o arquivo `generate_token.py` e substitua os placeholders:

```python
TENANT_ID = "seu-tenant-id-aqui"
CLIENT_ID = "seu-client-id-aqui"
CLIENT_SECRET = "seu-client-secret-aqui"
WORKSPACE_ID = "seu-workspace-id-aqui"
REPORT_ID = "seu-report-id-aqui"
```

**Opção 2 - Usando arquivo .env (recomendado):**
Crie um arquivo `.env` e modifique o `generate_token.py` para usar `python-dotenv`.

### 2. Gerar Embed Token

Execute o script Python:

```bash
python generate_token.py
```

**Saída esperada:**
```
Obtendo access token do Azure AD...
Gerando embed token do Power BI...

Embed Token:

H4sIAAAAAAAEAG2VB2+CQBCF....(token longo)
```

### 3. Configurar index.html

Copie o embed token gerado e substitua os placeholders:

```javascript
var embedToken = "COLE_O_TOKEN_GERADO_AQUI";
var embedUrl = "https://app.powerbi.com/reportEmbed?reportId=SEU_REPORT_ID&groupId=SEU_WORKSPACE_ID";
var reportId = "SEU_REPORT_ID";
```

### 4. Executar a Aplicação

Abra o arquivo `index.html` em um navegador web ou use um servidor local:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server

# Live Server (VS Code)
# Instale a extensão Live Server e clique com botão direito no index.html
```

## 🔄 Fluxo de Autenticação

1. **Script Python** → Azure AD (OAuth2) → **Access Token**
2. **Access Token** → Power BI API → **Embed Token** 
3. **Embed Token** → JavaScript Client → **Relatório Incorporado**

**⏱️ Validade dos Tokens:**
- Access Token: 1 hora
- Embed Token: 1 hora (configurável até 24h)

## 🛠️ Exemplo de Configuração JavaScript

```javascript
var config = {
    type: 'report',
    tokenType: models.TokenType.Embed,
    accessToken: embedToken,
    embedUrl: embedUrl,
    id: reportId,
    permissions: models.Permissions.All,
    settings: {
        panes: {
            filters: { visible: false },
            pageNavigation: { visible: true }
        }
    }
};
```

## 🔍 Troubleshooting

### Erros Comuns

1. **"Unauthorized" (401)**: 
   - Verifique se as credenciais (Client ID, Secret, Tenant ID) estão corretas
   - Confirme se as permissões foram concedidas no Azure AD

2. **"Forbidden" (403)**: 
   - Confirme se o service principal foi adicionado ao workspace do Power BI
   - Verifique se as configurações do Power BI Admin Portal estão habilitadas

3. **"Token expired"**: 
   - Execute novamente o `generate_token.py` para obter um novo token
   - Tokens de embed são válidos por 1 hora

4. **"Report not found"**: 
   - Verifique se o REPORT_ID e WORKSPACE_ID estão corretos
   - Confirme se o relatório existe no workspace especificado

5. **Erro no Python - "requests.exceptions.HTTPError"**:
   - Adicione tratamento de erro mais detalhado:
   ```python
   try:
       response.raise_for_status()
   except requests.exceptions.HTTPError as e:
       print(f"Erro HTTP: {e}")
       print(f"Resposta: {response.text}")
   ```

### Verificações de Segurança

- ✅ Client Secret está protegido e não exposto no frontend
- ✅ Tokens são gerados no backend
- ✅ Permissões mínimas necessárias foram concedidas
- ✅ HTTPS em produção

## 📝 Considerações de Produção

1. **Capacidade Premium**: Para melhor performance e recursos avançados
2. **Cache de Tokens**: Implemente cache para evitar gerações desnecessárias
3. **Monitoramento**: Configure logs e métricas de uso
4. **Backup**: Mantenha backup das configurações e IDs

## 📚 Recursos Adicionais

- [Documentação oficial Power BI Embedded](https://docs.microsoft.com/pt-br/power-bi/developer/embedded/)
- [Power BI REST APIs](https://docs.microsoft.com/pt-br/rest/api/power-bi/)
- [Playground Power BI Embedded](https://microsoft.github.io/PowerBI-JavaScript/demo/)

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação oficial da Microsoft
2. Verifique os logs de erro no console do navegador
3. Confirme as configurações no Azure Portal