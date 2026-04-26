---
theme:
    name: terminal-dark
    override:
        footer:
            style: template
            left: "Project SONAR | Fish Classification System"
            right: "{current_slide} / {total_slides}"
---

<!-- jump_to_middle -->
# Project SONAR 🐋

## Deep Learning for Advanced Fish Classification

Authors: Szymon Wilczek, Bartosz Kaprak 

<!-- end_slide -->
Why Fish Classification?

<!-- pause -->

# 🌍 Biodiversity Monitoring
Helping marine biologists track species populations in the wild.

<!-- pause -->

# 🏭 Commercial Use
Automating catch logging and quality control in the seafood industry.

<!-- pause -->

# 🎣 Educational Tool
Assisting anglers and hobbyists in identifying local catches.

<!-- end_slide -->
The "Master Dataset" Strategy

We combined multiple data sources to create a robust system of ~100 classes.

COLUMN_LAYOUT: [1, 1]

COLUMN: 0

## 1. Core Base
9 commercial species from academic sources.

## 2. Predator Expansion
14 species of sharks including Mako and Great White.

COLUMN: 1

## 3. Marine Animals
Additional aquatic life: Seals, Jellyfish, Rays.

## 4. Sonar Local
Our custom-curated collection of Polish freshwater species.

RESET_LAYOUT

<!-- end_slide -->
Data Gathering: Custom Scraper

We built an automated pipeline to gather specific local data.

# 🔍 Local Search
Targeting specific Polish species like Pike, Zander, and Wels Catfish.

<!-- pause -->

# 📥 Automated Download
Filtering images directly from search engines to match our needs.

<!-- pause -->

# 🛠️ Data Cleaning
Automatic verification and removal of corrupted or irrelevant files using fastai tools.

<!-- end_slide -->
Preprocessing & Augmentation

To make SONAR battle-ready for real-world photos.

# 🔄 Image Augmentation
The model sees every fish in multiple versions:


TODO: punktacja


Rotated at various angles.

Zoomed in and out.

Flipped horizontally.

<!-- pause -->

[!caution]
Without augmentation, models memorize the background instead of the fish!

<!-- end_slide -->
Architecture: Transfer Learning

Using the "brains" of world-class neural networks.

# 🧠 Base Model
Leveraging ResNet50V2 and MobileNetV2.

<!-- pause -->

# 📚 Pre-trained Knowledge
The model already knows how to see edges, textures, and scales.

<!-- pause -->

# 🎯 Custom Head
We only trained the final layers to focus specifically on our 100+ fish species.

<!-- end_slide -->
Performance Metrics

# 🚀 Initial Success
Achieved 99.37% Accuracy on the primary commercial dataset.

<!-- pause -->

# 📈 Scaling Up
Maintained high precision even after expanding to ~100 classes.

<!-- pause -->

# 🧪 Stability
Used Dropout layers and Regularization to ensure reliable results.

<!-- end_slide -->
User Interface: Gradio

SONAR is a functional tool, not just a Python script.

# 💻 Interactive UI
A web-based interface where users can drag and drop photos.

<!-- pause -->

# ⏱️ Real-time Inference
The model analyzes the image and returns the top 3 results in seconds.

<!-- end_slide -->
Conclusions & Future Scope

# ✅ Takeaways

TODO: punktacja

Transfer Learning is the most efficient path for specialized tasks.

Data quality is more important than sheer volume.

<!-- pause -->

# 🔭 Future Plans


TODO: punktacja
Mobile Deployment: Moving SONAR to smartphones via TFLite.

Object Detection: Transitioning to YOLOv11 to count multiple fish.

<!-- end_slide -->

<!-- jump_to_middle -->
Thank you for your attention!

## 🐟 Any questions?
