# Product Authenticity Checker — Updated

## What's included
- Backend (Flask) that scrapes product pages and applies heuristics to detect possible fake products (text + image + price checks).
- Frontend (React + Vite + Tailwind) with improved UI, animations, and components.
- Dockerfile + docker-compose for easy local deployment.

## Quick run (local)
### Backend
```
cd backend
python -m venv venv
source venv/bin/activate     # use `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py
```

### Frontend
```
cd frontend
npm install
npm run dev
```

### Docker (one container image)
```
docker compose up --build
# then open http://localhost:5000 or the frontend dev server at http://localhost:5173
```

## Notes / Next improvements
- Add ML image classifier or logo-matching to strengthen image checks.
- Add more robust price heuristics per category/brand.
- Add caching for scraped pages and rate-limiting.
- Playwright is listed in requirements; if scraping dynamic pages fails, ensure Playwright is installed and browsers are installed (`playwright install`).