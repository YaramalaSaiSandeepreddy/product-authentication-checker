
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_product_details
from detector import detect_fake_product

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return {'status':'ok'}


@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({'error':'No URL provided'}), 400
    try:
        details = scrape_product_details(url)
        verdict = detect_fake_product(details)
        return jsonify({'details': details, 'verdict': verdict})
    except Exception as e:
        return jsonify({'error':str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
