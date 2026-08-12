# image_classifier.py — simple image quality & logo detector
import io, math, requests
from PIL import Image, ImageStat
import numpy as np

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


# --- Compute entropy (image clarity) ---
def _entropy(img):
    """Shannon entropy: measures texture/clarity of an image."""
    hist = img.histogram()
    hist_size = sum(hist)
    probs = [float(h) / hist_size for h in hist if h != 0]
    return -sum([p * math.log(p, 2) for p in probs])


def compute_image_features(url):
    """
    Downloads the image and extracts simple features.
    Returns dict: {ok, width, height, size_kb, entropy, brightness}
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        img_bytes = io.BytesIO(r.content)
        img = Image.open(img_bytes).convert('RGB')
    except Exception as e:
        return {'ok': False, 'error': str(e)}

    try:
        width, height = img.size
        stat = ImageStat.Stat(img)
        brightness = sum(stat.mean) / (len(stat.mean) * 255)
        ent = _entropy(img.convert('L'))

        # file size in KB
        size_kb = len(r.content) / 1024

        return {
            'ok': True,
            'width': width,
            'height': height,
            'size_kb': round(size_kb, 2),
            'entropy': round(ent, 2),
            'brightness': round(brightness, 2)
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def simple_logo_likely(url):
    """
    Very basic heuristic: returns True if the image is probably just a logo,
    placeholder, or solid color background.
    """
    f = compute_image_features(url)
    if not f.get('ok'):
        return False
    # low entropy and very small size or high brightness → likely logo
    if f['entropy'] < 3.0 or f['size_kb'] < 15 or f['brightness'] > 0.95:
        return True
    return False
