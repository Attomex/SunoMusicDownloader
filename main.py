import os
import requests
from bs4 import BeautifulSoup


def get_song_title(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        heading_tag = soup.select_one('.chakra-heading')
        if heading_tag:
            song_title = heading_tag.text.strip()
            return song_title
        else:
            print("No song title found.")
            return None
    except Exception as e:
        print(f"Error while parsing HTML: {e}")
        return None


def download_song_from_page(song_page_url, save_dir="music"):
    try:
        if not song_page_url.startswith("https://suno.com/song/"):
            raise ValueError(
                "Incorrect URL. It should start with 'https://suno.com/song/'")

        song_id = song_page_url.split('/')[-1]
        song_page_title = f"https://suno.com/embed/{song_id}"
        response_title = requests.get(song_page_title)
        if response_title.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        html = response_title.text
        song_title = get_song_title(html)
        if not song_title:
            return

        song_url = f"https://cdn1.suno.ai/{song_id}.mp3"

        file_name = f"{song_title}.mp3"
        file_path = os.path.join(save_dir, file_name)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        response = requests.get(song_url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
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
