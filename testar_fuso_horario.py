import requests
import json
import os
from datetime import datetime, timezone, timedelta

def converter_para_brasilia(data_utc_str):
    """Converte uma string de data UTC para um objeto datetime de Brasília."""
    if not data_utc_str:
        return None
    try:
        fuso_brasilia = timezone(timedelta(hours=-3))
        data_utc = datetime.fromisoformat(data_utc_str.replace('Z', '+00:00'))
        return data_utc.astimezone(fuso_brasilia)
    except (ValueError, TypeError):
        return None


def testar_fuso_video_por_id(video_id):
    """
    Busca os detalhes de um único vídeo e testa a conversão de fuso horário.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Erro: A variável de ambiente YOUTUBE_API_KEY não foi definida.")
        print("Execute 'export YOUTUBE_API_KEY=\"SUA_CHAVE_AQUI\"' no seu terminal.")
        return

    # Usamos o endpoint 'videos' que é mais direto para buscar por ID.
    url_api = 'https://www.googleapis.com/youtube/v3/videos'
    
    params = {
        'part': 'snippet,liveStreamingDetails', # Adicionamos liveStreamingDetails
        'id': video_id,
        'key': api_key
    }

    print(f"--- Testando Fuso Horário para o Vídeo ID: {video_id} ---")

    try:
        response = requests.get(url_api, params=params)
        response.raise_for_status()
        dados = response.json()

        if not dados.get('items'):
            print("Erro: Vídeo não encontrado com o ID fornecido.")
            return

        snippet = dados['items'][0]['snippet']
        live_details = dados['items'][0].get('liveStreamingDetails', {})

        titulo = snippet.get('title')
        data_publicacao_utc_str = snippet.get('publishedAt')
        inicio_real_utc_str = live_details.get('actualStartTime')

        print(f"\n🎬 Título: {titulo}")
        print("-" * 50)

        # 1. Analisando 'publishedAt'
        print("1. Data de Publicação (publishedAt):")
        print(f"   - Bruto (UTC): {data_publicacao_utc_str}")
        data_publicacao_br = converter_para_brasilia(data_publicacao_utc_str)
        if data_publicacao_br:
            print(f"   - Convertido (Brasília): {data_publicacao_br.strftime('%d/%m/%Y %H:%M:%S')}")

        # 2. Analisando 'actualStartTime'
        print("\n2. Início Real da Live (actualStartTime):")
        if inicio_real_utc_str:
            print(f"   - Bruto (UTC): {inicio_real_utc_str}")
            inicio_real_br = converter_para_brasilia(inicio_real_utc_str)
            if inicio_real_br:
                print(f"   - Convertido (Brasília): {inicio_real_br.strftime('%d/%m/%Y %H:%M:%S')} <--- ESTE É PROVAVELMENTE O CORRETO")
        else:
            print("   - (Não era uma live ou dados indisponíveis)")

        print("\n" + "="*60 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")


if __name__ == "__main__":
    # --- LISTA DE VÍDEOS PARA TESTAR ---
    # Adicione aqui outros IDs de vídeo para comparar e encontrar o padrão.
    videos_para_testar = [
        "3FFRE_5e9AA"
        
        #"2Ti1_-SlVIE",
        #"7yzgWpzmjTc",
        #"ExFJx7YGuIk" 
        # O EP #128 que estávamos analisando
        # "ID_DE_OUTRO_VIDEO_AQUI",
        # "ID_DE_MAIS_UM_VIDEO_AQUI",
    ]

    for video_id in videos_para_testar:
        testar_fuso_video_por_id(video_id)