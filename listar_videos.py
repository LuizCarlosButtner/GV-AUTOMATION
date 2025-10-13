import yt_dlp

def listar_todos_videos(url_canal):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
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
            
            # Lista todos os vídeos
            for i, video in enumerate(info.get('entries', []), 1):
                titulo = video.get('title', 'Sem título')
                print(f"{i:3d}. {titulo}")
            
            print("=" * 80)
            print(f"✅ Listagem completa: {total_videos} vídeos")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL do canal está correta")

if __name__ == "__main__":
    # Canal padrão sempre @mundogv
    url = "https://www.youtube.com/@mundogv/streams"
    print(f"📺 Listando vídeos do canal: {url}")
    listar_todos_videos(url)

    