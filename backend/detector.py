# detector.py — Final version (with Slides & Shoes)
from image_classifier import compute_image_features

SUSPICIOUS_KEYWORDS = ['replica', 'copy', 'duplicate', 'knockoff', 'fake', 'unbranded', 'imitation', 'clone']
REAL_KEYWORDS = ['original', 'genuine', 'authentic', 'official', 'licensed']


def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


def detect_fake_product(details):
    """
    Category-aware detector with hard price rules:
      • Smartphones < ₹2000  → Fake
      • Smartwatches < ₹500  → Fake
      • Earbuds < ₹400       → Fake
      • Shoes < ₹350         → Fake
      • Slides < ₹300        → Fake
    """
    title = (details.get('title') or '').lower()
    desc = (details.get('description') or '').lower()
    price = _safe_float(details.get('price'))
    brand = (details.get('brand') or '').lower()
    image_url = details.get('image_url') or ''
    text = title + ' ' + desc
    reasons = []

    # -------- CATEGORY DETECTION --------
    if any(k in text for k in ['earbud', 'earphone', 'neckband', 'buds', 'airdopes']):
        category = 'earbuds'
    elif any(k in text for k in ['phone', 'smartphone', 'mobile', 'iphone', 'galaxy', 'oneplus']):
        category = 'smartphone'
    elif any(k in text for k in ['watch', 'smartwatch', 'fitbit', 'fastrack']):
        category = 'watch'
    elif any(k in text for k in ['shoe', 'sneaker']):
        category = 'shoes'
    elif any(k in text for k in ['slide', 'slipper']):
        category = 'slides'
    else:
        category = 'other'

    # -------- HARD PRICE RULES --------
    hard_limit = {
        'smartphone': 2000,
        'watch': 500,
        'earbuds': 400,
        'shoes': 350,
        'slides': 300
    }

    if category in hard_limit and price is not None and price < hard_limit[category]:
        reasons.append(f"{category.capitalize()} priced below ₹{hard_limit[category]} → automatically Fake.")
        return {
            'label': 'Fake',
            'confidence': 0.99,
            'category': category,
            'reasons': reasons,
            'image_features': None
        }

    # -------- TEXT SCORE --------
    text_score = 0.5
    for w in REAL_KEYWORDS:
        if w in text:
            text_score += 0.12
    for w in SUSPICIOUS_KEYWORDS:
        if w in text:
            text_score -= 0.3
    if 'apple' in brand or 'iphone' in title:
        text_score += 0.1
    if 'samsung' in brand or 'samsung' in title:
        text_score += 0.05
    text_score = max(0.0, min(1.0, text_score))

    # -------- PRICE SCORE (for non-hard cases) --------
    if price is None:
        price_score = 0.55
    elif category == 'smartphone':
        if price > 40000:
            price_score = 0.9
        elif price > 10000:
            price_score = 0.7
        else:
            price_score = 0.5
    elif category == 'watch':
        price_score = 0.8 if price > 1500 else 0.55
    elif category == 'earbuds':
        price_score = 0.8 if price > 800 else 0.55
    elif category == 'shoes':
        price_score = 0.8 if price > 700 else 0.55
    elif category == 'slides':
        price_score = 0.8 if price > 600 else 0.55
    else:
        price_score = 0.6

    # -------- IMAGE SCORE --------
    image_score = 0.6
    img_features = None
    if image_url:
        try:
            img_features = compute_image_features(image_url)
            if img_features.get('ok'):
                ent = img_features['entropy']
                if ent < 3.0:
                    image_score = 0.4
                elif ent < 4.0:
                    image_score = 0.65
                else:
                    image_score = 0.85
        except Exception as e:
            reasons.append(f"Image analysis error: {e}")

    # -------- COMBINE SCORES --------
    confidence = (
        text_score * 0.3 +
        price_score * 0.25 +
        image_score * 0.45
    )

    if not brand:
        confidence -= 0.05
        reasons.append('Brand missing or not detected.')

    confidence = max(0.0, min(1.0, confidence))

    # -------- THRESHOLD & SPECIAL CASES --------
    threshold = 0.5 if category == 'smartphone' else 0.45
    label = 'Real' if confidence >= threshold else 'Fake'

    # iPhone override: high-price Apple → Real
    if ('iphone' in title or 'apple' in brand) and price and price > 40000:
        label, confidence = 'Real', 0.9

    return {
        'label': label,
        'confidence': round(confidence, 2),
        'category': category,
        'reasons': reasons,
        'image_features': img_features
    }
