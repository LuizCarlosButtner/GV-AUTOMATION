import yt_dlp

def obter_data_formatada(timestamp):
    """Converte timestamp em data formatada"""
    from datetime import datetime
    try:
        data = datetime.strptime(str(timestamp), "%Y%m%d")
        return data.strftime("%d/%m/%Y")
    except:
        return "Data indisponível"

def formatar_moeda_br(valor):
    """Formata número float para moeda BR (ex: 1500 -> '1.500,00')."""
    try:
        # garante float
        v = float(valor)
    except Exception:
        return "0,00"
    # formata com separador de milhares em inglês e ponto decimal
    s = f"{v:,.2f}"
    # s exemplo: '1,500.00' -> queremos '1.500,00'
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s

def listar_todos_videos(url_canal, palavra_chave, mes=None, ano=None, valorPorMinuto=0, max_results=None):
    # Configuração inicial para listar vídeos
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'ignoreerrors': True,
        'skip_download': True,
        'no_warnings': True
    }
    
    try:
        # Primeiro passo: obter lista de vídeos
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Extraindo lista de vídeos do canal...")
            playlist = ydl.extract_info(url_canal, download=False)
            
            # Filtra os vídeos que querem pela palavra-chave
            entries = [e for e in playlist.get('entries', []) if e]
            videos_filtrados = [v for v in entries if palavra_chave.lower() in v.get('title', '').lower()]

            print(f"📺 Canal: {playlist.get('uploader', 'Canal desconhecido')}")
            print(f"🔎 Entradas com palavra-chave: {len(videos_filtrados)}")

            # Tenta filtrar cedo por upload_date disponível nas entradas planas
            videos_with_date = []
            videos_without_date = []
            for v in videos_filtrados:
                if v.get('upload_date'):
                    videos_with_date.append(v)
                else:
                    videos_without_date.append(v)

            videos_to_check = videos_filtrados
            # Se houver entradas planas com upload_date, aplicamos o filtro de mês/ano nelas
            early_matches = []
            if (mes or ano) and videos_with_date:
                for v in videos_with_date:
                    try:
                        ud = v.get('upload_date')
                        y = int(ud[0:4])
                        m = int(ud[4:6])
                    except Exception:
                        continue
                    if mes and m != mes:
                        continue
                    if ano and y != ano:
                        continue
                    early_matches.append(v)

                if early_matches:
                    # Só vamos detalhar as early_matches — evita extrair detalhes para os outros
                    videos_to_check = early_matches
                    if max_results:
                        videos_to_check = early_matches[:max_results]
                    print(f"⚡ Usando filtro antecipado por data: {len(videos_to_check)} entradas serão processadas (early matches)")
                else:
                    # nenhuma entrada plana bateu no filtro, mas ainda podemos ter matches apenas acessando detalhes
                    print("⚠️ Nenhuma data disponível nas entradas planas que atenda ao filtro; será necessário extrair detalhes para confirmar")
            else:
                print("" )
            print("=" * 100)
            
            # Segundo passo: obter detalhes de cada vídeo
            ydl_opts_detailed = {
                'quiet': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'skip_download': True
            }
            
####################################################################################################


            with yt_dlp.YoutubeDL(ydl_opts_detailed) as ydl_detailed:
                results_count = 0
                for i, video in enumerate(videos_to_check, 1):
                    try:
                        # Obtém informações detalhadas do vídeo
                        video_url = f"https://www.youtube.com/watch?v={video['id']}"
                        info = ydl_detailed.extract_info(video_url, download=False)

                        # Verifica filtro de mês/ano usando upload_date (YYYYMMDD)
                        upload_date = info.get('upload_date')
                        if mes or ano:
                            if not upload_date:
                                # sem data, não atende ao filtro
                                continue
                            try:
                                y = int(upload_date[0:4])
                                m = int(upload_date[4:6])
                            except:
                                continue
                            if mes and m != mes:
                                continue
                            if ano and y != ano:
                                continue

                        # Extrai e formata as informações
                        titulo = info.get('title', 'Sem título')
                        data = obter_data_formatada(upload_date if upload_date else '')
                        duracao = info.get('duration', 0)
                        duracao_min = duracao / 60 if isinstance(duracao, (int, float)) else 0
                        custo = duracao_min * valorPorMinuto if valorPorMinuto else 0

                        print(f"{i:3d}. ")
                        print(f"    🎬 Título: {titulo}")
                        print(f"    📅 Data: {data}")
                        print(f"    ⏱ Duração: {duracao_min:.2f} minutos")
                        print(f"    🔗 Link: {video_url}")
                        if valorPorMinuto:
                            print(f"    💰 Custo estimado: R$ {formatar_moeda_br(custo)}")

                        results_count += 1
                        # se max_results foi definido, interrompe quando atingir
                        if max_results and results_count >= max_results:
                            print(f"⛔ Atingido max_results={max_results}. Encerrando processamento.")
                            break

                    except Exception as e:
                        print(f"{i:3d}. [Erro ao obter detalhes] {video.get('title', 'Sem título')}")
            
            print("=" * 100)
            print(f"✅ Listagem completa: {len(videos_filtrados)} vídeos do podcast encontrados")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL do canal está correta")



####################################################################################################




if __name__ == "__main__":
    # Canal padrão sempre @mundogv

    mes = 10  # Exemplo: filtrar por outubro
    ano = 2025  # Exemplo: filtrar por 2023
    palavra_chave = "MUNDO GV SUPERBET"  # Exemplo: filtrar por palavra-chave no título
    valorPorHora = 750  # Exemplo: valor por hora
    valorPorMinuto = valorPorHora/60  # Divide o valor por minuto para obter o valor por hora
    url = "https://www.youtube.com/@mundogv/streams"
    print(f"📺 Listando vídeos do canal: {url}")
    # Passa os filtros: palavra_chave, mês, ano, valor por minuto e max_results
    listar_todos_videos(url, palavra_chave, mes, ano, valorPorMinuto, max_results=5)

