'use client'

import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Source {
  source: string
  page: number
  chunk_type: string
  similarity: number
  text?: string
}

interface QueryResponse {
  response: string
  sources: Source[]
  confidence: string
  retrieved_docs: any[]
}

export default function Home() {
  const [query, setQuery] = useState('')
  const [domain, setDomain] = useState('')
  const [response, setResponse] = useState<QueryResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [graphImage, setGraphImage] = useState('')
  const [graphType, setGraphType] = useState('wordcloud')
  const [loadingGraph, setLoadingGraph] = useState(false)

  const domains = [
    { id: '', name: 'All Domains' },
    { id: 'covid', name: 'COVID Clinical Research' },
    { id: 'diabetes', name: 'Diabetes' },
    { id: 'heart_attack', name: 'Heart Attack' },
    { id: 'knee_injuries', name: 'Knee Injuries' },
  ]

  const graphTypes = [
    { id: 'wordcloud', name: 'Word Cloud' },
    { id: 'term_frequency', name: 'Term Frequency' },
    { id: 'sources', name: 'Source Distribution' },
    { id: 'similarity', name: 'Similarity Scores' },
  ]

  const getDomainColor = (domainId: string) => {
    const colors: { [key: string]: string } = {
      covid: 'border-[#FF6B6B] bg-[#FF6B6B]/10',
      diabetes: 'border-[#FFD56B] bg-[#FFD56B]/10',
      heart_attack: 'border-[#FF6B6B] bg-[#FF6B6B]/10',
      knee_injuries: 'border-[#FFD56B] bg-[#FFD56B]/10',
    }
    return colors[domainId] || 'border-gray-600 bg-gray-800/50'
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!query.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError('')
    setResponse(null)
    setGraphImage('')

    try {
      const result = await axios.post(`${API_URL}/query`, {
        query: query.trim(),
        domain: domain || null,
      })

      setResponse(result.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred. Please make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = async (rating: 'up' | 'down') => {
    if (!response) return

    try {
      await axios.post(`${API_URL}/feedback`, {
        query,
        response: response.response,
        rating,
      })
      
      alert(`Thank you for your feedback! (${rating === 'up' ? '👍' : '👎'})`)
    } catch (err) {
      console.error('Error submitting feedback:', err)
    }
  }

  const handleGenerateGraph = async () => {
    if (!query.trim()) {
      setError('Please submit a query first')
      return
    }

    setLoadingGraph(true)
    setGraphImage('')

    try {
      const result = await axios.post(`${API_URL}/generate-graph`, {
        query: query.trim(),
        domain: domain || null,
        viz_type: graphType,
      })

      setGraphImage(result.data.image)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error generating graph')
    } finally {
      setLoadingGraph(false)
    }
  }

  return (
    <main className="min-h-screen bg-[#1a1a1a] p-4 md:p-8" style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      <div className="max-w-7xl mx-auto">
        {/* Retro Header */}
        <div className="text-center mb-8 md:mb-12 px-2">
          <div className="inline-block mb-4">
            <div className="border-4 border-[#FF6B6B] bg-[#FF6B6B]/5 px-6 py-2 transform -skew-x-3 shadow-[8px_8px_0px_0px_rgba(255,107,107,0.3)]">
              <span className="text-[#FFD56B] font-bold text-sm tracking-widest">EST. 2025</span>
            </div>
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-7xl font-bold mb-4 text-[#FF6B6B] tracking-tight" style={{ fontFamily: 'Georgia, serif', textShadow: '4px 4px 0px rgba(255,107,107,0.3)' }}>
            Clinical AI Assistant
          </h1>
          <div className="w-32 h-1 bg-[#FFD56B] mx-auto mb-4"></div>
          <p className="text-base sm:text-lg md:text-xl text-gray-300 max-w-3xl mx-auto px-4 leading-relaxed">
            Evidence-based medical research at your fingertips
          </p>
          <p className="text-sm text-gray-500 mt-2">COVID-19 • Diabetes • Heart Disease • Knee Injuries</p>
        </div>

        {/* Query Form */}
        <div className="bg-[#2a2a2a] border-4 border-[#FF6B6B] p-4 sm:p-6 md:p-10 mb-8 shadow-[12px_12px_0px_0px_rgba(255,107,107,0.3)] transform hover:shadow-[16px_16px_0px_0px_rgba(255,107,107,0.3)] transition-all duration-300">
          <form onSubmit={handleSubmit} className="space-y-4 md:space-y-6">
            {/* Domain Selection */}
            <div>
              <label className="block text-sm sm:text-base font-bold text-[#FFD56B] mb-3 md:mb-4 tracking-wide uppercase" style={{ fontFamily: 'Georgia, serif' }}>
                ◆ Select Clinical Domain
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 md:gap-3">
                {domains.map((d) => (
                  <button
                    key={d.id}
                    type="button"
                    onClick={() => setDomain(d.id)}
                    className={`py-2 sm:py-3 px-2 sm:px-4 border-2 text-xs sm:text-sm font-bold transition-all duration-200 truncate transform hover:translate-x-1 hover:translate-y-1 ${
                      domain === d.id
                        ? `${getDomainColor(d.id)} text-[#FFD56B] shadow-[4px_4px_0px_0px_rgba(255,213,107,0.5)]`
                        : 'bg-[#1a1a1a] text-gray-400 border-gray-600 hover:border-[#FFD56B] hover:text-[#FFD56B]'
                    }`}
                  >
                    {d.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Query Input */}
            <div>
              <label className="block text-sm sm:text-base font-bold text-[#FFD56B] mb-3 md:mb-4 tracking-wide uppercase" style={{ fontFamily: 'Georgia, serif' }}>
                ◆ Your Medical Question
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., What are the symptoms of COVID-19? How is diabetes managed with AI?"
                rows={4}
                className="w-full px-3 sm:px-5 py-3 sm:py-4 border-3 border-[#FF6B6B] bg-[#1a1a1a] focus:border-[#FFD56B] focus:shadow-[0_0_20px_rgba(255,213,107,0.3)] transition-all resize-none text-gray-200 placeholder-gray-600 text-sm sm:text-base font-mono"
                style={{ outline: 'none' }}
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#FF6B6B] text-[#1a1a1a] font-bold text-base sm:text-lg py-4 sm:py-5 px-6 sm:px-8 border-4 border-[#FF6B6B] hover:bg-[#FFD56B] hover:border-[#FFD56B] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:translate-x-2 hover:translate-y-2 shadow-[8px_8px_0px_0px_rgba(255,213,107,0.5)] hover:shadow-none uppercase tracking-wider"
              style={{ fontFamily: 'Georgia, serif' }}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 sm:h-6 sm:w-6 mr-2 sm:mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span className="text-sm sm:text-base">Analyzing Research...</span>
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <span className="text-xl sm:text-2xl mr-2">◆</span>
                  Submit Query
                </span>
              )}
            </button>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-[#2a2a2a] border-4 border-[#FF6B6B] p-4 md:p-5 mb-8 shadow-[8px_8px_0px_0px_rgba(255,107,107,0.5)]">
            <div className="flex items-start sm:items-center">
              <span className="text-2xl sm:text-3xl mr-2 sm:mr-3 flex-shrink-0 text-[#FF6B6B]">◆</span>
              <p className="text-[#FF6B6B] font-bold text-sm sm:text-base md:text-lg break-words">{error}</p>
            </div>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="space-y-6 md:space-y-8">
            {/* Main Response */}
            <div className="bg-[#2a2a2a] border-4 border-[#FFD56B] p-4 sm:p-6 md:p-10 shadow-[12px_12px_0px_0px_rgba(255,213,107,0.3)]">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 md:mb-6 gap-3">
                <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#FFD56B] flex items-center" style={{ fontFamily: 'Georgia, serif' }}>
                  <span className="text-2xl sm:text-3xl md:text-4xl mr-2 md:mr-3">◆</span>
                  AI Response
                </h2>
                <span className={`px-3 sm:px-4 md:px-5 py-1.5 sm:py-2 md:py-2.5 text-xs sm:text-sm font-bold border-3 self-start sm:self-auto uppercase tracking-wider ${
                  response.confidence === 'high' ? 'bg-[#FFD56B]/20 text-[#FFD56B] border-[#FFD56B]' :
                  response.confidence === 'medium' ? 'bg-[#FF6B6B]/20 text-[#FF6B6B] border-[#FF6B6B]' :
                  'bg-gray-700/50 text-gray-400 border-gray-600'
                }`}>
                  {response.confidence} CONFIDENCE
                </span>
              </div>

              <div className="bg-[#1a1a1a] border-2 border-[#FF6B6B]/30 p-4 sm:p-5 md:p-6 mb-4 md:mb-6">
                <p className="text-gray-200 text-sm sm:text-base md:text-lg leading-relaxed whitespace-pre-wrap break-words">
                  {response.response}
                </p>
              </div>

              {/* Feedback Buttons */}
              <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 pb-4 md:pb-6 mb-4 md:mb-6 border-b-2 border-[#FF6B6B]/30">
                <span className="text-sm sm:text-base font-bold text-gray-400 uppercase tracking-wide">Feedback:</span>
                <div className="flex gap-3">
                  <button
                    onClick={() => handleFeedback('up')}
                    className="flex items-center gap-2 px-4 sm:px-6 py-2 sm:py-3 bg-[#FFD56B] text-[#1a1a1a] border-2 border-[#FFD56B] hover:bg-transparent hover:text-[#FFD56B] transition-all transform hover:translate-x-1 hover:translate-y-1 shadow-[4px_4px_0px_0px_rgba(255,213,107,0.5)] hover:shadow-none font-bold text-sm"
                  >
                    <span className="text-lg sm:text-xl">↑</span>
                    <span>Helpful</span>
                  </button>
                  <button
                    onClick={() => handleFeedback('down')}
                    className="flex items-center gap-2 px-4 sm:px-6 py-2 sm:py-3 bg-[#FF6B6B] text-[#1a1a1a] border-2 border-[#FF6B6B] hover:bg-transparent hover:text-[#FF6B6B] transition-all transform hover:translate-x-1 hover:translate-y-1 shadow-[4px_4px_0px_0px_rgba(255,107,107,0.5)] hover:shadow-none font-bold text-sm"
                  >
                    <span className="text-lg sm:text-xl">↓</span>
                    <span>Not Helpful</span>
                  </button>
                </div>
              </div>

              {/* Evidence Section - Top 5 Documents */}
              {response.sources.length > 0 && (
                <div>
                  <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-[#FFD56B] mb-4 md:mb-5 flex items-center uppercase tracking-wide" style={{ fontFamily: 'Georgia, serif' }}>
                    <span className="text-2xl sm:text-3xl mr-2 md:mr-3">◆</span>
                    <span className="break-words">Evidence Sources (Top {Math.min(5, response.sources.length)})</span>
                  </h3>
                  <div className="space-y-4 md:space-y-5">
                    {response.sources.slice(0, 5).map((source, idx) => (
                      <div
                        key={idx}
                        className="bg-[#1a1a1a] border-3 border-[#FF6B6B]/50 p-4 sm:p-5 md:p-6 hover:border-[#FF6B6B] transition-all duration-300 transform hover:translate-x-2"
                      >
                        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-3 md:mb-4 gap-3">
                          <div className="flex items-start gap-2 md:gap-3 flex-1 min-w-0">
                            <span className="bg-[#FF6B6B] text-[#1a1a1a] text-xs sm:text-sm font-extrabold px-2 sm:px-3 py-1 sm:py-1.5 flex-shrink-0 border-2 border-[#FF6B6B]">
                              #{idx + 1}
                            </span>
                            <div className="flex-1 min-w-0">
                              <h4 className="font-bold text-gray-200 text-sm sm:text-base mb-1.5 leading-snug break-words">
                                {source.source}
                              </h4>
                              <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500">
                                <span className="bg-[#2a2a2a] border border-[#FFD56B]/30 px-2 sm:px-2.5 py-0.5 sm:py-1 font-semibold whitespace-nowrap">
                                  ◆ Page {source.page}
                                </span>
                                <span className="bg-[#2a2a2a] border border-[#FFD56B]/30 px-2 sm:px-2.5 py-0.5 sm:py-1 font-semibold truncate max-w-[150px]">
                                  {source.chunk_type}
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className="self-start sm:ml-3">
                            <span className="bg-[#FFD56B] text-[#1a1a1a] text-xs font-bold px-2 sm:px-3 py-1 sm:py-1.5 border-2 border-[#FFD56B] whitespace-nowrap inline-block">
                              {(source.similarity * 100).toFixed(1)}% MATCH
                            </span>
                          </div>
                        </div>
                        
                        {source.text && (
                          <div className="mt-3 md:mt-4 pl-3 sm:pl-4 md:pl-5 border-l-2 border-[#FFD56B]">
                            <p className="text-xs sm:text-sm font-bold text-[#FFD56B] mb-2 uppercase tracking-wide">
                              Excerpt:
                            </p>
                            <div className="bg-[#2a2a2a] border border-[#FF6B6B]/30 p-3 md:p-4">
                              <p className="text-gray-300 text-xs sm:text-sm leading-relaxed break-words font-mono">
                                "{source.text}"
                              </p>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* All Sources Summary */}
                  {response.sources.length > 5 && (
                    <div className="mt-4 md:mt-6 p-3 md:p-4 bg-[#2a2a2a] border-2 border-[#FFD56B]/30">
                      <p className="text-xs sm:text-sm text-gray-400 font-bold text-center uppercase tracking-wide">
                        + {response.sources.length - 5} additional sources referenced
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Graph Generation */}
            <div className="bg-[#2a2a2a] border-4 border-[#FF6B6B] p-4 sm:p-6 md:p-10 shadow-[12px_12px_0px_0px_rgba(255,107,107,0.3)]">
              <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-[#FF6B6B] mb-4 md:mb-6 flex items-center uppercase tracking-wide" style={{ fontFamily: 'Georgia, serif' }}>
                <span className="text-2xl sm:text-3xl md:text-4xl mr-2 md:mr-3">◆</span>
                Data Visualizations
              </h2>
              
              <div className="flex flex-col sm:flex-row gap-3 md:gap-4 mb-4 md:mb-6">
                <select
                  value={graphType}
                  onChange={(e) => setGraphType(e.target.value)}
                  className="flex-1 px-3 sm:px-4 md:px-5 py-3 md:py-4 border-3 border-[#FFD56B] bg-[#1a1a1a] text-gray-200 focus:border-[#FF6B6B] focus:shadow-[0_0_20px_rgba(255,107,107,0.3)] text-sm sm:text-base font-bold"
                  style={{ outline: 'none' }}
                >
                  {graphTypes.map((type) => (
                    <option key={type.id} value={type.id} className="bg-[#1a1a1a]">
                      {type.name}
                    </option>
                  ))}
                </select>

                <button
                  onClick={handleGenerateGraph}
                  disabled={loadingGraph}
                  className="px-6 sm:px-8 md:px-10 py-3 md:py-4 bg-[#FFD56B] text-[#1a1a1a] border-4 border-[#FFD56B] hover:bg-[#FF6B6B] hover:border-[#FF6B6B] disabled:opacity-50 transition-all duration-300 transform hover:translate-x-2 hover:translate-y-2 shadow-[8px_8px_0px_0px_rgba(255,107,107,0.5)] hover:shadow-none font-bold text-sm sm:text-base md:text-lg whitespace-nowrap uppercase tracking-wider"
                  style={{ fontFamily: 'Georgia, serif' }}
                >
                  {loadingGraph ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-4 w-4 sm:h-5 sm:w-5 mr-2" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Generating...
                    </span>
                  ) : (
                    '◆ Generate Graph'
                  )}
                </button>
              </div>

              {graphImage && (
                <div className="border-4 border-[#FFD56B] overflow-hidden shadow-[8px_8px_0px_0px_rgba(255,213,107,0.3)]">
                  <img
                    src={graphImage}
                    alt="Generated visualization"
                    className="w-full h-auto"
                  />
                </div>
              )}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 md:mt-16 px-4">
          <div className="inline-block border-t-2 border-b-2 border-[#FF6B6B] py-4 px-8">
            <p className="text-xs sm:text-sm text-gray-500 font-bold uppercase tracking-widest" style={{ fontFamily: 'Georgia, serif' }}>
              ◆ Clinical AI Assistant ◆
            </p>
            <p className="text-xs text-gray-600 mt-1">
              Powered by RAG • FAISS • OpenRouter
            </p>
          </div>
          <div className="mt-6 flex justify-center gap-4">
            <div className="w-16 h-1 bg-[#FF6B6B]"></div>
            <div className="w-16 h-1 bg-[#FFD56B]"></div>
            <div className="w-16 h-1 bg-[#FF6B6B]"></div>
          </div>
        </div>
      </div>
    </main>
  )
}
