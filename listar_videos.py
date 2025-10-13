import yt_dlp

def obter_data_formatada(timestamp):
    """Converte timestamp em data formatada"""
    from datetime import datetime
    try:
        data = datetime.strptime(str(timestamp), "%Y%m%d")
        return data.strftime("%d/%m/%Y")
    except:
        return "Data indisponível"

def listar_todos_videos(url_canal):
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
            
            # Filtra os vídeos que queremos
            videos_filtrados = [
                video for video in playlist.get('entries', [])
                if video and 'MUNDO GV SUPERBET' in video.get('title', '')
            ]
            
            print(f"📺 Canal: {playlist.get('uploader', 'Canal desconhecido')}")
            print(f"🎯 Vídeos encontrados: {len(videos_filtrados)}")
            print("=" * 100)
            
            # Segundo passo: obter detalhes de cada vídeo
            ydl_opts_detailed = {
                'quiet': True,
                'extract_flat': False,
                'ignoreerrors': True,
                'skip_download': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_detailed) as ydl_detailed:
                for i, video in enumerate(videos_filtrados, 1):
                    try:
                        # Obtém informações detalhadas do vídeo
                        video_url = f"https://www.youtube.com/watch?v={video['id']}"
                        info = ydl_detailed.extract_info(video_url, download=False)
                        
                        # Extrai e formata as informações
                        titulo = info.get('title', 'Sem título')
                        data = obter_data_formatada(info.get('upload_date', ''))
                        duracao = info.get('duration_string', 'Duração desconhecida')
                        
                        print(f"{i:3d}. [{data}] {titulo} ({duracao})")
                    except Exception as e:
                        print(f"{i:3d}. [Erro ao obter detalhes] {video.get('title', 'Sem título')}")
            
            print("=" * 100)
            print(f"✅ Listagem completa: {len(videos_filtrados)} vídeos do podcast encontrados")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL do canal está correta")

if __name__ == "__main__":
    # Canal padrão sempre @mundogv
    url = "https://www.youtube.com/@mundogv/streams"
    print(f"📺 Listando vídeos do canal: {url}")
    listar_todos_videos(url)

