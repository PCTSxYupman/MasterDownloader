import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import instaloader
from facebook_scraper import get_posts
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

def download_youtube_video(url, output_path='.'):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        file_size = stream.filesize
        pbar = tqdm(total=file_size, unit='B', unit_scale=True, desc=yt.title, ascii=True)

        def progress_function(chunk, file_handle, bytes_remaining):
            pbar.update(file_size - bytes_remaining)

        yt.register_on_progress_callback(progress_function)
        stream.download(output_path)
        pbar.close()
        
        print(f"\nDownloaded: {yt.title}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_tiktok_video(url, output_path='.'):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            video_url = None

            # Find the script tag containing the video URL
            for script in soup.find_all('script'):
                if 'videoObject' in script.text:
                    video_data = script.text.split('videoObject')[1].split('}')[-2] + '}'
                    video_url = eval(video_data)['contentUrl']
                    break

            if video_url:
                # Now you have the direct video URL, you can download or process it further
                print(f"Downloaded TikTok video from: {url}")
                print(f"Video URL: {video_url}")

                # Downloading the video
                file_name = f"{output_path}/tiktok_video.mp4"
                with requests.get(video_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                print(f"Saved video to: {file_name}")
            else:
                print("Video URL not found on the page.")
        else:
            print(f"Failed to fetch TikTok video: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_instagram_post(url, output_path='.'):
    try:
        L = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False, post_metadata_txt_pattern='')
        L.download_post(instaloader.Post.from_shortcode(L.context, url.split("/")[-2]), target=output_path)
        print(f"Downloaded Instagram post: {url}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_facebook_video(url, output_path='.'):
    try:
        # Placeholder for Facebook download code
        print("Facebook download functionality is not implemented.")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_spotify_track(track_url, client_id, client_secret, output_path='.'):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        track_info = sp.track(track_url)
        track_name = track_info['name']
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        print(f"Track: {track_name} by {artists} (URL: {track_url})")
        # Note: Actual downloading of Spotify tracks requires additional steps.
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the video URL: ")
    platform = input("Enter the platform (youtube, tiktok (doesnt work), instagram, facebook (doesnt work), spotify (requires spotify dev account): ").lower()
    
    output_path = '.'
    
    if platform == 'youtube':
        download_youtube_video(video_url, output_path)
    elif platform == 'tiktok':
        download_tiktok_video(video_url, output_path)
    elif platform == 'instagram':
        download_instagram_post(video_url, output_path)
    elif platform == 'facebook':
        download_facebook_video(video_url, output_path)
    elif platform == 'spotify':
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
        download_spotify_track(video_url, client_id, client_secret, output_path)
    else:
        print("Unsupported platform.")
