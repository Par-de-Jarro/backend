# FASTAPI TEMPLATE

# Colocando para rodar

## 1 - Clonar o repositório

### Windows
- Primeiramente vamos fazer uma configuração do github:
Essa configuração vai fazer que, quando você clonar repositorios, os delimatores de linha manterão o padrão do unix.

```git config --global core.autocrlf false```

- Depois vamos clonar o repositório

```git clone git@github.com:Projeto-ES-UFCG-2021-2/fastapi-template.git```

### Linux

- Vamos clonar o repositório

```git clone git@github.com:Projeto-ES-UFCG-2021-2/fastapi-template.git```

##  2 - Instale o Docker
https://docs.docker.com/engine/install/

## 3 - Instale o Docke Compose V2
https://docs.docker.com/compose/

## 4 - Crie seu .env com base no .env.example

```cp .env.example .env```

- Altere as variáveis que julgar necessárias.

## 5 - Rode o Docker Compose para subir o container da aplicação

```docker compose up```

## 6 - Caso deseja desligar a aplicação utilize o docker compose para para a aplicação

```docker compose down```


# Rodando os testes

## 1 - Alterar banco de dados
- Altera o campo  ```POSTGRES_DB``` no arquivo ```docker-compose``` para ```postgres_test```

- Alterar a variável ```SQLALCHEMY_DATABASE_URL``` no seu .env para utilizar o banco de dados ```postgres_test```

## 2 - Rodar os testes

```make test-docker```

