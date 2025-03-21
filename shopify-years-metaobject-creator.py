import requests
import json
import time
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Shopify store configuration
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")  # Seu nome de loja Shopify
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")  # Seu token de acesso à API Admin do Shopify

# GraphQL endpoint
API_URL = f"https://{SHOP_NAME}.myshopify.com/admin/api/2023-10/graphql.json"

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

def get_all_metaobjects():
    """
    Get all metaobjects of type 'years'
    """
    # GraphQL query to get all metaobjects of type 'years'
    query = """
    query {
      metaobjects(first: 100, type: "years") {
        edges {
          node {
            id
            handle
            fields {
              key
              value
            }
          }
        }
      }
    }
    """
    
    # Make the API request
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": query}
    )
    
    data = response.json()
    
    if "data" in data and "metaobjects" in data["data"]:
        return data["data"]["metaobjects"]["edges"]
    
    return []

def find_year_metaobject(year, all_metaobjects):
    """
    Check if a metaobject for the given year already exists
    """
    year_str = str(year)
    
    for edge in all_metaobjects:
        node = edge["node"]
        for field in node["fields"]:
            if field["key"] == "name" and field["value"] == year_str:
                return node
    
    return None

def update_year_metaobject(metaobject_id, year):
    """
    Update an existing year metaobject
    """
    # GraphQL mutation to update a metaobject
    mutation = """
    mutation metaobjectUpdate($id: ID!, $metaobject: MetaobjectUpdateInput!) {
      metaobjectUpdate(id: $id, metaobject: $metaobject) {
        metaobject {
          id
          handle
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    # Variables for the mutation
    variables = {
        "id": metaobject_id,
        "metaobject": {
            "fields": [
                {
                    "key": "name",
                    "value": str(year)
                }
            ],
            "capabilities": {
                "publishable": {
                    "status": "ACTIVE"
                }
            }
        }
    }
    
    # Make the API request
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": mutation, "variables": variables}
    )
    
    # Return the response data
    return response.json()

def create_year_metaobject(year):
    """
    Create a single year metaobject entry
    """
    # GraphQL mutation to create a metaobject
    mutation = """
    mutation metaobjectCreate($metaobject: MetaobjectCreateInput!) {
      metaobjectCreate(metaobject: $metaobject) {
        metaobject {
          id
          handle
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    # Variables for the mutation
    variables = {
        "metaobject": {
            "type": "years",  # The metaobject definition type
            "fields": [
                {
                    "key": "name",
                    "value": str(year)
                }
            ],
            "capabilities": {
                "publishable": {
                    "status": "ACTIVE"
                }
            }
        }
    }
    
    # Make the API request
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": mutation, "variables": variables}
    )
    
    # Return the response data
    return response.json()

def process_year(year, all_metaobjects):
    """
    Process a single year - check if it exists, update if it does, create if it doesn't
    """
    print(f"Processing year {year}...")
    
    # First, check if the metaobject already exists
    existing_metaobject = find_year_metaobject(year, all_metaobjects)
    
    if existing_metaobject:
        print(f"Metaobject for year {year} already exists with ID {existing_metaobject['id']}. Updating...")
        result = update_year_metaobject(existing_metaobject['id'], year)
        action = "updated"
    else:
        print(f"Metaobject for year {year} does not exist. Creating new...")
        result = create_year_metaobject(year)
        action = "created"
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Check for errors
    if "errors" in result or (
        "data" in result and 
        (("metaobjectUpdate" in result["data"] and result["data"]["metaobjectUpdate"]["userErrors"]) or
         ("metaobjectCreate" in result["data"] and result["data"]["metaobjectCreate"]["userErrors"]))
    ):
        print(f"Error {action} metaobject for year {year}: {json.dumps(result, indent=2)}")
        return {"success": False, "result": result, "action": action}
    else:
        print(f"Successfully {action} metaobject for year {year}")
        return {"success": True, "result": result, "action": action}

def get_metaobject_definition_by_type(type_name):
    """
    Verifica se existe uma definição de metaobjeto com o tipo especificado
    """
    # GraphQL query para buscar definições de metaobjetos
    query = """
    query {
      metaobjectDefinitions(first: 100) {
        edges {
          node {
            id
            name
            type
            fieldDefinitions {
              name
              key
              type {
                name
              }
            }
          }
        }
      }
    }
    """
    
    # Faz a requisição API
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": query}
    )
    
    data = response.json()
    
    if "data" in data and "metaobjectDefinitions" in data["data"]:
        definitions = data["data"]["metaobjectDefinitions"]["edges"]
        for definition in definitions:
            if definition["node"]["type"] == type_name:
                return definition["node"]
    
    return None

def create_metaobject_definition():
    """
    Cria uma definição de metaobjeto para 'years' se não existir
    """
    print("Verificando se a definição de metaobjeto 'years' já existe...")
    
    # Verifica se a definição já existe
    definition = get_metaobject_definition_by_type("years")
    if definition:
        print(f"Definição de metaobjeto 'years' já existe com ID: {definition['id']}")
        return True
    
    print("Definição de metaobjeto 'years' não encontrada. Criando nova definição...")
    
    # GraphQL mutation para criar definição de metaobjeto
    mutation = """
    mutation metaobjectDefinitionCreate($definition: MetaobjectDefinitionCreateInput!) {
      metaobjectDefinitionCreate(definition: $definition) {
        metaobjectDefinition {
          id
          name
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    # Variáveis para a mutation
    variables = {
        "definition": {
            "name": "Years",
            "type": "years",
            "fieldDefinitions": [
                {
                    "name": "Name",
                    "key": "name",
                    "type": "single_line_text_field",
                    "validations": {
                        "required": True
                    }
                }
            ],
            "capabilities": {
                "publishable": {
                    "enabled": True
                }
            }
        }
    }
    
    # Faz a requisição API
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": mutation, "variables": variables}
    )
    
    data = response.json()
    
    # Verifica se houve erros
    if "errors" in data or "userErrors" in data.get("data", {}).get("metaobjectDefinitionCreate", {}):
        error_msg = data.get("errors", []) or data.get("data", {}).get("metaobjectDefinitionCreate", {}).get("userErrors", [])
        print(f"Erro ao criar definição de metaobjeto: {json.dumps(error_msg, indent=2)}")
        return False
    
    print("Definição de metaobjeto 'years' criada com sucesso!")
    return True

def process_all_years(start_year=1999, end_year=2025):
    """
    Process metaobject entries for all years in the specified range
    """
    results = []
    
    # Primeiro, cria a definição do metaobjeto se não existir
    if not create_metaobject_definition():
        print("Não foi possível criar a definição do metaobjeto. Encerrando...")
        return []
    
    # Pequeno atraso para garantir que a definição esteja disponível
    time.sleep(2)
    
    # Get all existing metaobjects first
    print("Fetching all existing metaobjects...")
    all_metaobjects = get_all_metaobjects()
    print(f"Found {len(all_metaobjects)} existing metaobjects")
    
    for year in range(start_year, end_year + 1):
        result = process_year(year, all_metaobjects)
        results.append(result)
    
    return results

if __name__ == "__main__":
    print("Starting processing of year metaobjects...")
    
    # You can customize the year range if needed
    results = process_all_years(1999, 2025)
    
    print(f"Completed processing {len(results)} year metaobjects")
    
    # Count successful creations and updates
    successful = sum(1 for r in results if r["success"])
    created = sum(1 for r in results if r["success"] and r["action"] == "created")
    updated = sum(1 for r in results if r["success"] and r["action"] == "updated")
    
    print(f"Successfully processed {successful} year metaobjects ({created} created, {updated} updated)")