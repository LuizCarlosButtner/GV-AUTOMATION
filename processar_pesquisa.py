import re
import json
from datetime import datetime, timezone, timedelta
from consultar_youtube import consultar_youtube

def formatar_data_hora(data_iso, fuso_horario_local=timezone(timedelta(hours=-3))):
    """
    Converte uma data em formato ISO 8601 (ex: '2025-10-20T18:00:00Z')
    para o formato DD/MM/AAAA HH:MM, ajustando para o fuso horário de Brasília (UTC-3).
    """
    if not data_iso:
        return "N/A"
    try:
        # Converte de string para datetime ciente do fuso UTC
        data_utc = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
        # Converte para o fuso horário local
        data_local = data_utc.astimezone(fuso_horario_local)
        return data_local.strftime('%d/%m/%Y %H:%M')
    except (ValueError, TypeError):
        return "Data inválida"

def parse_iso8601_duration(duration_str):
    """Converte a duração ISO 8601 do YouTube (ex: PT1H23M45S) para um timedelta."""
    if not duration_str or not duration_str.startswith('PT'):
        return timedelta()

    hours = re.search(r'(\d+)H', duration_str)
    minutes = re.search(r'(\d+)M', duration_str)
    seconds = re.search(r'(\d+)S', duration_str)

    return timedelta(
        hours=int(hours.group(1)) if hours else 0,
        minutes=int(minutes.group(1)) if minutes else 0,
        seconds=int(seconds.group(1)) if seconds else 0
    )

def obter_detalhes_videos(video_ids):
    """
    Busca detalhes completos (incluindo de live) para uma lista de IDs de vídeo.
    """
    from consultar_youtube import API_KEY
    if not video_ids:
        return {}
    import requests

    url_videos_api = 'https://www.googleapis.com/youtube/v3/videos'
    detalhes_videos = {}
    # A API permite buscar até 50 IDs de uma vez em 'id' separado por vírgulas
    for i in range(0, len(video_ids), 50):
        chunk_ids = video_ids[i:i+50]
        
        params = {
            'part': 'snippet,liveStreamingDetails,contentDetails',
            'id': ','.join(chunk_ids),
            'key': API_KEY
        }
        try:
            response = requests.get(url_videos_api, params=params)
            response.raise_for_status()
            dados = response.json()
            
            for item in dados.get('items', []):
                video_id = item.get('id')
                if video_id:
                    detalhes_videos[video_id] = item
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar detalhes dos vídeos: {e}")
            continue
            
    return detalhes_videos

def obter_data_referencia(detalhe_video):
    """
    Retorna a data mais precisa: 'actualStartTime' para lives, ou 'publishedAt' como fallback.
    """
    live_details = detalhe_video.get('liveStreamingDetails', {})
    if live_details and 'actualStartTime' in live_details:
        return live_details['actualStartTime']
    
    snippet = detalhe_video.get('snippet', {})
    return snippet.get('publishedAt')

def extrair_numero_episodio(titulo):
    """Extrai o número do episódio de um título usando regex (procura por #NUMERO)."""
    if not titulo:
        return "N/A"
    match = re.search(r'#(\d+)', titulo)
    return match.group(1) if match else "N/A"

def extrair_nome_convidado(titulo):
    """Extrai o nome do convidado do título, que é o que vem após o padrão e o número do episódio."""
    if not titulo:
        return "N/A"
    # Procura por "SUPER MUNDO GV SUPERBET #<numero> " e captura o resto.
    match = re.search(r'SUPER MUNDO GV SUPERBET #\d+\s*(.*)', titulo, re.IGNORECASE)
    # Retorna o nome do convidado se encontrado, senão retorna o título original.
    return match.group(1).strip() if match and match.group(1) else titulo

def filtrar_videos_com_regex(dados_api, padrao_regex, ano=None, mes=None):
    """
    Primeiro, filtra por mês/ano no fuso de Brasília, depois busca detalhes e aplica o regex.

    Args:
        dados_api (dict): O dicionário JSON retornado pela API.
        padrao_regex (str): O padrão de regex para procurar no título.

    Returns:
        list: Uma lista de dicionários, cada um contendo título, ID e data do vídeo.
    """
    if not dados_api or 'items' not in dados_api:
        print("Dados da API inválidos ou vazios.")
        return []

    # Etapa 1: Pré-filtrar IDs por data no fuso de Brasília
    ids_no_mes = []
    print("\nPré-filtrando vídeos por data no fuso de Brasília...")
    for item in dados_api.get('items', []):
        video_id = item.get('id', {}).get('videoId')
        data_publicacao_utc = item.get('snippet', {}).get('publishedAt')

        if not video_id or not data_publicacao_utc:
            continue

        try:
            data_utc = datetime.fromisoformat(data_publicacao_utc.replace('Z', '+00:00'))
            data_brasilia = data_utc.astimezone(timezone(timedelta(hours=-3)))
            
            if (ano and data_brasilia.year == ano) and (mes and data_brasilia.month == mes):
                ids_no_mes.append(video_id)
        except (ValueError, TypeError):
            continue
    
    print(f"Encontrados {len(ids_no_mes)} vídeos dentro do mês {mes}/{ano} (horário de Brasília).")
    if not ids_no_mes:
        return []

    # Etapa 2: Buscar detalhes minuciosos para os IDs pré-filtrados
    print(f"Buscando detalhes minuciosos para {len(ids_no_mes)} vídeo(s)...")
    detalhes_completos = obter_detalhes_videos(ids_no_mes)

    # Etapa 3: Aplicar o filtro final de regex no título
    videos_filtrados = []
    padrao = re.compile(padrao_regex, re.IGNORECASE) # re.IGNORECASE para ignorar maiúsculas/minúsculas

    for video_id, detalhe in detalhes_completos.items():
        titulo = detalhe.get('snippet', {}).get('title')

        if titulo and padrao.search(titulo):
            videos_filtrados.append({
                'titulo': titulo,
                'videoId': video_id,
                'detalhe': detalhe # Adicionamos o dicionário de detalhes completo
            })

    return videos_filtrados

