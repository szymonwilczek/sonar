from ddgs import DDGS
from fastai.vision.utils import download_images, verify_images
from fastai.vision.core import get_image_files
from pathlib import Path
import time
import os
import random

def search_images_safe(term, max_images=100):
    print(f"Searching for: {term}...")
    for attempt in range(5):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(keywords=term, max_results=max_images))
                return [r['image'] for r in results]
        except Exception as e:
            wait_time = 15 + (attempt * 10) # 15s, 25s, 35s...
            print(f"  -> DDG is blocking home IP. Waiting {wait_time} seconds... (Attempt {attempt+1}/5)")
            time.sleep(wait_time)
    return []

gatunki_pl_total = {
    'Karp': 'karp ryba cyprinus carpio underwater',
    'Amur_Bialy': 'amur biały grass carp underwater',
    'Leszcz': 'leszcz ryba abramis brama',
    'Krap': 'krąp ryba blicca bjoerkna',
    'Ploc': 'płoć ryba roach fish',
    'Wzdrega': 'wzdręga krasnopiórka rudd fish',
    'Lin': 'lin ryba tinca tinca',
    'Brzana': 'brzana pospolita barbus barbus',
    'Bolen': 'boleń rapa asp fish',
    'Klen': 'kleń ryba chub fish',
    'Jaz': 'jaź ryba ide fish',
    'Ukleja': 'ukleja pospolita alburnus alburnus',
    'Kielb': 'kiełb pospolity gudgeon fish',
    'Certa': 'certa ryba vimba vimba',
    'Swinka': 'świnka ryba chondrostoma nasus',
    'Szczupak': 'szczupak ryba esox lucius underwater',
    'Okon': 'okoń europejski perch underwater',
    'Sandacz': 'sandacz pospolity zander underwater',
    'Sum_Europejski': 'sum europejski wels catfish underwater',
    'Mietus': 'miętus ryba burbot',
    'Wegorz_Europejski': 'węgorz europejski anguilla anguilla',
    'Jazgarz': 'jazgarz ryba ruffe fish',
    'Lipien': 'lipień europejski thymallus thymallus',
    'Glowacica': 'głowacica ryba hucho hucho',
    'Troc_Wedrowna': 'troć wędrowna salmo trutta trutta',
    'Sielawa': 'sielawa ryba vendace',
    'Fladra_Stornia': 'stornia flądra platichthys flesus',
    'Belona': 'belona ryba garfish',
    'Tolpyga_Biala': 'tołpyga biała silver carp',
    'Tolpyga_Pstara': 'tołpyga pstra bighead carp',
    'Karas_Pospolity': 'karaś złocisty carassius carassius',
    'Karas_Srebrzysty': 'karaś srebrzysty japanczyk',
    'Kielb_Krotkopletwy': 'kiełb krótkopłetwy gobio gobio',
    'Jelec': 'jelec ryba leuciscus leuciscus',
    'Rozpior': 'rozpiór ryba ballerus ballerus',
    'Piekielnica': 'piekielnica ryba alburnoides bipunctatus',
    'Sumik_Karlowaty': 'sumik karłowaty ameiurus nebulosus',
    'Ciernik': 'ciernik ryba gasterosteus aculeatus',
    'Pstrag_Potokowy': 'pstrąg potokowy salmo trutta fario',
    'Pstrag_Tecczowy': 'pstrąg tęczowy rainbow trout',
    'Pstrag_Zrodlany': 'pstrąg źródlany brook trout',
    'Losos_Atlantycki': 'łosoś atlantycki salmo salar',
    'Sieja': 'sieja ryba coregonus lavaretus',
    'Dorsz': 'dorsz bałtycki gadus morhua',
    'Sledz_Baltycki': 'śledź bałtycki clupea harengus',
    'Szprot': 'szprot ryba sprattus sprattus',
    'Gladzica': 'gładzica ryba pleuronectes platessa',
    'Turbot': 'turbot ryba scophthalmus maximus',
    'Kur_Diabel': 'kur diabeł ryba myoxocephalus scorpius'
}

path = Path('MASTER_DATASET')
path.mkdir(exist_ok=True)

print("--- RUNNING SONAR SCRAPER (Stealth version - 100 images) ---")
for nazwa_folderu, haslo_wyszukiwania in gatunki_pl_total.items():
    dest = path / nazwa_folderu
    dest.mkdir(exist_ok=True, parents=True)
    
    if len(list(dest.glob('*.jpg'))) + len(list(dest.glob('*.png'))) > 85:
        print(f"[SKIPPED] {nazwa_folderu} - already enough images.")
        continue

    urls = search_images_safe(haslo_wyszukiwania, max_images=100)
    
    if urls:
        print(f"[DOWNLOADING] {nazwa_folderu}: found {len(urls)} links.")
        download_images(dest, urls=urls)
    
    oddech = random.uniform(6, 12)
    time.sleep(oddech)

print("\n--- DOWNLOAD FINISHED ---")
print("Scanning and deleting broken files (this will take a moment)...")
failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
print(f"Deleted {len(failed)} broken files. Your MASTER_DATASET is clean!")
