import React from 'react'
import { motion } from 'framer-motion'

export default function Header(){
  return (
    <header className="py-8 bg-white shadow">
      <div className="max-w-5xl mx-auto px-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-brand">Fake Product Detector</h1>
          <p className="text-sm text-gray-500">AI-assisted checks for product authenticity — image + text ready</p>
        </div>
        <motion.div animate={{ rotate: [0, 360] }} transition={{ repeat: Infinity, duration: 10 }} className="w-14 h-14 rounded-xl bg-gradient-to-br from-brand to-accent flex items-center justify-center text-white font-bold">
          AI
        </motion.div>
      </div>
    </header>
  )
}
