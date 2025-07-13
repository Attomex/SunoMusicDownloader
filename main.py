import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from mutagen.id3 import ID3, APIC, TIT2, TPE1, ID3NoHeaderError, TALB

def get_song_title(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.text.strip()
            song_title = title_text.replace(" | Suno", "")
            print(f"Song title: {song_title}")
            return song_title
        else:
            print("No song title found.")
            return None
    except Exception as e:
        print(f"Error while parsing HTML: {e}")
        return None
    
def get_song_img(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
        return None
    except Exception as e:
        print(f"Error while parsing HTML: {e}")
        return None

def get_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        html = page.content()
        browser.close()
        return html

def download_image(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def add_cover_to_mp3(mp3_path, cover_data, title, artist=None):
    try:
        # Create ID3 object
        try:
            audio = ID3(mp3_path)
        except ID3NoHeaderError:
            audio = ID3()
        
        # Delete old cover
        audio.delall('APIC')
        
        # Determine MIME type
        if cover_data.startswith(b'\xFF\xD8'):
            mime = 'image/jpeg'
        elif cover_data.startswith(b'\x89PNG'):
            mime = 'image/png'
        else:
            mime = 'image/jpeg'
        
        # Add cover
        audio.add(APIC(
            encoding=3,
            mime=mime,
            type=3,
            desc='Cover',
            data=cover_data
        ))
        
        # Update tags
        audio.delall('TIT2')
        audio.add(TIT2(encoding=3, text=title))
        
        if artist:
            audio.delall('TPE1')
            audio.add(TPE1(encoding=3, text=artist))
        
        audio.delall('TALB')
        audio.add(TALB(encoding=3, text='Suno Track'))
        
        # Save tags without padding
        audio.save(mp3_path, v2_version=3)
        return True
        
    except Exception as e:
        print(f"[add_cover] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def download_song_from_page(song_page_url, save_dir="music"):
    try:
        if not song_page_url.startswith("https://suno.com/song/"):
            raise ValueError("Incorrect URL. It should start with 'https://suno.com/song/'")

        song_id = song_page_url.split('/')[-1]
        song_page_title = f"https://suno.com/embed/{song_id}"

        try:
            response_title = get_rendered_html(song_page_title)
        except Exception as e:
            print(f"Playwright error: {e}")
            return
        
        song_title = get_song_title(response_title)
        if not song_title:
            return

        # Get cover image
        cover_url = get_song_img(response_title)
        cover_data = None
        if cover_url:
            cover_data = download_image(cover_url)

        # Download song
        song_url = f"https://cdn1.suno.ai/{song_id}.mp3"
        file_name = f"{song_title}.mp3"
        file_name = file_name.replace('"', "")
        file_path = os.path.join(save_dir, file_name)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        response = requests.get(song_url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            
            # Add cover to mp3
            if cover_data:
                if add_cover_to_mp3(file_path, cover_data, song_title):
                    print(f"Cover added to {file_name}")
                else:
                    print(f"Failed to add cover to {file_name}")
            
            print(f"{file_name} downloaded in {file_path}")
        else:
            print(f"Download error {file_name}: {response.status_code}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"There's been an error: {e}")

if __name__ == "__main__":
    print("Software for downloading music from suno.com")
    print("Go to suno.com, pick a song you like, go to the song page and copy the link.")
    print("Example link: https://suno.com/song/eaba4d6e-f7ab-4bc4-a48b-6e2c8d859dbc")
    print("Paste the link at the bottom and press Enter.")
    while True:
        song_page_url = input(f"\nEnter a link to the song's page: ")
        download_song_from_page(song_page_url)
        if (input("Would you like to continue? (y/n): ") == "n"):
            break