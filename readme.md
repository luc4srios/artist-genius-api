# Python - API Genius

Este projeto é uma API REST em Python usando Flask que consome a API do Genius para listar as 10 músicas mais populares de um artista. Foi utilizado Redis (via Docker) para armazenar em cache e DynamoDB/AWS para armazenar as transações de busca

## Pré-requisitos

* Python 3.10+
* Docker Desktop (Necessário para rodar o serviço Redis)
* Token de acesso API Genius
* Credenciais AWS

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/luc4srios/artist-genius-api.git
cd artist-genius-api
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do modelo disponivel e insira suas credenciais. (Necessário para conexão com Genius e AWS (DynamoDB))

```bash
copy .env.example .env
```
Abra o arquivo .env criado e adicione suas credenciais nos lugares de SEU_TOKEN_GENIUS, SUA_CHAVE_AWS e SUA_CHAVE_SECRETA

4. Inicialização do Redis (Docker)

Certifique-se de que o Docker Desktop está em execução e inicie o contêiner Redis:

```bash
docker run --name genius-redis -p 6379:6379 -d redis
```

## No terminal com o "venv" ativado, inicie o aplicativo Flask:

```bash
python app.py
```

A API estará disponível em: `http://127.0.0.1:5000`

## Testes e Exemplos de Uso

**Parametros:**

* `artista` (obrigatório): nome do artista (usar "-" quando houver espaço no nome)

### 1. Cache Miss (Primeira Chamada / Força Consulta ao Genius)
* Esta é a primeira chamada para o artista. O cache e o DynamoDB serão atualizados.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada (Lenta):**

```json
{
  "transaction_id": "uuid-gerado",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius"
}
```

### 2. Cache Hit (Segunda Chamada Imediata)
* Ao chamar a mesma URL novamente, a resposta deve ser quase instantânea e vir do Redis.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada (Instantânea):**

```json
{
  "transaction_id": "uuid-gerado",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "cache"
}
```

### 3. Force Update (Limpar Cache e Consultar Genius)
* O parâmetro cache=false força a limpeza do Redis e realiza uma nova busca no Genius, **gerando um NOVO `transaction_id`**.

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr&cache=false
```

**Resposta esperada (Lenta):**

```json
{
  "transaction_id": "uuid-gerado",
  "data": [
    {"title": "Como Tudo Deve Ser", "url": "..."},
    {"title": "Lugar ao Sol", "url": "..."}
  ],
  "fonte": "genius"
}
```