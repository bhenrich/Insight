import argparse
import os
import subprocess
import json
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("Module 'pyperclip' not installed. Clipboard copy functionality disabled.")

# ANSI color codes for terminal output
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"

# NerdFont icons (Unicode) for enhanced visual cues
ICON_INFO = "\uF05A"  # nf-fa-info_circle
ICON_DOWNLOAD = "\uF019" # nf-fa-download
ICON_FILTER = "\uF0B0" # nf-fa-filter
ICON_OPENAI = "\uEE9C"  # nf-fa-brain
ICON_CHECK = "\uF00C"  # nf-fa-check
ICON_ERROR = "\uF00D"  # nf-fa-times_circle
ICON_VIDEO = "\uF03D"  # nf-fa-video_camera
ICON_CLIPBOARD = "\uF0EA" # nf-fa-clipboard

# Global title variable to store video title
title = ""
client = OpenAI(os.getenv("OPENAI_API_KEY"))

def get_video_info(url):
    """
    Fetches video information using yt-dlp.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        dict: A dictionary containing video information in JSON format.
              Returns None and prints an error message if an error occurs.
    """
    try:
        command = ["yt-dlp", "--skip-download", "--print-json", url]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        return video_info
    except subprocess.CalledProcessError as e:
        print(f"{COLOR_RED}{ICON_ERROR} Error getting video info: yt-dlp returned {e.returncode}{COLOR_RESET}")
        print(f"{COLOR_RED}yt-dlp output:\n{e.stderr}{COLOR_RESET}")
        return None
    except json.JSONDecodeError as e:
        print(f"{COLOR_RED}{ICON_ERROR} Error parsing yt-dlp output: {e}{COLOR_RESET}")
        print(f"{COLOR_RED}yt-dlp output:\n{result.stdout}{COLOR_RESET}")
        return None
    except Exception as e:
        print(f"{COLOR_RED}{ICON_ERROR} An unexpected error occurred: {e}{COLOR_RESET}")
        return None

