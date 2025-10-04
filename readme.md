# Python - API Genius

Este projeto é uma API REST em Python usando Flask que consome a API do Genius.
Passado o nome de um artista, a API retorna as 10 músicas mais populares do artista pesquisado.

## Pré-requisitos

* Python 3.10+
* Token de acesso da API Genius (crie em [https://genius.com/developers](https://genius.com/developers))

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/artist-genius-api.git
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

4. Configure a variável de ambiente com seu token Genius:

```bash
copy .env.example .env
```
Abra o .env e substitua SEU_TOKEN_AQUI pelo seu token real do Genius:

## Rodando a API

```bash
python app.py
```

A API estará disponível em: `http://127.0.0.1:5000`

## Endpoints

### GET /musicas

Retorna as 10 músicas mais populares do artista.

**Parametros:**

* `artista` (obrigatório): nome do artista (usar "-" quando houver espaço no nome)

**Exemplo:**

```
http://127.0.0.1:5000/musicas?artista=Charlie-brown-jr
```

**Resposta esperada:**

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