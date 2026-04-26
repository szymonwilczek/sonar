# Slide 2: The Motivation & Problem Statement

### Why Fish Classification?
* **Biodiversity Monitoring:** Assisting marine biologists in tracking species populations.
* **Commercial Applications:** Automating catch logging in fisheries and supermarkets.
* **Educational Tool:** Helping anglers identify local catches (e.g., Polish freshwater species).

### The Challenge
* **High Intra-class Variance:** Fish of the same species can look vastly different based on age, lighting, and water clarity.
* **Data Imbalance:** Some species (e.g., Carp, Pike) have millions of images online, while others are rare.

---
# Slide 3: The "Master Dataset" Strategy

To make Sonar a robust system, we didn't rely on a single source. We built a **Multi-Source Master Dataset** containing ~100 species.

**Data Sources:**
1. **The Core Base:** A Large-Scale Fish Dataset (Izmir University) - 9 commercial species.
2. **The Predator Expansion:** Kaggle Shark Species Dataset (Mako, Great White, Tiger).
3. **The Global Expansion:** 50+ mixed marine species.
4. **The Local Touch:** Custom-scraped Polish freshwater species.

---
# Slide 4: Data Gathering - The Custom Scraper

To include local Polish species, we developed an automated pipeline using `duckduckgo_search` and `fastai`. 

```python
# Snippet: Automated Image Scraping & Verification
from duckduckgo_search import DDGS
from fastai.vision.utils import download_images, verify_images

def search_images_safe(term, max_images=100):
    with DDGS() as ddgs:
        results = list(ddgs.images(keywords=term, max_results=max_images))
        return [r['image'] for r in results]

# Example: Gathering local species
urls = search_images_safe('szczupak ryba esox lucius underwater')
download_images(dest_folder, urls=urls)

# Crucial: Removing corrupted files before training
failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
```

---

Slide 5: Data Preprocessing & Augmentation

Deep Learning models are data-hungry. To prevent overfitting and make the model robust against poor-quality smartphone photos, we applied real-time Image Augmentation.

```python
# Snippet: Data Augmentation Pipeline
train_datagen = ImageDataGenerator(
    rescale=1./255,           # Normalizing pixel values (0 to 1)
    rotation_range=30,        # Simulating different camera angles
    width_shift_range=0.2,    # Handling off-center subjects
    height_shift_range=0.2,
    zoom_range=0.2,           # Simulating distance
    horizontal_flip=True,     # Fish swim in both directions!
    validation_split=0.2      # Reserving 20% for testing
)
```

---

Slide 6: System Architecture - Transfer Learning

Training a deep Convolutional Neural Network (CNN) from scratch requires massive computational power. We utilized Transfer Learning.

Base Model: ResNet50V2 (or MobileNetV2 for agility).

Pre-trained Weights: ImageNet (millions of general images).

Strategy: Freeze the base layers (feature extractors) and train a custom "classification head" exclusively on our Master Dataset.

---

Slide 7: Model Compilation

We replaced the top layer of the pre-trained model with a custom network capable of distinguishing our specific number of classes.


```python
# Snippet: Building the Sonar Model
base_model = ResNet50V2(weights='imagenet', include_top=False, 
                        input_shape=(224, 224, 3))
base_model.trainable = False # Freezing feature extractors

model = Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5), # Regularization to prevent memorization
    layers.Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', 
              metrics=['accuracy'])

```

---

Slide 8: Training & Performance Metrics

Hardware: Google Colab (GPU T4).

Initial Results (9 Classes): Achieved 99.37% Validation Accuracy.

Master Dataset Results (80+ Classes): Maintaining high accuracy despite massive class expansion.

Note: Sudden spikes in validation loss were mitigated using Early Stopping and Dropout layers.


---

Slide 9: User Interface - The "Warstwa Odpowiedzi"

A model is only as good as its usability. Instead of a raw terminal output, we deployed a rapid, interactive web interface using Gradio.

```python
# Snippet: Real-time inference UI
import gradio as gr

def predict_fish(img):
    img_resized = cv2.resize(img, (224, 224))
    img_batch = np.expand_dims(img_resized / 255.0, axis=0)
    prediction = model.predict(img_batch)[0]
    return {labels[i]: float(prediction[i]) for i in range(len(labels))}

interface = gr.Interface(fn=predict_fish, inputs=gr.Image(), 
                         outputs=gr.Label(num_top_classes=3))

```

---

Slide 10: Conclusion & Future Scope
Key Takeaways

Transfer Learning is highly effective for specialized biological classification.

Data curation (cleaning scraped data) is more critical than simply having more data.

Future Development

Object Detection: Upgrading from Image Classification to YOLOv11 to detect multiple fish in one frame and draw bounding boxes.

Mobile Deployment: Exporting the .h5 model to TensorFlow Lite for an offline Android/iOS app.

Addressing Long-Tail Distribution: Gathering more data for rare Polish species (e.g., Piekielnica) to balance the dataset further.

Thank You! Questions?

