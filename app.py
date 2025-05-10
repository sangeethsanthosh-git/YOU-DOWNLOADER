import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import os
import threading
import sys
from PIL import Image, ImageTk
import requests
from io import BytesIO

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("900x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(False, False)

        # Variables
        self.download_path = tk.StringVar(value=os.getcwd())
        self.url = tk.StringVar()
        self.audio_only = tk.BooleanVar(value=False)
        self.progress = tk.DoubleVar(value=0)
        self.video_options = []
        self.audio_options = [("320kbps", "320"), ("192kbps", "192"), ("128kbps", "128"), ("64kbps", "64")]
        self.selected_video_quality = tk.StringVar()
        self.selected_audio_quality = tk.StringVar(value="192kbps")
        self.is_running = True
        self.thumbnail_image = None

        # Apply a dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Helvetica', 10), foreground='white', background='#1C2526')
        self.style.configure('TButton', font=('Helvetica', 10), foreground='white', background='#4CAF50')
        self.style.configure('TCombobox', font=('Helvetica', 10), foreground='white', background='#2E3B3E')
        self.style.configure('TEntry', font=('Helvetica', 10), foreground='white', background='#2E3B3E')
        self.style.configure('TFrame', background='#1C2526')
        self.style.configure('TCheckbutton', background='#1C2526', foreground='white')
        self.style.configure('TProgressbar', background='#4CAF50', troughcolor='#2E3B3E')

        # Main container (Canvas for background thumbnail)
        self.canvas = tk.Canvas(self.root, bg='#1C2526', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Overlay for readability (semi-transparent background over thumbnail)
        self.overlay = self.canvas.create_rectangle(0, 0, 900, 600, fill='#1C2526', stipple='gray50')

        # URL Entry (Top-Center Position)
        self.url_frame = tk.Frame(self.root, bg='#1C2526')
        self.url_frame_window = self.canvas.create_window(450, 50, window=self.url_frame, anchor="n")
        ttk.Label(self.url_frame, text="Paste YouTube URL:").pack(side="left", padx=(0, 5))
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.url, width=50)
        self.url_entry.pack(side="left", padx=(0, 5))
        ttk.Button(self.url_frame, text="Check Formats", command=self.check_formats).pack(side="left")

        # Download Options Sidebar (Right Side)
        self.sidebar = ttk.Frame(self.root, style='TFrame', width=250)
        self.sidebar_window = self.canvas.create_window(650, 300, window=self.sidebar, anchor="center")

        # Sidebar Title
        ttk.Label(self.sidebar, text="Download Options", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Download Path
        ttk.Label(self.sidebar, text="Download Location:").pack(anchor="w", padx=10)
        path_frame = ttk.Frame(self.sidebar, style='TFrame')
        path_frame.pack(fill="x", padx=10, pady=2)
        ttk.Entry(path_frame, textvariable=self.download_path, width=20).pack(side="left", fill="x", expand=True)
        ttk.Button(path_frame, text="Browse", command=self.browse_path).pack(side="left", padx=5)

        # Download Mode
        ttk.Label(self.sidebar, text="Download Mode:").pack(anchor="w", padx=10, pady=2)
        self.mode = ttk.Combobox(self.sidebar, values=["Single Video", "Playlist"], state="readonly")
        self.mode.set("Single Video")
        self.mode.pack(anchor="w", padx=10, pady=2)

        # Audio Only Checkbox
        ttk.Checkbutton(self.sidebar, text="Audio Only", variable=self.audio_only, command=self.toggle_quality).pack(anchor="w", padx=10, pady=5)

        # Video Quality
        ttk.Label(self.sidebar, text="Video Quality:").pack(anchor="w", padx=10, pady=2)
        self.video_quality = ttk.Combobox(self.sidebar, textvariable=self.selected_video_quality, state="readonly")
        self.video_quality.pack(anchor="w", padx=10, pady=2)

        # Audio Quality
        ttk.Label(self.sidebar, text="Audio Quality:").pack(anchor="w", padx=10, pady=2)
        self.audio_quality = ttk.Combobox(self.sidebar, textvariable=self.selected_audio_quality, state="readonly")
        self.audio_quality['values'] = [opt[0] for opt in self.audio_options]
        self.audio_quality.set("192kbps")
        self.audio_quality.pack(anchor="w", padx=10, pady=2)

        # Download Button
        ttk.Button(self.sidebar, text="Download", command=self.start_download, style='Accent.TButton').pack(pady=20)
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=('Helvetica', 10, 'bold'))

        # Status Label (Bottom-Center)
        self.status_text = self.canvas.create_text(450, 550, text="Ready", font=('Helvetica', 10, 'italic'), fill='white')

    def load_thumbnail(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                if thumbnail_url:
                    response = requests.get(thumbnail_url)
                    img_data = BytesIO(response.content)
                    image = Image.open(img_data)
                    image = image.resize((900, 600), Image.Resampling.LANCZOS)
                    self.thumbnail_image = ImageTk.PhotoImage(image)
                    self.canvas.create_image(0, 0, image=self.thumbnail_image, anchor="nw", tags="thumbnail")
                    self.canvas.tag_raise(self.overlay)
                    self.canvas.tag_raise(self.url_frame_window)
                    self.canvas.tag_raise(self.sidebar_window)
                    self.canvas.tag_raise(self.status_text)
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            self.canvas.create_text(450, 300, text="No Preview Available", font=('Helvetica', 12), fill='white', tags="thumbnail_error")

    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.download_path.get())
        if path:
            self.download_path.set(path)

    def toggle_quality(self):
        if self.audio_only.get():
            self.video_quality.config(state="disabled")
            self.audio_quality.config(state="readonly")
        else:
            self.video_quality.config(state="readonly")
            self.audio_quality.config(state="disabled")

    def check_formats(self):
        url = self.url.get()
        if not url:
            self.canvas.itemconfig(self.status_text, text="Please enter a valid URL")
            return

        self.canvas.itemconfig(self.status_text, text="Fetching formats...")

        def fetch_formats():
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'format_sort': ['res', 'vcodec:avc', 'acodec']}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
                    formats = sorted(formats, key=lambda x: int(x.get('height', 0) or 0), reverse=True)

                    self.video_options = []
                    seen_heights = set()
                    for f in formats:
                        height = f.get('height')
                        if height and height not in seen_heights:
                            self.video_options.append((height, f['format_id']))
                            seen_heights.add(height)

                    self.root.after(0, lambda: self.update_video_quality())
                    self.root.after(0, lambda: self.load_thumbnail(url))
                    self.root.after(0, lambda: self.canvas.itemconfig(self.status_text, text="Formats loaded"))
            except Exception as e:
                self.root.after(0, lambda: self.canvas.itemconfig(self.status_text, text=f"Error: {str(e)}"))

        threading.Thread(target=fetch_formats, daemon=True).start()

    def update_video_quality(self):
        self.video_quality['values'] = [f"{height}p" for height, _ in self.video_options]
        if self.video_options and not self.audio_only.get():
            self.video_quality.set(f"{self.video_options[0][0]}p")
        else:
            self.video_quality.set("")

    def on_progress(self, d):
        if not self.is_running:
            return
        if d['status'] == 'downloading':
            percentage = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            self.progress.set(percentage)
            self.canvas.itemconfig(self.status_text, text=f"Downloading: {percentage:.2f}%")
        elif d['status'] == 'finished':
            self.progress.set(100)
            self.canvas.itemconfig(self.status_text, text="Download completed!")

    def download(self):
        url = self.url.get()
        download_path = self.download_path.get()
        is_audio_only = self.audio_only.get()
        mode = self.mode.get()
        selected_video = self.selected_video_quality.get()
        selected_audio = self.selected_audio_quality.get()

        if not url:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a YouTube URL"))
            return

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s' if mode == "Single Video" else '%(playlist_title)s/%(title)s.%(ext)s'),
            'progress_hooks': [self.on_progress],
            'noplaylist': mode == "Single Video",
            'merge_output_format': 'mp4',
            'format_sort': ['vcodec:avc', 'acodec:aac'],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'overwrites': True,
        }

        if is_audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            audio_bitrate = next(bitrate for name, bitrate in self.audio_options if name == selected_audio)
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_bitrate,
            }]
        else:
            if selected_video and self.video_options:
                selected_height = int(selected_video.replace('p', ''))
                format_id = next(fid for height, fid in self.video_options if height == selected_height)
                ydl_opts['format'] = f"{format_id}+bestaudio[ext=m4a]/bestaudio"
            else:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if self.is_running:
                self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
        except Exception as e:
            if self.is_running:
                self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            if self.is_running:
                self.root.after(0, lambda: self.canvas.itemconfig(self.status_text, text="Ready"))

    def start_download(self):
        self.progress.set(0)
        self.canvas.itemconfig(self.status_text, text="Starting download...")
        thread = threading.Thread(target=self.download)
        thread.start()

    def on_closing(self):
        self.is_running = False
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()
        sys.exit(0)