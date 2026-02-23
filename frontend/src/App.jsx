
import React, { useState } from 'react'
import InputURL from './components/InputURL'
import ProductCard from './components/ProductCard'
import './styles.css'

export default function App(){
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-5xl mx-auto">
        <header className="hero mb-6 flex items-center justify-between"><div className="header-icon mr-4"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" className="w-6 h-6"><path d="M3 12h18" strokeLinecap="round" strokeLinejoin="round"></path><path d="M12 3v18" strokeLinecap="round" strokeLinejoin="round"></path></svg></div>
          <div>
            <h1 className="text-3xl font-extrabold">Product Authenticity Checker</h1>
            <p className="mt-2 text-slate-600">Paste a product URL from Amazon / Flipkart / Myntra / Ajio and get a quick real-or-fake assessment.</p>
          </div>
          <div>
            <button className="btn-dynamic">
              Try Demo
            </button>
          </div>
        </header>

        <InputURL onResult={(r)=>{ setResult(r) }} setLoading={setLoading} loading={loading} />

        <div className="mt-8">
          {loading && <div className="p-6 bg-white rounded-2xl shadow shimmer">Scanning product — running checks...</div>}
          {result && <ProductCard data={result} />}
        </div>
      </div>
    </div>
  )
}
