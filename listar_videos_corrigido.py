import yt_dlp

def listar_todos_videos(url_canal):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Precisa ser False para pegar detalhes
        'ignoreerrors': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Extraindo lista completa de vídeos...")
            info = ydl.extract_info(url_canal, download=False)
            
            canal = info.get('uploader', info.get('channel', 'Canal'))
            total_videos = len(info.get('entries', []))
            
            print(f"📺 Canal: {canal}")
            print(f"📊 Total de vídeos: {total_videos}")
            print("=" * 80)
            
            # Filtra apenas vídeos com a frase específica
            frase_filtro = "SUPER MUNDO GV SUPERBET - EPISÓDIO"
            episodios_encontrados = []
            
            print(f"🔍 Filtro: '{frase_filtro}'")
            print("⏳ Extraindo informações detalhadas...")
            print("=" * 80)
            
            for video in info.get('entries', []):
                titulo = video.get('title', 'Sem título')
                if frase_filtro in titulo:
                    # Extrai número do episódio usando regex
                    import re
                    match = re.search(r'#(\d+)', titulo)
                    numero_episodio = match.group(1) if match else "N/A"
                    
                    # Pega informações de data e duração
                    data_upload = video.get('upload_date', 'N/A')
                    if data_upload != 'N/A' and len(data_upload) == 8:
                        # Converte YYYYMMDD para DD/MM/YYYY
                        data_formatada = f"{data_upload[6:8]}/{data_upload[4:6]}/{data_upload[0:4]}"
                    else:
                        data_formatada = "N/A"
                    
                    duracao = video.get('duration', 0)
                    if duracao:
                        h, m, s = duracao//3600, (duracao%3600)//60, duracao%60
                        duracao_str = f"{h:02d}:{m:02d}:{s:02d}"
                    else:
                        duracao_str = "N/A"
                    
                    episodios_encontrados.append({
                        'titulo': titulo,
                        'episodio': numero_episodio,
                        'data': data_formatada,
                        'duracao': duracao_str
                    })
            
            print(f"📊 Episódios encontrados: {len(episodios_encontrados)}")
            print("=" * 80)
            
            # Lista episódios com informações detalhadas
            for i, ep in enumerate(episodios_encontrados, 1):
                print(f"{i:3d}. EPISÓDIO #{ep['episodio']}")
                print(f"     📅 Data: {ep['data']}")
                print(f"     ⏱️ Duração: {ep['duracao']}")
                print(f"     📝 {ep['titulo']}")
                print("-" * 60)
            
            print(f"✅ Total de episódios: {len(episodios_encontrados)}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL do canal está correta")

if __name__ == "__main__":
    # Canal padrão sempre @mundogv
    url = "https://www.youtube.com/@mundogv/streams"
    print(f"📺 Listando vídeos do canal: {url}")
    listar_todos_videos(url)