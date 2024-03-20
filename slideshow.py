import os
import tkinter as tk
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SlideshowApp:
    def __init__(self, root, directory):
        self.root = root
        self.directory = directory
        self.image_files = []
        self.update_image_list()

        self.label = tk.Label(root)
        self.label.pack()

        self.show_image(0)
        self.observe_directory()

    def update_image_list(self):
        """Update the list of image files."""
        self.image_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    def show_image(self, index):
        """Show the image at the specified index."""
        if self.image_files:
            image_path = self.image_files[index % len(self.image_files)]
            image = Image.open(image_path)
            image = image.resize((800, 600), Image.ANTIALIAS)  # Resize to fit the window, if necessary
            photo = ImageTk.PhotoImage(image)

            self.label.config(image=photo)
            self.label.image = photo  # Keep a reference!

            # Schedule the next image
            self.root.after(5000, lambda: self.show_image(index + 1))

    def observe_directory(self):
        """Monitor the directory for changes and update the slideshow."""
        event_handler = FileSystemEventHandler()
        event_handler.on_created = lambda event: self.update_image_list()
        observer = Observer()
        observer.schedule(event_handler, self.directory, recursive=False)
        observer.start()

def main():
    root = tk.Tk()
    app = SlideshowApp(root, "..\latency\images") 
    root.mainloop()

if __name__ == "__main__":
    main()
