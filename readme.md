# Python - API Genius

Este projeto é uma API REST em Python usando Flask que consome a API do Genius para listar as 10 músicas mais populares de um artista. Foi utilizado Redis (via Docker) para armazenar em cache e DynamoDB/AWS para armazenar as transações de busca

## Pré-requisitos

* Python 3.10+
* Docker Desktop (Necessário para rodar o serviço Redis)
* Token de acesso API Genius
* Conta AWS (com credenciais e permissões para DynamoDB)

## Configuração

### 1. Clone o repositório:

```bash
git clone https://github.com/luc4srios/artist-genius-api.git
cd artist-genius-api
```

### 2. Crie e ative um ambiente virtual (venv):

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```
### 4. Obtendo o Token de Acesso da API Genius

Para que a aplicação consiga se comunicar com a API do Genius, é necessário gerar um **token de acesso**.

1. **Acesse o site do Genius Developers:**  
 [https://genius.com/developers](https://genius.com/developers)
2. **Faça login ou crie uma conta** no Genius.

3. **Crie uma nova aplicação** clicando em **"Create an API Client"**.

4. **Preencha os campos solicitados**, como nome da aplicação e URL (ex: `http://localhost`).

5. Após criar a aplicação, anote o **Client Access Token** para usar no passo 6.


### 5. Configuração da AWS (IAM e DynamoDB)

A aplicação utiliza o **Amazon DynamoDB** para armazenar as transações de busca.  
Antes de iniciar o Flask, é necessário configurar um **usuário IAM** com acesso programático e criar a tabela no DynamoDB com o esquema esperado pelo serviço.

1. **Acesse o site da AWS:**  
 [https://console.aws.amazon.com/console/home](https://console.aws.amazon.com/console/home)


2. **Faça login ou crie uma conta**

#### 5.1 Configuração de Credenciais e Permissões (IAM)

1. No console da AWS, procure por **IAM (Identity and Access Management)**.

2. Vá em **Usuários: Adicionar usuário** e defina um nome claro, por exemplo:  `artist-genius-api`

3. Selecione **Acesso programático** (isso irá gerar a *Access Key* e *Secret Key*).

4. Escolha **Anexar políticas existentes diretamente** e selecione a política gerenciada: `AmazonDynamoDBFullAccess`  

5. Após criar o usuário, anote a **Access Key ID** e a **Secret Access Key** para usar no passo 6.  

#### 5.2 Criação da Tabela no DynamoDB

O serviço **dynamo_service.py** espera uma tabela específica para registrar as transações.
1. **Acesse o DynamoDB**  
   No console AWS, procure por **DynamoDB - Criar tabela**.

2. **Configure a tabela:**  
    - Nome da tabela: **artist_genius_traces**
    - Chave primária (Partition Key): **transaction_id**
    - Tipo: **String**

3. **Crie a tabela**  
   Clique em Criar/Create e aguarde até que o status esteja como **Active**.

#### 5.3 Escolha da Região AWS

Ao criar os recursos acima, verifique em qual **região da AWS** você está utilizando.
1. No canto superior direito do console da AWS, clique na região exibida

2. Copie o código da região correspondente para usar no passo 6. (ex: `sa-east-1`)


### 6. Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do modelo disponível, insira suas credenciais e a região que será utilizada (Necessário para conexão com Genius e AWS (DynamoDB))

```bash
copy .env.example .env
```
Abra o arquivo `.env` gerado após o comando acima e adicione suas credenciais e região escolhida na AWS: 
```bash
GENIUS_API_TOKEN=SEU_TOKEN_GENIUS
AWS_ACCESS_KEY_ID=SUA_CHAVE_AWS
AWS_SECRET_ACCESS_KEY=SUA_CHAVE_SECRETA
AWS_REGION=REGIAO_CONFIGURADA_AWS
```

### 7. Inicialização do Redis (Docker)

Certifique-se de que o Docker Desktop está em execução e inicie o contêiner Redis:

```bash
docker run --name genius-redis -p 6379:6379 -d redis
```

### 8. Iniciar a API Flask

No terminal com **`(venv)`** ativado, inicie o aplicativo Flask:

```bash
python app.py
```

A API estará disponível em: `http://127.0.0.1:5000`

## Testes e exemplos de Uso

**Parâmetros:**

* `artista` (obrigatório): nome do artista (usar "-" quando houver espaço no nome)
* `cache` (opcional, padrão `true`): Use `&cache=false` para forçar a limpeza do cache e realizar a busca no Genius.

#### 1. Primeira chamada: força consulta ao Genius
* Esta é a primeira chamada para o artista. O cache e o DynamoDB serão atualizados.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada (Lenta):**

```json
{
  "transaction_id": "79cc8738-3fcd-49c6-80f1-aa57c206f538",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius"
}
```

#### 2. Segunda chamada: resposta imediata
* Ao chamar a mesma URL novamente, a resposta deve ser quase instantânea e vir do Redis.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada (Instantânea):**

```json
{
  "transaction_id": "6d88d579-1e35-427a-ada5-abd521de066b",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "cache"
}
```

#### 3. Terceira chamada: limpar cache e consumir API Genius
* O parâmetro cache=false força a limpeza do Redis e realiza uma nova busca no Genius.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr&cache=false
```

**Resposta esperada (Lenta):**

```json
{
  "transaction_id": "c662f524-6e60-4b3a-9ead-fc249968ccf9",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius"
}
```

## Documentação da API

A API possui documentação interativa no Swagger, que permite testar os endpoints diretamente do navegador.

Acesse em: [http://127.0.0.1:5000/docs/](http://127.0.0.1:5000/docs/)