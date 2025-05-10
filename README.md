# YOU-DOWNLOADER
YouTube Downloader GUI
Overview
YouTube Downloader GUI is a Python-based desktop application designed to download videos and audio from YouTube with a user-friendly interface. Built using tkinter for the GUI and yt_dlp for downloading, the application features a dark-themed design with a canvas-based layout that displays the video thumbnail as the background. It supports downloading single videos or playlists, with options to choose video quality or extract audio in various bitrates.
Features

Dynamic Thumbnail Background: Displays the YouTube video thumbnail as the background when a URL is entered.
Download Options Sidebar: Includes settings for download location, mode (single video or playlist), audio-only toggle, video quality, and audio quality (64kbps to 320kbps).
Dark Theme: A sleek dark interface with white text and green buttons for better readability.
Real-Time Status Updates: Shows progress and status messages (e.g., "Fetching formats...", "Downloading: 50.00%", "Download completed!").
Threaded Operations: Uses threading to prevent GUI freezing during format fetching and downloading.
Error Handling: Provides user-friendly error messages for invalid URLs or download paths.

Installation

Clone the Repository:
git clone https://github.com/yourusername/youtube-downloader-gui.git
cd youtube-downloader-gui


Install Python:Ensure you have Python 3.6 or higher installed. You can download it from python.org.

Install Dependencies:Install the required Python libraries using pip:
pip install yt-dlp Pillow requests


yt-dlp: For downloading YouTube videos and audio.
Pillow: For handling thumbnail images.
requests: For fetching thumbnails.


Install FFmpeg:FFmpeg is required for audio extraction and video merging. Download and install it from ffmpeg.org or via a package manager:

On Windows: Download the binary and add it to your system PATH.
On macOS: brew install ffmpeg
On Linux: sudo apt-get install ffmpeg


Run the Application:Execute the main script to launch the application:
python app.py



Usage

Launch the Application:Run the script to open the YouTube Downloader window.

Enter a YouTube URL:Paste a YouTube video or playlist URL in the top entry field and click "Check Formats" to load available video qualities and display the thumbnail in the background.

Configure Download Options:

Download Location: Select a folder to save the downloaded files.
Download Mode: Choose between "Single Video" or "Playlist".
Audio Only: Toggle to download audio only (MP3 format).
Video Quality: Select from available resolutions (e.g., 1080p, 720p).
Audio Quality: Choose the bitrate for audio downloads (e.g., 192kbps).


Start Downloading:Click the "Download" button to begin the download process. The status label at the bottom will show real-time progress.

Monitor Progress:Watch the status updates (e.g., "Downloading: 50.00%"). A success or error message will appear when the download completes.


Dependencies

Python 3.6+
yt-dlp: For downloading YouTube content.
Pillow: For processing and displaying thumbnails.
requests: For fetching thumbnail images.
tkinter: For the GUI (included with Python).
FFmpeg: For audio extraction and video merging.

Screenshots
Main interface with URL entry, download options sidebar, and thumbnail background.
Legal Notice
Downloading videos from YouTube may violate YouTube's Terms of Service unless you have explicit permission from the content owner or are downloading your own content. Use this application responsibly and at your own risk. The developers are not responsible for any misuse or legal consequences arising from the use of this software.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the application. Potential enhancements include:

Adding a progress bar for downloads.
Supporting more video platforms.
Implementing a cancel download feature.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with yt-dlp for YouTube downloading.
Uses Pillow for image processing.
Inspired by the need for a simple, user-friendly YouTube downloader.

