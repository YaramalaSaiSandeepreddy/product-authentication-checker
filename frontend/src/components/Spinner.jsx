import React from 'react'

export default function Spinner(){ 
  return (
    <div className="flex items-center gap-2">
      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" opacity="0.2"></circle>
        <path d="M4 12a8 8 0 018-8" stroke="currentColor" strokeWidth="4" strokeLinecap="round"></path>
      </svg>
      <span className="text-sm">Scanning...</span>
    </div>
  )
}