![INSIGHT Logo](./ASSETS/INSIGHT_Logo.png)

## Description

**Insight** is a command-line interface (CLI) tool designed to quickly and efficiently summarize YouTube videos. Leveraging the power of `yt-dlp` for video information and caption extraction, `youtube-transcript-api` for transcript retrieval, and OpenAI's cutting-edge language models for summarization, Insight provides concise summaries in your terminal.

Whether you need a quick overview in a few sentences or a structured breakdown in bullet points, Insight offers flexible modes to suit your needs, helping you grasp the essence of video content without watching the entire duration.

## Features

  * **Multiple Summary Modes:**
      * **Standart Mode (Default):** Generates a summary in a few concise sentences, ideal for a quick overview.
      * **Bulletpoint Mode:** Provides a summary in markdown-formatted bullet points, perfect for structured and easily digestible information.
  * **Configurable Output:**
      * **Language Selection:** Specify the caption language using the `--lang` or `-l` tag.
      * **Mode Selection:** Choose between `standart` and `bulletpoint` modes using the `--mode` or `-m` tag.
  * **Clipboard Integration:** Automatically copy the generated summary to your clipboard with the `--copy` or `-c` flag for seamless use in notes or documents.
  * **Formatted Terminal Output:** Enjoy a clean and readable summary directly in your terminal, enhanced with colors, icons, and structured formatting.
  * **Modular Prompt System:** Easily extensible architecture for adding new summary modes in the future.
  * **Powered by OpenAI:** Utilizes the advanced `chatgpt-4o-latest` model for high-quality and informative summaries.

## Installation

1.  **Prerequisites:**

      * **Python 3.7+**
      * **pip** (Python package installer)
      * **yt-dlp:**  Follow the installation instructions on the [yt-dlp releases page](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/yt-dlp/yt-dlp/releases). Ensure `yt-dlp` is in your system's PATH.
      * **OpenAI API Key:** You will need an OpenAI API key to use the summarization features. Set your API key in the `api_key` variable within the Python script.

2.  **Install Python Packages:**

    Clone the repository (if you create one) or save the Python script (`your_script_name.py`). Then, navigate to the script's directory in your terminal and install the required Python packages using pip:

    ```bash
    pip install youtube-transcript-api openai pyperclip
    ```

      * `youtube-transcript-api`: For fetching YouTube video transcripts.
      * `openai`:  The official OpenAI Python library.
      * `pyperclip`: (Optional) For clipboard copy functionality. Install if you want to use the `--copy` flag.

## Usage

Run `insight` (or `your_script_name.py` if you haven't renamed it) from your terminal with a YouTube video URL as the argument.

**Basic Usage (Standart Mode, English Captions):**

```bash
python your_script_name.py <YouTube_Video_URL>
```

**Example:**

```bash
python your_script_name.py [https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
```

**Options:**

  * **`--lang <language_code>`, `-l <language_code>`:**  Specify the language of the captions (e.g., `en`, `es`, `de`). Defaults to `en` (English).

    ```bash
    python your_script_name.py --lang de <YouTube_Video_URL>
    python your_script_name.py -l es <YouTube_Video_URL>
    ```

  * **`--mode <mode>`, `-m <mode>`:** Choose the summary output mode. Available modes: `standart`, `bulletpoint`. Defaults to `standart`.

    ```bash
    python your_script_name.py --mode bulletpoint <YouTube_Video_URL>
    python your_script_name.py -m bulletpoint <YouTube_Video_URL>
    ```

  * **`--copy`, `-c`:**  Copy the generated summary to your clipboard automatically.

    ```bash
    python your_script_name.py --copy <YouTube_Video_URL>
    python your_script_name.py -c <YouTube_Video_URL>
    python your_script_name.py -m bulletpoint -c <YouTube_Video_URL> # Bulletpoint mode and copy to clipboard
    ```

**Help:**

For a full list of options, run:

```bash
python your_script_name.py --help
```

## Dependencies

  * Python 3.7+
  * yt-dlp
  * youtube-transcript-api
  * openai
  * pyperclip (optional, for clipboard functionality)

## Future Enhancements

  * Support for more output modes (e.g., detailed summary, key takeaways).
  * Configuration file for persistent settings (API key, default mode, etc.).
  * Error handling improvements and more informative error messages.
  * Potential integration with other services or platforms.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://www.google.com/url?sa=E&source=gmail&q=LICENSE.md) file for details.