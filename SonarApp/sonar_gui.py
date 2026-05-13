import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sonar
import os
import descriptions_loader


class SonarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sonar Pro - AI Fish Recognition")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f8f9fa")

        self.model = None
        self.image_path = None

        app_dir = os.path.dirname(os.path.abspath(__file__))
        keras_models = [f for f in os.listdir(app_dir) if f.endswith(".keras")]
        if not keras_models:
            keras_models = ["No models found"]

        self.current_model_path = keras_models[0]

        title_font = ("Helvetica", 24, "bold")
        btn_font = ("Helvetica", 13, "bold")
        result_font = ("Helvetica", 16, "bold")

        tk.Label(root, text="Fishing Sonar AI", font=title_font, bg="#f8f9fa", fg="#2c3e50").pack(side=tk.TOP, pady=15)

        bottom_frame = tk.Frame(root, bg="#f8f9fa")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.img_frame = tk.Frame(root, bg="#e9ecef", bd=0, highlightbackground="#dee2e6", highlightthickness=2)
        self.img_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=30, pady=10)

        self.image_panel = tk.Label(self.img_frame, text="Select a fish image...", bg="#e9ecef", font=("Helvetica", 14),
                                    fg="#adb5bd")
        self.image_panel.pack(expand=True)

        model_frame = tk.Frame(bottom_frame, bg="#f8f9fa")
        model_frame.pack(pady=5)

        tk.Label(model_frame, text="Select Model:", font=("Helvetica", 12), bg="#f8f9fa").pack(side=tk.LEFT, padx=5)

        self.model_var = tk.StringVar(value=self.current_model_path)
        model_options = keras_models
        self.model_dropdown = tk.OptionMenu(model_frame, self.model_var, *model_options, command=self.on_model_change)
        self.model_dropdown.config(font=("Helvetica", 11), bg="white")
        self.model_dropdown.pack(side=tk.LEFT, padx=5)

        self.descriptions = descriptions_loader.get_descriptions_dict()

        btn_frame = tk.Frame(bottom_frame, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Image", font=btn_font, bg="#3498db", fg="white",
                  activebackground="#2980b9", activeforeground="white", relief=tk.FLAT,
                  width=15, cursor="hand2", command=self.load_image).grid(row=0, column=0, padx=10)

        self.btn_analyze = tk.Button(btn_frame, text="Analyze", font=btn_font, bg="#2ecc71", fg="white",
                                     activebackground="#27ae60", activeforeground="white", relief=tk.FLAT,
                                     width=15, cursor="hand2", state=tk.DISABLED, command=self.perform_analysis)
        self.btn_analyze.grid(row=0, column=1, padx=10)

        self.result_label = tk.Label(bottom_frame, text="Waiting for AI model...", font=result_font, bg="#f8f9fa", fg="#95a5a6")
        self.result_label.pack(pady=5)

        self.desc_label = tk.Label(bottom_frame, text="", font=("Helvetica", 12), bg="#f8f9fa", fg="#34495e", wraplength=1000)
        self.desc_label.pack(pady=5)

        self.root.after(100, self.setup_ai)

    def on_model_change(self, value):
        self.current_model_path = value
        self.result_label.config(text="Loading new model...", fg="#f39c12")
        self.root.update()
        self.setup_ai()

    def setup_ai(self):
        try:
            if self.current_model_path == "No models found":
                raise ValueError("No .keras model files found in the application folder")

            app_dir = os.path.dirname(os.path.abspath(__file__))
            full_model_path = os.path.join(app_dir, self.current_model_path)
            self.model = sonar.get_model(full_model_path)
            self.result_label.config(text="System Ready! Cast your line.", fg="#2ecc71")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}", fg="#e74c3c")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.image_path = path
            img = Image.open(path)

            img.thumbnail((800, 420), Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)
            self.image_panel.config(image=img_tk, text="")
            self.image_panel.image = img_tk

            self.btn_analyze.config(state=tk.NORMAL)
            self.result_label.config(text="Image loaded. Ready to analyze.", fg="#34495e")

    def perform_analysis(self):
        if self.model and self.image_path:
            self.result_label.config(text="Analyzing scales and fins...", fg="#f39c12")
            self.desc_label.config(text="")
            self.root.update()

            fish, confidence = sonar.predict_fish(self.model, self.image_path)

            if "Not recognized" not in fish:
                self.result_label.config(text=f"Fish: {fish}\nConfidence: {confidence:.2f}%", fg="#e74c3c")
                desc = self.descriptions.get(fish, "No description available for this species.")
                self.desc_label.config(text=desc)
            else:
                self.result_label.config(text=f"{fish}\nConfidence: {confidence:.2f}%", fg="#e74c3c")
                self.desc_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = SonarApp(root)
    root.mainloop()