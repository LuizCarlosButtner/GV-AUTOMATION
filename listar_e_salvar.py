import yt_dlp
from datetime import datetime

def listar_e_salvar_videos(url_canal):
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
            
            # Prepara conteúdo para salvar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"videos_{canal.replace(' ', '_')}_{timestamp}.txt"
            
            conteudo = f"Canal: {canal}\n"
            conteudo += f"Total de vídeos: {total_videos}\n"
            conteudo += f"Data da extração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            conteudo += "=" * 80 + "\n\n"
            
            # Lista e salva todos os vídeos
            for i, video in enumerate(info.get('entries', []), 1):
                titulo = video.get('title', 'Sem título')
                linha = f"{i:3d}. {titulo}\n"
                print(f"{i:3d}. {titulo}")
                conteudo += linha
            
            # Salva no arquivo
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            print("=" * 80)
            print(f"✅ Listagem completa: {total_videos} vídeos")
            print(f"💾 Lista salva em: {nome_arquivo}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se a URL do canal está correta")

if __name__ == "__main__":
    # Canal padrão sempre @mundogv
    url = "https://www.youtube.com/@mundogv"
    print(f"📺 Listando vídeos do canal: {url}")
    listar_e_salvar_videos(url)