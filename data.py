import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd

class ImageLabeler:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ Image Labeling Tool")
        self.image_files = []
        self.current_index = 0
        self.labels = {}
        self.label_options = ["cat", "dog", "car", "tree", "other"]

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.label_var = tk.StringVar()
        self.label_menu = tk.OptionMenu(root, self.label_var, *self.label_options)
        self.label_menu.pack()

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        tk.Button(self.btn_frame, text="Previous", command=self.prev_image).pack(side="left")
        tk.Button(self.btn_frame, text="Save Label", command=self.save_label).pack(side="left")
        tk.Button(self.btn_frame, text="Next", command=self.next_image).pack(side="left")
        tk.Button(self.btn_frame, text="Export CSV", command=self.export_labels).pack(side="left")

        self.load_images()

    def load_images(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if not folder:
            self.root.quit()
        self.image_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        self.show_image()

    def show_image(self):
        if 0 <= self.current_index < len(self.image_files):
            img_path = self.image_files[self.current_index]
            img = Image.open(img_path).resize((400, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)
            self.label_var.set(self.labels.get(img_path, self.label_options[0]))

    def save_label(self):
        img_path = self.image_files[self.current_index]
        self.labels[img_path] = self.label_var.get()
        messagebox.showinfo("Saved", f"Labeled as '{self.label_var.get()}'")

    def next_image(self):
        self.save_label()
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def export_labels(self):
        df = pd.DataFrame(list(self.labels.items()), columns=["image_path", "label"])
        df.to_csv("labeled_data.csv", index=False)
        messagebox.showinfo("Exported", "Labels saved to labeled_data.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabeler(root)
    root.mainloop()


