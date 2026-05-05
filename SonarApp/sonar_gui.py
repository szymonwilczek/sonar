import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sonar


class SonarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sonar Pro - AI Fish Recognition")
        self.root.geometry("800x800")
        self.root.configure(bg="#f8f9fa")

        self.model = None
        self.image_path = None

        title_font = ("Helvetica", 24, "bold")
        btn_font = ("Helvetica", 13, "bold")
        result_font = ("Helvetica", 16, "bold")

        tk.Label(root, text="Fishing Sonar AI", font=title_font, bg="#f8f9fa", fg="#2c3e50").pack(pady=25)

        self.img_frame = tk.Frame(root, bg="#e9ecef", bd=0, highlightbackground="#dee2e6", highlightthickness=2)
        self.img_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)

        self.image_panel = tk.Label(self.img_frame, text="Select a fish image...", bg="#e9ecef", font=("Helvetica", 14),
                                    fg="#adb5bd")
        self.image_panel.pack(expand=True)

        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Load Image", font=btn_font, bg="#3498db", fg="white",
                  activebackground="#2980b9", activeforeground="white", relief=tk.FLAT,
                  width=15, cursor="hand2", command=self.load_image).grid(row=0, column=0, padx=10)

        self.btn_analyze = tk.Button(btn_frame, text="Analyze", font=btn_font, bg="#2ecc71", fg="white",
                                     activebackground="#27ae60", activeforeground="white", relief=tk.FLAT,
                                     width=15, cursor="hand2", state=tk.DISABLED, command=self.perform_analysis)
        self.btn_analyze.grid(row=0, column=1, padx=10)

        self.result_label = tk.Label(root, text="Waiting for AI model...", font=result_font, bg="#f8f9fa", fg="#95a5a6")
        self.result_label.pack(pady=20)

        self.root.after(100, self.setup_ai)

    def setup_ai(self):
        try:
            self.model = sonar.get_model()
            self.result_label.config(text="System Ready! Cast your line.", fg="#2ecc71")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}", fg="#e74c3c")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.image_path = path
            img = Image.open(path)

            img.thumbnail((700, 550), Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)
            self.image_panel.config(image=img_tk, text="")
            self.image_panel.image = img_tk

            self.btn_analyze.config(state=tk.NORMAL)
            self.result_label.config(text="Image loaded. Ready to analyze.", fg="#34495e")

    def perform_analysis(self):
        if self.model and self.image_path:
            self.result_label.config(text="Analyzing scales and fins...", fg="#f39c12")
            self.root.update()

            fish, confidence = sonar.predict_fish(self.model, self.image_path)

            self.result_label.config(text=f"Fish: {fish}\nConfidence: {confidence:.2f}%", fg="#e74c3c")


if __name__ == "__main__":
    root = tk.Tk()
    app = SonarApp(root)
    root.mainloop()