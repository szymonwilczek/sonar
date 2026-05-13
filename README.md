# Sonar Pro - AI Fish Recognition

Sonar Pro is an artificial intelligence-based application designed to identify various species of fish from images. Built with Python, TensorFlow/Keras, and Tkinter, it provides a user-friendly desktop interface to analyze images, providing real-time predictions along with detailed descriptions of the recognized fish.

**Note on Development Workflow:** The heavy deep learning model training for this project was conducted on [Kaggle](https://www.kaggle.com) to leverage their GPU acceleration. The data collection, inference logic, and the graphical user interface (GUI) are developed and executed entirely locally.

## Features

- **AI-Powered Fish Identification:** Uses a pre-trained EfficientNetB0 model to classify images of fish into various categories (Polish local species, Ocean species, Sharks, etc.).
- **Desktop GUI:** Built with Tkinter, allowing users to select an image, choose a model version, and view the results interactively.
- **Dynamic Model Selection:** Automatically detects available `.keras` model files in the application directory and allows switching between them dynamically.
- **Detailed Descriptions:** Pulls data from a local CSV file to provide comprehensive information about the recognized fish (Habitat, Average Size, Description).
- **Stealth Data Scraper:** Includes a robust DuckDuckGo image scraper (`scraper.py`) with retry mechanisms to gather training datasets locally.

## Technologies Used

- **Python 3.13+**
- **TensorFlow / Keras:** For loading the pre-trained EfficientNetB0 architecture and running inference.
- **Tkinter:** For the graphical user interface.
- **Pillow (PIL):** For image processing and display in the GUI.
- **Pandas:** For loading and managing fish descriptions from a CSV file.
- **FastAI & DuckDuckGo Search (DDGS):** Used in the scraper script for automated dataset creation.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/szymonwilczek/sonar
   cd sonar
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   Make sure your `pip` is up to date. You can install the key dependencies manually:
   ```bash
   pip install tensorflow pandas pillow fastai duckduckgo_search
   ```

4. **Verify Models:**
   Ensure your `.keras` model files (e.g., `sonar_fish_model_ULTRA_V3_final.keras`) are placed inside the `SonarApp/` directory.

## Usage

1. Navigate to the application directory:
   ```bash
   cd SonarApp
   ```
2. Run the application:
   ```bash
   python sonar_gui.py
   ```
3. In the GUI:
   - Select your preferred AI model from the dropdown menu.
   - Click **Load Image** to select a fish photo from your computer.
   - Click **Analyze** to process the image and see the prediction and details.

## Project Structure

- `SonarApp/sonar_gui.py`: The main entry point for the Desktop Application.
- `SonarApp/sonar.py`: AI inference module; handles model initialization and image prediction.
- `SonarApp/descriptions_loader.py`: Module to parse `descriptions.csv` for species info.
- `scraper.py`: A script for downloading images from DuckDuckGo to build a training dataset.
- `pyproject.toml` / `uv.lock`: Project configuration and dependency lockfiles.

## Documentation

For a detailed breakdown of the system architecture, Kaggle training workflow, and component interactions, please refer to the [DOCUMENTATION.md](DOCUMENTATION.md).
