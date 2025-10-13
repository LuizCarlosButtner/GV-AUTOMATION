import yt_dlp

def extrair_lives_canal(url_canal):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 50,  # Limita a 50 vídeos para teste
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extrai informações do canal
            info = ydl.extract_info(url_canal, download=False)
            
            print(f"Canal: {info.get('uploader', 'N/A')}")
            print(f"Total de vídeos encontrados: {len(info['entries'])}")
            print("-" * 60)
            
            lives_encontradas = 0
            
            for video in info['entries']:
                # Extrai detalhes de cada vídeo
                video_info = ydl.extract_info(video['url'], download=False)
                
                # Verifica se é live ou foi live
                is_live = video_info.get('is_live', False)
                was_live = video_info.get('was_live', False)
                
                if is_live or was_live:
                    lives_encontradas += 1
                    titulo = video_info.get('title', 'Sem título')
                    duracao = video_info.get('duration', 0)
                    
                    # Converte duração para formato legível
                    if duracao:
                        horas = duracao // 3600
                        minutos = (duracao % 3600) // 60
                        segundos = duracao % 60
                        duracao_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                    else:
                        duracao_str = "Em andamento" if is_live else "N/A"
                    
                    status = "🔴 AO VIVO" if is_live else "📹 LIVE PASSADA"
                    
                    print(f"{status}")
                    print(f"Título: {titulo}")
                    print(f"Duração: {duracao_str}")
                    print(f"URL: {video['url']}")
                    print("-" * 40)
            
            print(f"\nTotal de lives encontradas: {lives_encontradas}")
            
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    # Exemplo de uso - substitua pela URL do canal desejado
    url_canal = input("Digite a URL do canal do YouTube: ")
    extrair_lives_canal(url_canal)