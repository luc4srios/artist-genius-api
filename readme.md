# Python - API Genius

Este projeto é uma API REST em Python usando Flask que consome a API do Genius para listar as 10 músicas mais populares de um artista. Foi utilizado Redis (via Docker) para armazenar em cache e DynamoDB/AWS para armazenar as transações de busca

## Pré-requisitos

* Python 3.10+
* Docker Desktop (Necessário para rodar o serviço Redis)
* Token de acesso API Genius
* Credenciais AWS

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

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do modelo disponivel e insira suas credenciais. (Necessário para conexão com Genius e AWS (DynamoDB))

```bash
copy .env.example .env
```
Abra o arquivo .env criado e adicione suas credenciais nos lugares de SEU_TOKEN_GENIUS, SUA_CHAVE_AWS e SUA_CHAVE_SECRETA

### 5. Inicialização do Redis (Docker)

Certifique-se de que o Docker Desktop está em execução e inicie o contêiner Redis:

```bash
docker run --name genius-redis -p 6379:6379 -d redis
```

### 6. Iniciar a API Flask

No terminal **COM O `(venv)` ATIVADO**, inicie o aplicativo Flask:

```bash
python app.py
```

A API estará disponível em: `http://127.0.0.1:5000`

## Testes e exemplos de Uso

**Parametros:**

* `artista` (obrigatório): nome do artista (usar "-" quando houver espaço no nome)
* `cache` (opcional, padrão `true`): Use `&cache=false` para forçar a limpeza do cache e a busca no Genius.

#### 1. Primeira chamada: força consulta ao Genius
* Esta é a primeira chamada para o artista. O cache e o DynamoDB serão atualizados.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada (Lenta):**

```json
{
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius",
  "transaction_id": "79cc8738-3fcd-49c6-80f1-aa57c206f538"
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
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "cache",
  "transaction_id": "6d88d579-1e35-427a-ada5-abd521de066b"
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
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius",
  "transaction_id": "c662f524-6e60-4b3a-9ead-fc249968ccf9"
}
```