def download_captions(video_id, lang_code="en"):
    """
    Downloads captions for a YouTube video using youtube-transcript-api.

    Args:
        video_id (str): The ID of the YouTube video.
        lang_code (str, optional): Language code for captions (default: 'en').

    Returns:
        str: SRT formatted captions.
             Returns an error message string if download fails.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=[lang_code]
        )
        srt_captions = ""
        for entry in transcript:
            start_time = entry["start"]
            duration = entry["duration"]
            end_time = start_time + duration
            text = entry["text"].replace("\n", " ")
            srt_captions += f"{start_time} --> {end_time}\n{text}\n\n"
        return srt_captions
    except Exception as e:
        return f"{COLOR_RED}{ICON_ERROR} An error occurred: {e}{COLOR_RESET}"

def filter_captions(captions):
    """
    Filters and cleans the downloaded captions to extract only text lines.

    Args:
        captions (str): SRT formatted captions.

    Returns:
        str:  A string containing space-separated text lines from captions.
    """
    lines = captions.strip().split("\n")
    text_lines = [line for i, line in enumerate(lines) if (i - 1) % 3 == 0]
    return " ".join(text_lines)

def fetch_gpt3_response(prompt, max_tokens=4069):
    """
    Fetches a response from OpenAI's ChatGPT model.

    Args:
        prompt (str): The prompt message for the model.
        max_tokens (int, optional): Maximum tokens for the response (default: 4069).

    Returns:
        str: The response text from the model.
             Returns an error message string if fetching fails.
    """
    try:
        response = client.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant whose job is to explain a shortened version of information to the user."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"{COLOR_RED}{ICON_ERROR} Error fetching GPT-3 response: {e}{COLOR_RESET}"

def generate_standart_prompt(video_title, filtered_captions):
    """
    Generates the prompt for 'standart' mode.

    Args:
        video_title (str): Title of the YouTube video.
        filtered_captions (str): Filtered captions text.

    Returns:
        str: The prompt for standart summary mode.
    """
    return (
        f"Please summarize the following video script in a few sentences. The name of the YouTube Video is {video_title}. "
        "Filter out only the information and do not include any possible sponsored segments. "
        "ABSOLUTELY NEVER use phrases like 'the video explains', or 'the script argues', or 'the video discusses', "
        "instead just focus on the raw information, as if you were asked to explain the topic to someone without sounding like you learnt it in a YouTube video. "
        "Lastly again, completely ignore anything that seems like a sponsorship or a sponsored segment, or anything where someone directly talks about a product. "
        "Don't leave out any facts in the video. Simply lay out the explained information for easy digestion. "
        f"Here is the related video script:\n\n{filtered_captions}\n\nSummary:"
    )

def generate_bulletpoint_prompt(video_title, filtered_captions):
    """
    Generates the prompt for 'bulletpoint' mode.

    Args:
        video_title (str): Title of the YouTube video.
        filtered_captions (str): Filtered captions text.

    Returns:
        str: The prompt for bulletpoint summary mode.
    """
    return (
        f"Please summarize the following video script in concise bullet points using markdown syntax. The name of the YouTube Video is {video_title}. "
        "Filter out only the information and do not include any possible sponsored segments. "
        "ABSOLUTELY NEVER use phrases like 'the video explains', or 'the script argues', or 'the video discusses', "
        "instead just focus on the raw information, as if you were asked to explain the topic to someone without sounding like you learnt it in a YouTube video. "
        "Lastly again, completely ignore anything that seems like a sponsorship or a sponsored segment, or anything where someone directly talks about a product. "
        "Don't leave out any facts in the video. Simply lay out the explained information in bullet points for easy digestion and markdown formatting. "
        f"Here is the related video script:\n\n{filtered_captions}\n\nSummary in bullet points and markdown syntax:"
    )

def get_video_summary(video_url, video_lang="en", mode="standart", copy_to_clipboard=False):
    """
    Orchestrates the video summary process.

    Args:
        video_url (str): URL of the YouTube video.
        video_lang (str, optional): Language code for captions (default: 'en').
        mode (str, optional): Summary output mode ('standart' or 'bulletpoint', default: 'standart').
        copy_to_clipboard (bool, optional): Automatically copy summary to clipboard (default: False).

    Returns:
        str: The generated video summary. Returns None if an error occurs.
    """
    print(f"{COLOR_CYAN}{ICON_VIDEO} Processing video: {COLOR_YELLOW}{video_url}{COLOR_CYAN}, "
          f"Language: {COLOR_YELLOW}{video_lang}{COLOR_CYAN}, Mode: {COLOR_YELLOW}{mode}{COLOR_RESET}")

    video_info = get_video_info(video_url)
    if not video_info:
        return None

    global title  # Access the global title variable
    title = video_info['title']
    video_id = video_info['id']

    print(f"{COLOR_BLUE}{ICON_DOWNLOAD} Downloading Captions...{COLOR_RESET}")
    captions = download_captions(video_id, video_lang)
    if "Error occurred" in captions:
        print(f"{COLOR_RED}{ICON_ERROR} Failed to download captions.{COLOR_RESET}")
        print(captions)
        return None

    print(f"{COLOR_YELLOW}{ICON_FILTER} Filtering Captions...{COLOR_RESET}")
    filtered_captions = filter_captions(captions)

    if mode == "standart":
        prompt = generate_standart_prompt(title, filtered_captions)
    elif mode == "bulletpoint":
        prompt = generate_bulletpoint_prompt(title, filtered_captions)
    else:
        print(f"{COLOR_RED}{ICON_ERROR} Unknown mode selected: {mode}. Falling back to standart mode.{COLOR_RESET}")
        prompt = generate_standart_prompt(title, filtered_captions)

    print(f"{COLOR_MAGENTA}{ICON_OPENAI} Fetching OpenAI Response...{COLOR_RESET}")
    response = fetch_gpt3_response(prompt)
    if "Error fetching GPT-3 response" in response:
        print(f"{COLOR_RED}{ICON_ERROR} Failed to fetch OpenAI Response.{COLOR_RESET}")
        print(response)
        return None

    # --- Enhanced Summary Output ---
    separator = COLOR_CYAN + "-" * 50 + COLOR_RESET # Separator line

    print(f"\n{separator}")
    print(f"{COLOR_GREEN}{ICON_CHECK} {COLOR_BOLD}Summary ({mode.capitalize()} Mode):{COLOR_RESET}\n") # Bold Summary Title

    if mode == "bulletpoint": # Indent bullet points for bulletpoint mode
        bullet_lines = response.splitlines()
        for line in bullet_lines:
            print(f"  {line}") # Indent bullet points
    else:
        print(response + "\n")

    print(f"{separator}\n")


    if copy_to_clipboard:
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(response)
            print(f"{COLOR_BLUE}{ICON_CLIPBOARD} Summary copied to clipboard{COLOR_RESET}")
        else:
            print(f"{COLOR_YELLOW}{ICON_INFO} Clipboard copy requested but 'pyperclip' module is not installed.{COLOR_RESET}")

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a YouTube video.")
    parser.add_argument("video_url", help="The URL of the YouTube video.")
    parser.add_argument("--lang", default="en", help="The language of the captions (default: en).")
    parser.add_argument("--mode", "-m", default="standart", choices=["standart", "bulletpoint"], help="Output mode (standart or bulletpoint).")
    parser.add_argument("--copy", "-c", action="store_true", default=False, help="Automatically copy the summary to clipboard.") # Added copy argument
    args = parser.parse_args()

    get_video_summary(args.video_url, args.lang, args.mode, args.copy) # Pass copy_to_clipboard flag