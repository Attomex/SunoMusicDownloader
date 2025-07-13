
# Music Downloader for Suno.com

This Python script allows you to download songs directly from [Suno.com](https://suno.com). It extracts the song title and downloads the associated MP3 file to your local device.

## Features

- Automatically fetches song titles from Suno.com song pages.
- Downloads MP3 files with appropriate titles.
- Supports saving files in a user-specified directory (default is `music`).

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone this repository or download the script.
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Usage

1. Run the script:
   ```bash
   python script_name.py
   ```

2. Follow the prompts in the terminal:
   - Copy the link of a song page from Suno.com (e.g., `https://suno.com/song/<song_id>`).
   - Paste the link into the terminal when prompted.

3. The script will:
   - Extract the song title from the page.
   - Download the MP3 file to the `music` directory (or create the directory if it doesn’t exist).

### Example

```bash
$ python script_name.py
Software for downloading music from suno.com
Go to suno.com, pick a song you like, go to the song page and copy the link.
Example link: https://suno.com/song/eaba4d6e-f7ab-4bc4-a48b-6e2c8d859dbc

Enter a link to the song's page: https://suno.com/song/eaba4d6e-f7ab-4bc4-a48b-6e2c8d859dbc
Song_Name.mp3 downloaded in music/Song_Name.mp3
Would you like to continue? (y/n): n
```

## Directory Structure

The downloaded files will be stored in the `music` directory (or a directory you specify in the `save_dir` argument).

## Error Handling

- Ensures the provided URL starts with `https://suno.com/song/`.
- Gracefully handles network errors, missing song titles, or failed downloads.
- Prints descriptive error messages for easier debugging.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Feel free to open issues or submit pull requests if you'd like to contribute to this project. Suggestions and improvements are welcome!
