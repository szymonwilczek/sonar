# Sonar Pro - Full Project Documentation

## 1. Introduction
Sonar Pro is an end-to-end Machine Learning project aimed at classifying images of fish across multiple categories (including local Polish species, ocean fish, and various sharks). This documentation provides an in-depth look at the system architecture, the hybrid development approach (Local Data Prep & Inference + Kaggle Training), and the responsibilities of each module.

## 2. System Architecture & Workflow

The project follows a decoupled workflow, separating the heavy computational task of model training from local execution and data gathering.

### Phase 1: Data Collection (Local)
Data gathering is handled by `scraper.py`. It uses the DuckDuckGo Search API (`DDGS`) to look up images for a predefined dictionary of fish species (`gatunki_pl_total`).
- **Stealth and Safety:** Implements exponential backoff and delay randomization to avoid IP blocking from search engines.
- **Validation:** Uses FastAI's `verify_images` to scan downloaded files and automatically remove corrupt or broken images.
- **Output:** The script generates a clean, organized `MASTER_DATASET` directory locally, categorized by fish species.

### Phase 2: Model Training (Kaggle Workflow)
Because image classification with deep learning requires significant computational power, the model training was intentionally offloaded to **Kaggle**.
- **Process:** The `MASTER_DATASET` generated locally is uploaded to Kaggle as a custom dataset.
- **Architecture:** The model leverages **EfficientNetB0**, a highly efficient and accurate Convolutional Neural Network (CNN). The base model is initialized without top layers (`include_top=False`).
- **Data Augmentation:** Random flips, rotations (15%), and zooming (15%) are applied directly within the model sequential pipeline to make it robust against varied image inputs.
- **Custom Head:** A Global Average Pooling layer, followed by a Dropout layer (30% for regularization), and a final Dense layer with a `softmax` activation function are added on top of the base model.
- **Export:** After training on Kaggle's GPU accelerators, the final model weights are exported as `.keras` files (e.g., `sonar_fish_model_ULTRA_V3_final.keras`) and downloaded back to the local machine.

### Phase 3: Inference & GUI (Local)
The final application runs entirely locally. It loads the downloaded Kaggle models and provides an interactive GUI for the user to perform inference.

---

## 3. Component Breakdown

### `SonarApp/sonar_gui.py`
The frontend of the application, built using the standard Python `tkinter` library.
- **Initialization:** Scans the `SonarApp` folder for `.keras` files and populates a dropdown menu. This allows users to dynamically switch between different model versions (e.g., PRO vs ULTRA).
- **Image Handling:** Uses `PIL` (Pillow) to open, resize (using LANCZOS resampling to fit the UI panel), and display the selected image.
- **Integration:** Calls `sonar.predict_fish()` when the user clicks "Analyze" and displays the returned species and confidence score.
- **Details Integration:** Fetches species information from `descriptions_loader.py` and updates the UI label to provide context to the user.

### `SonarApp/sonar.py`
The core AI engine wrapper.
- **`get_model(model_path)`:** Reconstructs the exact `EfficientNetB0` architecture used during Kaggle training. It builds the sequential layers (augmentation -> base_model -> pooling -> dropout -> dense) and successfully loads the `.keras` weights from the disk.
- **`predict_fish(model, img_path)`:** 
  1. Loads and resizes the target image to `224x224` pixels (the standard input size for EfficientNetB0).
  2. Expands dimensions to match the batch format `(1, 224, 224, 3)`.
  3. Runs `model.predict()`.
  4. Identifies the class with the highest probability.
  5. **Thresholding:** Applies a confidence threshold of **33.0%**. If the highest prediction falls below this, the system returns `"Not recognized (Object out of knowledge scope)"` to prevent false positives on random images.

### `SonarApp/descriptions_loader.py`
A data utility using `pandas`.
- **Functionality:** Reads `descriptions.csv` located in the `SonarApp` directory.
- **Formatting:** Concatenates the species Name, Description, Habitat, and Average Size into a single formatted string.
- **Output:** Returns a Python dictionary mapping the `Class_Name` (matching the model's output exactly) to the formatted descriptive string.

### `scraper.py`
The automated dataset builder.
- Uses `DDGS` (DuckDuckGo Search) to find image URLs safely.
- Uses `fastai.vision.utils.download_images` for parallel downloading.
- Maps Polish fish names (e.g., 'Karp', 'Szczupak') to effective, multi-lingual search queries (e.g., 'szczupak ryba esox lucius underwater') to ensure high-quality dataset images that match real-world fishing scenarios.

---

## 4. Class Categories (The Knowledge Scope)
The model is trained on a wide array of classes (defined in `CLASS_NAMES` inside `sonar.py`), which are broadly categorized into:
- **`PL_` (Polish Species):** Local freshwater and Baltic species like Pike (Szczupak), Perch (Okon), Carp (Karp), Zander (Sandacz), etc.
- **`Ocean_`:** General ocean creatures like Sea Turtles, Jellyfish, Lobsters, etc.
- **`Shark_`:** Specific shark species including Great White, Tiger, Hammerhead, Mako, etc.
- **`Turbo_`:** Additional freshwater and commercial species globally (Tilapia, Milkfish, Mudfish, etc.).

---

## 5. Extensibility & Upgrades
Because the GUI dynamically discovers and loads models at runtime, iterating on the AI is completely decoupled from the software logic. To improve the model's accuracy or add new fish species:
1. Run `scraper.py` locally to gather more images for new or struggling classes.
2. Upload the updated dataset to Kaggle.
3. Retrain the model on Kaggle and download the new `.keras` weights file.
4. Place the new `.keras` file into the `SonarApp/` directory.
5. Launch the application; the new model will automatically appear in the dropdown menu.