def carregar_config():
    """Carrega as configurações do arquivo config.json."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"Configuração carregada: Ano {config['ano_alvo']}, Mês {config['mes_alvo']}, Valor/h R$ {config['valor_por_hora']:.2f}")
            return config
    except FileNotFoundError:
        print("Erro: Arquivo de configuração 'config.json' não encontrado.")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao ler o arquivo de configuração 'config.json': {e}")
        return None

if __name__ == "__main__":
    config = carregar_config()
    if not config:
        exit() # Encerra o script se a configuração falhar

    # --- PARÂMETROS DA BUSCA ---
    ID_DO_CANAL = "UCbyaO5D4CLDIxQ-7tSS_2DA"  # Canal Mundo GV
    ORDEM = "date" # Ordenar por data
    MAX_RESULTADOS = 50 # Máximo por página de busca

    # 1. Busca os dados da API
    dados_brutos = consultar_youtube(ID_DO_CANAL, ORDEM, MAX_RESULTADOS,
                                     published_after=f"{config['ano_alvo']}-{config['mes_alvo']:02d}-01T00:00:00", 
                                     published_before=f"{config['ano_alvo']}-{config['mes_alvo']+1:02d}-01T23:59:59")

    # 2. Filtra os resultados com a nova lógica robusta
    if dados_brutos:
        PADRAO_TITULO = r"SUPER MUNDO GV SUPERBET #"
        videos_encontrados = filtrar_videos_com_regex(dados_brutos, PADRAO_TITULO, ano=config['ano_alvo'], mes=config['mes_alvo'])

        custo_total = 0.0
        duracao_total_timedelta = timedelta()
        total_episodios = len(videos_encontrados)

        print(f"\n--- Vídeos encontrados com o padrão '{PADRAO_TITULO}' ---")
        for i, video in enumerate(videos_encontrados, 1):
            detalhe = video['detalhe']
            titulo = detalhe.get('snippet', {}).get('title', 'Sem Título')
            video_id = detalhe.get('id')
            
            # Extração de dados
            numero_ep = extrair_numero_episodio(titulo)
            nome_convidado = extrair_nome_convidado(titulo)
            horario_inicio_utc = obter_data_referencia(detalhe)
            horario_inicio_br = datetime.fromisoformat(horario_inicio_utc.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=-3)))
            
            duration_iso = detalhe.get('contentDetails', {}).get('duration')
            duracao_timedelta = parse_iso8601_duration(duration_iso)
            duracao_minutos = duracao_timedelta.total_seconds() / 60
            
            horario_fim_br = horario_inicio_br + duracao_timedelta
            
            # Cálculo de custo
            valor_por_minuto = config['valor_por_hora'] / 60
            custo_episodio = duracao_minutos * valor_por_minuto
            
            custo_total += custo_episodio
            duracao_total_timedelta += duracao_timedelta
            
            # Impressão do relatório
            print("-" * 70)
            print(f"Episódio #{numero_ep} - {nome_convidado}")
            print(f"  - Início (BRT): {horario_inicio_br.strftime('%d/%m/%Y %H:%M')}")
            print(f"  - Fim (BRT):    {horario_fim_br.strftime('%d/%m/%Y %H:%M')}")
            print(f"  - Duração:      {duracao_minutos:.2f} minutos")
            print(f"  - Custo Est.:   R$ {custo_episodio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            print(f"  - Link:         https://www.youtube.com/watch?v={video_id}")

        # --- IMPRESSÃO DO RESUMO FINAL ---
        print("\n" + "=" * 70)
        print("--- RESUMO GERAL ---")
        total_segundos = duracao_total_timedelta.total_seconds()
        total_horas = int(total_segundos // 3600)
        total_minutos = int((total_segundos % 3600) // 60)

        print(f"Total de Episódios: {total_episodios}")
        print(f"Tempo Total Gravado: {duracao_total_timedelta.total_seconds() / 60:.2f} minutos ({total_horas:02d}h{total_minutos:02d}m)")
        print(f"Valor Total Estimado: R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print("=" * 70)