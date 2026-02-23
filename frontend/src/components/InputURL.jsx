
import React, { useState } from 'react'
import * as api from '../api'
import Spinner from './Spinner'

export default function InputURL({onResult, setLoading, loading}){
  const [url, setUrl] = useState('')
  const [err, setErr] = useState(null)

  async function handleCheck(){
    setErr(null)
    if(!url) { setErr('Please paste a product URL'); return }
    try{
      setLoading(true)
      const resp = await fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({url})
      })
      const data = await resp.json()
      onResult({details: data.details, verdict: data.verdict})
    }catch(e){
      setErr('Server error: '+e.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="p-6 bg-white rounded-2xl shadow-md">
      <label className="block font-semibold mb-2">Product URL</label>
      <div className="flex gap-3">
        <input value={url} onChange={e=>setUrl(e.target.value)} className="flex-1 px-4 py-3 border rounded-xl" placeholder="https://www.flipkart.com/..." />
        <button onClick={handleCheck} className="btn-dynamic">Check</button>
      </div>
      <div className="mt-3">{ loading ? <Spinner /> : null }</div>
      {err && <div className="mt-3 text-red-600">{err}</div>}
    </div>
  )
}
