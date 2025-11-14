import requests
import json
import os
from datetime import datetime, timezone, timedelta

# --- CONFIGURAÇÃO ---
# É uma boa prática carregar chaves de API de variáveis de ambiente.
# Execute `export YOUTUBE_API_KEY='SUA_CHAVE_AQUI'` no seu terminal antes de rodar o script.
API_KEY = os.getenv('YOUTUBE_API_KEY')

# URL base da API de busca do YouTube.
URL_API = 'https://www.googleapis.com/youtube/v3/search'
# --------------------

def consultar_youtube(channel_id, order, max_results, event_type=None, published_after=None, published_before=None):
    """
    Realiza uma consulta na API de busca do YouTube.
    As datas published_after e published_before são interpretadas como horário de Brasília (UTC-3) 
    e convertidas para UTC para a API.
    """
    if not API_KEY:
        print("Erro: A variável de ambiente YOUTUBE_API_KEY não foi definida.")
        print("Execute 'export YOUTUBE_API_KEY=\"SUA_CHAVE_AQUI\"' no seu terminal.")
        return None

    # Parâmetros da requisição.
    params = {
        'part': 'snippet',
        'key': API_KEY,
        'channelId': channel_id,
        'order': order,
        'maxResults': max_results,
        'type': 'video'  # Garante que estamos buscando apenas vídeos.
    }

    # Adiciona o filtro de tipo de evento apenas se ele for especificado.
    if event_type:
        params['eventType'] = event_type

    # Converte as datas do horário de Brasília para UTC, se fornecidas.
    fuso_brasilia = timezone(timedelta(hours=-3))
    if published_after:
        try:
            dt_brasilia = datetime.fromisoformat(published_after).replace(tzinfo=fuso_brasilia)
            dt_utc = dt_brasilia.astimezone(timezone.utc)
            params['publishedAfter'] = dt_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            print(f"Formato de data inválido para published_after: {published_after}")
            return None
    if published_before:
        try:
            dt_brasilia = datetime.fromisoformat(published_before).replace(tzinfo=fuso_brasilia)
            dt_utc = dt_brasilia.astimezone(timezone.utc)
            params['publishedBefore'] = dt_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            print(f"Formato de data inválido para published_before: {published_before}")
            return None

    print(f"Buscando vídeos do canal (Mundo GV)")

    try:
        # Faz a requisição GET para a API do YouTube.
        response = requests.get(URL_API, params=params)
        response.raise_for_status()  # Lança um erro para respostas HTTP 4xx/5xx.

        # Converte a resposta para formato JSON.
        dados = response.json()

        return dados

    except requests.exceptions.HTTPError as http_err:
        print(f"\nErro HTTP ao fazer a requisição: {http_err}")
        print(f"Resposta do servidor: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\nOcorreu um erro de conexão: {e}")
        return None
    except json.JSONDecodeError:
        print("\nErro: Não foi possível decodificar a resposta JSON do servidor.")
        return None


if __name__ == "__main__":
    # --- PARÂMETROS DA BUSCA ---
    # Substitua pelos valores que desejar.
    ID_DO_CANAL = "UCbyaO5D4CLDIxQ-7tSS_2DA"  # Ex: Canal Mundo GV
    ORDEM = "date"  # Ordenar por data
    # TIPO_EVENTO = "completed"  # Se quiséssemos apenas lives, usaríamos esta linha.
    MAX_RESULTADOS = 50 # Máximo por página
    
    # --- DEFINIÇÃO DO PERÍODO ALVO ---
    ANO_ALVO = 2025
    MES_ALVO = 10  # Outubro
    
    # --- CÁLCULO AUTOMÁTICO DA BUSCA AMPLA ---
    # Para garantir a captura de todos os vídeos devido ao fuso horário,
    # a busca é feita de um dia antes do início do mês alvo até um dia depois do fim.
    primeiro_dia_mes_alvo = datetime(ANO_ALVO, MES_ALVO, 1)
    proximo_mes = primeiro_dia_mes_alvo.replace(day=28) + timedelta(days=4)  # Vai para o próximo mês
    ultimo_dia_mes_alvo = proximo_mes - timedelta(days=proximo_mes.day)
    DATA_INICIO_BUSCA_AMPLA = (primeiro_dia_mes_alvo - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')
    DATA_FIM_BUSCA_AMPLA = (ultimo_dia_mes_alvo + timedelta(days=1)).strftime('%Y-%m-%dT23:59:59')
    # -------------------------

    # Executa a consulta
    dados_api = consultar_youtube(ID_DO_CANAL, ORDEM, MAX_RESULTADOS,
                                  published_after=DATA_INICIO_BUSCA_AMPLA, published_before=DATA_FIM_BUSCA_AMPLA)

    # Se a consulta foi bem-sucedida, imprime os resultados
    if dados_api:
        print("\n--- RESPOSTA COMPLETA DA API (JSON) ---")
        print(json.dumps(dados_api, indent=4, ensure_ascii=False))

        print("\n--- TÍTULOS DOS VÍDEOS ENCONTRADOS ---")
        for item in dados_api.get('items', []):
            titulo = item.get('snippet', {}).get('title')
            video_id = item.get('id', {}).get('videoId')
            print(f"- {titulo} (ID: {video_id})")
