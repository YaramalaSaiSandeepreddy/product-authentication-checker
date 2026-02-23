import requests, json, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


# --- Safe text helper ---
def _safe_text(el):
    return el.get_text(strip=True) if el else None


# --- Better price parser ---
def _parse_price(text):
    if not text:
        return None
    # Remove currency symbols and spaces
    t = re.sub(r'[^\d.,]', '', text)
    t = t.replace(',', '')
    try:
        val = float(t)
        # avoid wrong small parses like 1.0 from ₹1,999
        if val < 100:
            return None
        return val
    except Exception:
        return None


# --- Pick first valid image url ---
def _extract_image(soup, base=None):
    # og:image
    m = soup.find('meta', property='og:image')
    if m and m.get('content'):
        return urljoin(base, m['content'])
    # data-a-dynamic-image (Amazon)
    dyn = soup.find('img', attrs={'data-a-dynamic-image': True})
    if dyn:
        try:
            j = json.loads(dyn['data-a-dynamic-image'])
            if isinstance(j, dict):
                return urljoin(base, list(j.keys())[0])
        except Exception:
            pass
    # fallback
    img = soup.find('img')
    if img and img.get('src'):
        return urljoin(base, img['src'])
    return None


def _scrape_bs(html, base=None):
    soup = BeautifulSoup(html, 'html.parser')

    # --- Title ---
    title = _safe_text(soup.find('h1')) or _safe_text(soup.find('span', id='productTitle'))

    # --- Price ---
    price_el = soup.select_one('[class*="price"], [id*="price"], meta[property="product:price:amount"]')
    price = None
    if price_el:
        price = price_el.get('content') if price_el.name == 'meta' else price_el.get_text(strip=True)

    # --- Description ---
    desc = soup.find('meta', {'name': 'description'}) or soup.find('div', id='productDescription')
    description = desc.get('content') if getattr(desc, 'get', None) else _safe_text(desc)

    # --- Image ---
    image = _extract_image(soup, base)

    # --- Brand detection ---
    brand = None
    for s in soup.find_all('script', type='application/ld+json'):
        try:
            j = json.loads(s.string or '{}')
            if isinstance(j, dict):
                b = j.get('brand') or j.get('manufacturer')
                if isinstance(b, dict):
                    brand = b.get('name') or brand
                elif isinstance(b, str):
                    brand = b
        except Exception:
            pass

    # --- Fallback brand from title ---
    if not brand and title:
        if 'apple' in title.lower():
            brand = 'Apple'
        elif 'samsung' in title.lower():
            brand = 'Samsung'

    # --- Flipkart / Amazon category hint ---
    # Add category keyword to help detector
    if base:
        base_l = base.lower()
        if '/mob' in base_l and title and 'phone' not in title.lower():
            title = f"{title} phone"
        elif '/shoe' in base_l and title and 'shoe' not in title.lower():
            title = f"{title} shoes"
        elif '/watch' in base_l and title and 'watch' not in title.lower():
            title = f"{title} watch"
        elif '/slipper' in base_l and 'slide' not in title.lower():
            title = f"{title} slides"

    return {
        'title': title,
        'price': _parse_price(price),
        'description': description,
        'image_url': image,
        'brand': brand
    }


# --- Dynamic (Playwright) Scraper ---
def _scrape_dynamic(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent=HEADERS['User-Agent'])
            page.goto(url, timeout=25000, wait_until='domcontentloaded')
            html = page.content()
            browser.close()
            return _scrape_bs(html, base=url)
    except PlaywrightTimeoutError:
        return {'title': None, 'price': None, 'description': None, 'image_url': None, 'brand': None}


# --- Main function ---
def scrape_product_details(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = _scrape_bs(r.text, base=url)
        # fallback to dynamic if important fields missing
        if not data.get('title') or not data.get('image_url'):
            data = _scrape_dynamic(url)
    except Exception:
        data = _scrape_dynamic(url)

    data['url'] = url
    return data
