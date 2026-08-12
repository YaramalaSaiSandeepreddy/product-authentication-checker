import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5000'

export async function scrapeURL(url) {
  const res = await axios.post(`${API_BASE}/api/scrape`, { url })
  return res.data
}

export async function predict(details) {
  const res = await axios.post(`${API_BASE}/api/predict`, { details })
  return res.data
}
