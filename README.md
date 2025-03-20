# Shopify Metaobject Creator

Script Python para criar e gerenciar metaobjetos do tipo "anos" no Shopify.

## Funcionalidades

- Cria metaobjetos para anos de 1999 a 2025 (intervalo personalizável)
- Verifica metaobjetos existentes para evitar duplicação
- Atualiza metaobjetos existentes se necessário
- Gerencia status de publicação dos metaobjetos

## Requisitos

- Python 3.6+
- Biblioteca `requests` 
- Biblioteca `python-dotenv`
- Acesso à API Admin do Shopify

## Configuração

1. Clone o repositório:
   ```
   git clone https://github.com/luccasfzn/shopify-metaobject-creator.git
   cd shopify-metaobject-creator
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` baseado no `.env.example` e configure suas credenciais:
   ```
   cp .env.example .env
   ```

4. Edite o arquivo `.env` com suas informações da API Shopify:
   ```
   SHOPIFY_SHOP_NAME=seu-shop-name
   SHOPIFY_ACCESS_TOKEN=seu-access-token
   ```

## Uso

Execute o script com:

```
python shopify-years-metaobject-creator.py
```

O script criará metaobjetos para os anos de 1999 a 2025 por padrão. Você pode modificar esse intervalo editando a chamada da função `process_all_years()` no final do script.