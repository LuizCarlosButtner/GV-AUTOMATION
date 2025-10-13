import yt_dlp

def buscar_lives(url_canal):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Não baixa detalhes de cada vídeo
        'playlistend': 50,
        'ignoreerrors': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("🔍 Buscando vídeos do canal...")
            info = ydl.extract_info(url_canal, download=False)
            
            print(f"🎥 Canal: {info.get('uploader', info.get('channel', 'N/A'))}")
            print(f"📊 Total de vídeos: {len(info.get('entries', []))}")
            print("=" * 60)
            
            # Agora busca detalhes apenas dos primeiros vídeos
            ydl_detailed = yt_dlp.YoutubeDL({'quiet': True, 'ignoreerrors': True})
            
            lives_encontradas = 0
            for i, video in enumerate(info.get('entries', [])[:20], 1):
                try:
                    print(f"⏳ Verificando vídeo {i}/20...", end="\r")
                    
                    # Extrai detalhes do vídeo
                    video_info = ydl_detailed.extract_info(video['url'], download=False)
                    
                    if video_info.get('is_live') or video_info.get('was_live'):
                        lives_encontradas += 1
                        titulo = video_info.get('title', 'Sem título')[:70]
                        duracao = video_info.get('duration', 0)
                        
                        if duracao:
                            h, m, s = duracao//3600, (duracao%3600)//60, duracao%60
                            duracao_str = f"{h:02d}:{m:02d}:{s:02d}"
                        else:
                            duracao_str = "🔴 AO VIVO" if video_info.get('is_live') else "N/A"
                        
                        status = "🔴 LIVE" if video_info.get('is_live') else "📹 PASSADA"
                        
                        print(f"\n{status} - {titulo}")
                        print(f"⏱️ Duração: {duracao_str}")
                        print("-" * 40)
                        
                except Exception as e:
                    print(f"\n❌ Erro no vídeo {i}: {str(e)[:50]}...")
                    continue
            
            print(f"\n✅ Busca concluída! Lives encontradas: {lives_encontradas}")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        print("💡 Tente com uma URL diferente ou verifique sua conexão")

if __name__ == "__main__":
    url = input("URL do canal: ")
    buscar_lives(url)