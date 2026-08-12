import React from 'react'

export default function ResultBadge({result}){
  if(!result) return null
  const { label, confidence, reason } = result
  const color = label === 'Real' ? 'bg-green-100 text-green-800' : label === 'Fake' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
  return (
    <div className={`inline-flex items-center gap-3 px-4 py-2 rounded-full ${color}`}>
      <strong>{label}</strong>
      <span className="text-xs opacity-80">{confidence*100}%</span>
      <span className="ml-2 text-sm">{reason}</span>
    </div>
  )
}
