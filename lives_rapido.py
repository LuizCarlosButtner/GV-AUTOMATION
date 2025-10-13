import yt_dlp

def buscar_lives_rapido(url_canal):
    # Configuração mais simples e rápida
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 10,  # Apenas 10 vídeos para ser mais rápido
        'ignoreerrors': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Extraindo lista de vídeos...")
            playlist_info = ydl.extract_info(url_canal, download=False)
            
            canal = playlist_info.get('uploader', playlist_info.get('channel', 'Canal'))
            print(f"📺 {canal}")
            print("=" * 50)
            
            # Lista apenas os títulos dos vídeos mais recentes
            for i, video in enumerate(playlist_info.get('entries', [])[:10], 1):
                titulo = video.get('title', 'Sem título')
                print(f"{i}. {titulo}")
            
            print(f"\n✅ Listados os {len(playlist_info.get('entries', [])[:10])} vídeos mais recentes")
            print("💡 Para verificar lives, use o script completo")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL está correta")

if __name__ == "__main__":
    url = input("URL do canal: ")
    buscar_lives_rapido(url)