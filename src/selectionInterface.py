# This file was created by ChatGPT (GPT-5.6 Luna, OpenAI). August 30, 2026

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from urllib.parse import urlparse


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DVD Generator")
        self.root.resizable(False, False)

        self.result = None
        self.submitted = False

        # ─────────────────────────────────────
        # Download file / URL
        # ─────────────────────────────────────

        tk.Label(
            root,
            text="Download file or link:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=(10, 5),
            sticky="w"
        )

        self.inputEntry = tk.Entry(root, width=40)
        self.inputEntry.grid(
            row=0,
            column=1,
            padx=10,
            pady=(10, 5)
        )
        self.inputEntry.insert(0, "Download.txt")

        tk.Button(
            root,
            text="Browse...",
            command=self.browse
        ).grid(
            row=0,
            column=2,
            padx=(0, 10),
            pady=(10, 5)
        )

        # ─────────────────────────────────────
        # Image source selection
        # ─────────────────────────────────────

        tk.Label(
            root,
            text="Image Source:"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.imageMode = tk.StringVar(value="local")

        self.localRadio = tk.Radiobutton(
            root,
            text="Local JPGs",
            variable=self.imageMode,
            value="local",
            command=self.update_image_mode
        )
        self.localRadio.grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.youtubeRadio = tk.Radiobutton(
            root,
            text="YouTube Channel",
            variable=self.imageMode,
            value="youtube",
            command=self.update_image_mode
        )
        self.youtubeRadio.grid(
            row=2,
            column=2,
            padx=(0, 10),
            pady=5,
            sticky="w"
        )

        # ─────────────────────────────────────
        # Local JPG frame
        # ─────────────────────────────────────

        self.localFrame = tk.Frame(root)

        # YouTuber name
        tk.Label(
            self.localFrame,
            text="YouTuber name:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.nameEntry = tk.Entry(self.localFrame, width=40)
        self.nameEntry.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        # JPG 1
        tk.Label(
            self.localFrame,
            text="Chapter Page Background:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.jpg1Entry = tk.Entry(
            self.localFrame,
            width=40
        )
        self.jpg1Entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        tk.Button(
            self.localFrame,
            text="Browse...",
            command=lambda: self.browse_image(self.jpg1Entry)
        ).grid(
            row=1,
            column=2,
            padx=(0, 10),
            pady=5
        )

        # JPG 2
        tk.Label(
            self.localFrame,
            text="Chapter Background:"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.jpg2Entry = tk.Entry(
            self.localFrame,
            width=40
        )
        self.jpg2Entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=5
        )

        tk.Button(
            self.localFrame,
            text="Browse...",
            command=lambda: self.browse_image(self.jpg2Entry)
        ).grid(
            row=2,
            column=2,
            padx=(0, 10),
            pady=5
        )

        # JPG 3
        tk.Label(
            self.localFrame,
            text="Channel Picture:"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.jpg3Entry = tk.Entry(
            self.localFrame,
            width=40
        )
        self.jpg3Entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=5
        )

        tk.Button(
            self.localFrame,
            text="Browse...",
            command=lambda: self.browse_image(self.jpg3Entry)
        ).grid(
            row=3,
            column=2,
            padx=(0, 10),
            pady=5
        )

        # ─────────────────────────────────────
        # YouTube frame
        # ─────────────────────────────────────

        self.youtubeFrame = tk.Frame(root)

        tk.Label(
            self.youtubeFrame,
            text="YouTube Channel:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.youtubeEntry = tk.Entry(
            self.youtubeFrame,
            width=40
        )
        self.youtubeEntry.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        # Example
        tk.Label(
            self.youtubeFrame,
            text="Example: https://www.youtube.com/@MrBeast",
            fg="gray"
        ).grid(
            row=1,
            column=1,
            columnspan=2,
            padx=10,
            pady=(0, 5),
            sticky="w"
        )

        # ─────────────────────────────────────
        # MP3
        # ─────────────────────────────────────

        self.musicFrame = tk.Frame(root)

        tk.Label(
            self.musicFrame,
            text="Background Music:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.mp3Entry = tk.Entry(
            self.musicFrame,
            width=40
        )
        self.mp3Entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        tk.Button(
            self.musicFrame,
            text="Browse...",
            command=self.browse_mp3
        ).grid(
            row=0,
            column=2,
            padx=(0, 10),
            pady=5
        )

        self.musicFrame.grid(
            row=5,
            column=0,
            columnspan=3
        )

        # ─────────────────────────────────────
        # Run button
        # ─────────────────────────────────────

        self.runButton = tk.Button(
            root,
            text="Run",
            width=15,
            command=self.submit
        )
        self.runButton.grid(
            row=6,
            column=0,
            columnspan=3,
            pady=10
        )

        # ─────────────────────────────────────
        # Status message
        # ─────────────────────────────────────

        self.statusLabel = tk.Label(
            root,
            text="Ready",
            anchor="center"
        )
        self.statusLabel.grid(
            row=7,
            column=0,
            columnspan=3,
            padx=10,
            pady=(0, 10)
        )

        # ─────────────────────────────────────
        # Show initial image mode
        # ─────────────────────────────────────

        self.update_image_mode()

    # ─────────────────────────────────────────
    # Image mode
    # ─────────────────────────────────────────

    def update_image_mode(self):
        """Show the controls for the currently selected image source."""

        self.localFrame.grid_forget()
        self.youtubeFrame.grid_forget()

        if self.imageMode.get() == "local":

            self.localFrame.grid(
                row=3,
                column=0,
                columnspan=3
            )

            # Keep music below the local JPG controls
            self.musicFrame.grid_configure(row=6)
            self.runButton.grid_configure(row=7)
            self.statusLabel.grid_configure(row=8)

        else:

            self.youtubeFrame.grid(
                row=3,
                column=0,
                columnspan=3
            )

            # Move music up because YouTube mode only has one field
            self.musicFrame.grid_configure(row=5)
            self.runButton.grid_configure(row=6)
            self.statusLabel.grid_configure(row=7)

    # ─────────────────────────────────────────
    # Browse functions
    # ─────────────────────────────────────────

    def browse(self):
        """Open a file explorer and let the user choose a download file."""

        filename = filedialog.askopenfilename(
            title="Select Download File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.inputEntry.delete(0, tk.END)
            self.inputEntry.insert(0, filename)

    def browse_image(self, entry):
        """Open a file explorer and select a JPG image."""

        filename = filedialog.askopenfilename(
            title="Select JPG Image",
            filetypes=[
                ("JPEG images", "*.jpg *.jpeg"),
                ("JPG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )

        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def browse_mp3(self):
        """Open a file explorer and select an MP3."""

        filename = filedialog.askopenfilename(
            title="Select MP3",
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.mp3Entry.delete(0, tk.END)
            self.mp3Entry.insert(0, filename)

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    def is_url(self, value):
        """Return True if the input looks like an HTTP/HTTPS URL."""

        try:
            parsed = urlparse(value)

            return (
                parsed.scheme in ("http", "https")
                and bool(parsed.netloc)
            )

        except Exception:
            return False

    def is_youtube_channel(self, value):
        """
        Check whether the supplied URL looks like a YouTube channel URL.

        Supports:
            /@handle
            /channel/UC...
            /c/...
            /user/...
        """

        try:
            parsed = urlparse(value)

            if parsed.scheme not in ("http", "https"):
                return False

            hostname = parsed.netloc.lower()

            # Remove www.
            if hostname.startswith("www."):
                hostname = hostname[4:]

            if hostname not in (
                "youtube.com",
                "m.youtube.com"
            ):
                return False

            path = parsed.path.rstrip("/")

            return (
                path.startswith("/@")
                or path.startswith("/channel/")
                or path.startswith("/c/")
                or path.startswith("/user/")
            )

        except Exception:
            return False

    # ─────────────────────────────────────────
    # Submit
    # ─────────────────────────────────────────

    def submit(self):
        """Validate the input and save the selected values."""

        myInput = self.inputEntry.get().strip()

        mp3 = self.mp3Entry.get().strip()

        image_mode = self.imageMode.get()

        # ─────────────────────────────────────
        # Defaults
        # ─────────────────────────────────────

        if not myInput:
            myInput = "Download.txt"

        # ─────────────────────────────────────
        # Validate download input
        # ─────────────────────────────────────

        if self.is_url(myInput):

            pass

        else:

            try:
                if not Path(myInput).is_file():

                    messagebox.showerror(
                        "Error",
                        f"File not found:\n\n{myInput}"
                    )

                    return

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Could not check the file:\n\n{e}"
                )

                return

        # ─────────────────────────────────────
        # Image source
        # ─────────────────────────────────────

        ytName = None
        jpg1 = None
        jpg2 = None
        jpg3 = None
        youtube_channel = None

        # ─────────────────────────────────────
        # Local JPG mode
        # ─────────────────────────────────────

        if image_mode == "local":

            jpg1 = self.jpg1Entry.get().strip()
            jpg2 = self.jpg2Entry.get().strip()
            jpg3 = self.jpg3Entry.get().strip()
            ytName = self.nameEntry.get().strip()
            if not ytName:
                ytName = "default"

            jpg_files = {
                "Background.jpg": jpg1,
                "ChapterBackground.jpg": jpg2,
                "ChannelPic.jpg": jpg3
            }

            # All three are required in local mode
            for filename, jpg in jpg_files.items():

                if not jpg:

                    messagebox.showerror(
                        "Error",
                        f"Please select:\n\n{filename}"
                    )

                    return

                path = Path(jpg)

                if not path.is_file():

                    messagebox.showerror(
                        "Error",
                        f"JPG file was not found:\n\n{jpg}"
                    )

                    return

                if path.suffix.lower() not in (
                    ".jpg",
                    ".jpeg"
                ):

                    messagebox.showerror(
                        "Error",
                        f"File must be a JPG:\n\n{jpg}"
                    )

                    return

        # ─────────────────────────────────────
        # YouTube mode
        # ─────────────────────────────────────

        elif image_mode == "youtube":

            youtube_channel = self.youtubeEntry.get().strip()

            if not youtube_channel:

                messagebox.showerror(
                    "Error",
                    "Please enter a YouTube channel URL."
                )

                return

            if not self.is_youtube_channel(youtube_channel):

                messagebox.showerror(
                    "Error",
                    "Please enter a valid YouTube channel URL.\n\n"
                    "Examples:\n"
                    "https://www.youtube.com/@MrBeast\n"
                    "https://www.youtube.com/channel/UC..."
                )

                return

        # ─────────────────────────────────────
        # Validate MP3
        # ─────────────────────────────────────

        if mp3:

            mp3_path = Path(mp3)

            if not mp3_path.is_file():

                messagebox.showerror(
                    "Error",
                    f"MP3 file was not found:\n\n{mp3}"
                )

                return

            if mp3_path.suffix.lower() != ".mp3":

                messagebox.showerror(
                    "Error",
                    f"Selected audio file must be an MP3:\n\n{mp3}"
                )

                return

        # ─────────────────────────────────────
        # Submit
        # ─────────────────────────────────────

        self.result = (
            myInput,
            ytName,
            {
                "ImageMode": image_mode,

                "Background.jpg": jpg1,
                "ChapterBackground.jpg": jpg2,
                "ChannelPic.jpg": jpg3,

                "YouTubeChannel": youtube_channel,

                "Music.mp3": mp3 if mp3 else None
            }
        )

        self.submitted = True

        self.statusLabel.config(
            text="Generating DVD..."
        )

        self.runButton.config(
            state=tk.DISABLED
        )

        self.root.after(
            100,
            self.check_submission
        )

    # ─────────────────────────────────────────
    # Submission check
    # ─────────────────────────────────────────

    def check_submission(self):
        """Check whether the user has submitted the form."""

        if self.submitted:

            self.root.quit()

        else:

            self.root.after(
                100,
                self.check_submission
            )

    # ─────────────────────────────────────────
    # Finish
    # ─────────────────────────────────────────

    def finish(self):
        """Called by main() when DVD generation is completely finished."""

        self.statusLabel.config(
            text="Finished successfully!"
        )

        messagebox.showinfo(
            "Success",
            "DVD generation has finished successfully."
        )

        self.root.destroy()


_app = None


def getInput():
    global _app

    root = tk.Tk()
    _app = App(root)

    root.mainloop()

    return _app.result


def finish():
    """Tell the GUI that main() has finished generating the DVD."""

    global _app

    if _app is not None:
        _app.finish()
