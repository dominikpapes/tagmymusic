from pathlib import Path
from mutagen.flac import FLAC
import argparse
import os

# https://github.com/moehmeni/syncedlyrics
import syncedlyrics

def normalize_title(title):
    """Normalize FLAC title by replacing dashes and ticks."""
    title = title.replace("—", "-").replace("–", "-")
    title = title.replace("`", "'").replace("’", "'")
    return title

def process_flac_file(file_path):
    audio = FLAC(file_path)

    # Normalize title
    original_title = audio.get('title', ['Unknown Title'])[0]
    normalized_title = normalize_title(original_title)
    if normalized_title != original_title:
        audio['title'] = normalized_title
        audio.save()
        print(f"Normalized title: {file_path} -> {normalized_title}")
    else:
        print(f"No title normalization needed: {file_path}")

    # Get artist for lyrics search
    artist = audio.get('albumartist', ['Unknown Artist'])[0]

    # Search for lyrics
    lrc = syncedlyrics.search(f"{artist} {normalized_title}", plain_only="true", providers=["Lrclib"])
    status = f"{artist}: {normalized_title} - "
    if lrc:
        audio["lyrics"] = lrc
        audio.save()
        status += "Lyrics found."
    else:
        status += "Lyrics not found."
    print(status)

def main():
    parser = argparse.ArgumentParser(description="Normalize FLAC titles and get lyrics")
    parser.add_argument('directory')
    args = parser.parse_args()

    directory = Path(args.directory)
    print(f"Processing FLAC files in directory: {directory}")

    for path, folders, files in os.walk(directory):
        for filename in files:
            file = os.path.join(path, filename)
            if os.path.isfile(file) and file.lower().endswith('.flac'):
                try:
                    process_flac_file(file)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    main()
