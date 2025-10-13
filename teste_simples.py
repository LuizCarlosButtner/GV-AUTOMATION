import yt_dlp

url = "https://www.youtube.com/@mundogv"
ydl_opts = {'quiet': True, 'extract_flat': True, 'ignoreerrors': True}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    frase = "SUPER MUNDO GV SUPERBET - EPISÓDIO"
    count = 0
    
    for video in info.get('entries', []):
        titulo = video.get('title', '')
        if frase in titulo:
            count += 1
            print(f"{count}. {titulo}")
    
    print(f"\nTotal: {count} episódios")