
import React from 'react'

export default function ProductCard({data}){
  if(!data) return null
  const {details, verdict} = data
  const label = verdict.label || 'Unknown'
  return (
    <div className="product-card grid result-card fade-in grid-cols-1 md:grid-cols-3 gap-4 items-center">
      <div className="product-image md:col-span-1">
        <img src={details.image_url || ''} alt={details.title} className="w-full h-64 object-cover rounded-xl" />
      </div>
      <div className="md:col-span-2">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold">{details.title}</h2>
            <p className="text-sm text-slate-500 mt-1">{details.brand || ''}</p>
            <p className="text-lg mt-3 font-semibold">{details.price || ''}</p>
          </div>
          <div className="text-right">
            <div className={label === 'Real' ? 'badge-real' : label === 'Fake' ? 'badge-fake' : 'px-3 py-1 rounded-full bg-amber-400 text-sm font-semibold'}>
              {label}
            </div>
            <div className="mt-2 text-sm text-slate-600">Confidence: {verdict.confidence}</div>
          </div>
        </div>

        <div className="mt-4">
          <h3 className="font-semibold">Reasons / Notes</h3>
          <ul className="mt-2 list-disc ml-5 text-slate-700">
            {verdict.reasons && verdict.reasons.length>0 ? verdict.reasons.map((r,i)=><li key={i}>{r}</li>) : <li>No specific issues detected.</li>}
          </ul>
        </div>

        <div className="mt-4">
          <h4 className="font-semibold">Image analysis</h4>
          <div className="text-sm text-slate-600 mt-2">{data.verdict.image_features ? (<div>Size: {data.verdict.image_features.size_kb}KB — {data.verdict.image_features.width}x{data.verdict.image_features.height} — Entropy: {data.verdict.image_features.entropy}</div>) : <div>No image data</div>}</div>
        </div>

        <div className="mt-4 flex gap-3">
          <a className="btn-dynamic" href={details.url} target="_blank" rel="noreferrer">Open product</a>
          <button className="px-4 py-2 rounded-lg border hover:shadow">View more checks</button>
        </div>
      </div>
    </div>
  )
}
