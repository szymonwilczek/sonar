import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image

CLASS_NAMES = ['Ocean_Goldfish', 'Ocean_Harbor_seal', 'Ocean_Jellyfish', 'Ocean_Lobster', 'Ocean_Oyster', 'Ocean_Sea_turtle', 'Ocean_Squid', 'Ocean_Starfish', 'PL_Amur_Bialy', 'PL_Belona', 'PL_Bolen', 'PL_Brzana', 'PL_Certa', 'PL_Ciernik', 'PL_Dorsz', 'PL_Fladra_Stornia', 'PL_Gladzica', 'PL_Glowacica', 'PL_Jaz', 'PL_Jazgarz', 'PL_Jelec', 'PL_Karas_Pospolity', 'PL_Karas_Srebrzysty', 'PL_Karp', 'PL_Kielb', 'PL_Kielb_Krotkopletwy', 'PL_Klen', 'PL_Krap', 'PL_Kur_Diabel', 'PL_Leszcz', 'PL_Lin', 'PL_Lipien', 'PL_Losos_Atlantycki', 'PL_Mietus', 'PL_Okon', 'PL_Piekielnica', 'PL_Ploc', 'PL_Pstrag_Potokowy', 'PL_Pstrag_Tecczowy', 'PL_Pstrag_Zrodlany', 'PL_Rozpior', 'PL_Sandacz', 'PL_Sieja', 'PL_Sielawa', 'PL_Sledz_Baltycki', 'PL_Sum_Europejski', 'PL_Sumik_Karlowaty', 'PL_Swinka', 'PL_Szczupak', 'PL_Szprot', 'PL_Tolpyga_Biala', 'PL_Tolpyga_Pstara', 'PL_Troc_Wedrowna', 'PL_Turbot', 'PL_Ukleja', 'PL_Wegorz_Europejski', 'PL_Wzdrega', 'Shark_basking', 'Shark_blacktip', 'Shark_blue', 'Shark_bull', 'Shark_hammerhead', 'Shark_lemon', 'Shark_mako', 'Shark_nurse', 'Shark_sand_tiger', 'Shark_thresher', 'Shark_tiger', 'Shark_whale', 'Shark_white', 'Shark_whitetip', 'Turbo_Bighead_carp', 'Turbo_Blackchin_Tilapia', 'Turbo_Carp', 'Turbo_Catfish', 'Turbo_Climbing_Perch', 'Turbo_Freshwater_Eel', 'Turbo_Goby', 'Turbo_Gold_Fish', 'Turbo_Gourami', 'Turbo_Indian_Carp', 'Turbo_Indo-pacific_Tarpon', 'Turbo_Jaguar_Guapote', 'Turbo_Janitor_Fish', 'Turbo_Knife_Fish', 'Turbo_Manila_Catfish', 'Turbo_Milkfish', 'Turbo_Mosquito_Fish', 'Turbo_Mudfish', 'Turbo_Mullet', 'Turbo_Scat_Fish', 'Turbo_Silver_Barb', 'Turbo_Silver_Carp', 'Turbo_Silver_Perch', 'Turbo_Tenpounder', 'Turbo_Tilapia']

MODEL_PATH = 'sonar_fish_model_ULTRA.keras'


def get_model():
    """Buduje szkielet i ładuje wagi modelu."""
    print("Inicjalizacja silnika AI...")

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.15),
    ])

    base_model = tf.keras.applications.EfficientNetB0(
        input_shape=(224, 224, 3), include_top=False, weights=None
    )

    model = tf.keras.Sequential([
        data_augmentation,
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(len(CLASS_NAMES), activation='softmax')
    ])

    model.build((None, 224, 224, 3))

    if os.path.exists(MODEL_PATH):
        model.load_weights(MODEL_PATH)
        return model
    else:
        raise FileNotFoundError(f"Nie znaleziono pliku {MODEL_PATH}")


def predict_fish(model, img_path):
    """Przyjmuje model i ścieżkę do zdjęcia, zwraca nazwę i pewność."""
    img = keras_image.load_img(img_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)
    idx = np.argmax(predictions[0])
    confidence = 100 * np.max(predictions[0])

    label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Nieznany ({idx})"
    return label, confidence