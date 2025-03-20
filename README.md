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
- Acesso à API Admin do Shopify

## Configuração

1. Configure suas credenciais no início do arquivo:
   ```python
   SHOP_NAME = "seu-shop-name"
   ACCESS_TOKEN = "seu-access-token"
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Execute o script com:

```
python shopify-years-metaobject-creator.py
```

## Nota de Segurança

⚠️ Este repositório contém um token de acesso à API do Shopify no código. Recomenda-se armazenar informações sensíveis em variáveis de ambiente ou arquivos de configuração seguros.