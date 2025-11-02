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
      covid: 'from-purple-500 to-purple-700',
      diabetes: 'from-blue-500 to-blue-700',
      heart_attack: 'from-red-500 to-red-700',
      knee_injuries: 'from-green-500 to-green-700',
    }
    return colors[domainId] || 'from-gray-500 to-gray-700'
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
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-block mb-4">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold shadow-lg">
              Powered by Landing AI • RAG Pipeline • FAISS Vector Search
            </div>
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Clinical AI Assistant
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Ask evidence-based questions about COVID-19, Diabetes, Heart Disease, and Knee Injuries
          </p>
          <p className="text-sm text-gray-500 mt-3 font-medium">
            🔒 100% Grounded in Local Research Papers • No Internet Data • Fully Cited Responses
          </p>
        </div>

        {/* Query Form */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10 mb-8 border-2 border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Domain Selection */}
            <div>
              <label className="block text-base font-bold text-gray-800 mb-3">
                🏥 Select Clinical Domain
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {domains.map((d) => (
                  <button
                    key={d.id}
                    type="button"
                    onClick={() => setDomain(d.id)}
                    className={`py-3 px-4 rounded-xl font-semibold transition-all duration-200 border-2 ${
                      domain === d.id
                        ? `bg-gradient-to-r ${getDomainColor(d.id)} text-white border-transparent shadow-xl transform scale-105`
                        : 'bg-gray-50 text-gray-700 border-gray-200 hover:border-gray-400 hover:bg-gray-100'
                    }`}
                  >
                    {d.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Query Input */}
            <div>
              <label className="block text-base font-bold text-gray-800 mb-3">
                💬 Your Question
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., What are the symptoms of COVID-19? How is diabetes managed with AI? What ML models predict heart attacks?"
                rows={5}
                className="w-full px-5 py-4 border-2 border-gray-300 rounded-2xl focus:ring-4 focus:ring-blue-200 focus:border-blue-500 transition-all resize-none text-gray-800 placeholder-gray-400 text-base"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white font-bold text-lg py-5 px-8 rounded-2xl hover:shadow-2xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98]"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-6 w-6 mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing Research Papers...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <span className="text-2xl mr-2">🔍</span>
                  Submit Query
                </span>
              )}
            </button>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-5 mb-8 shadow-lg">
            <div className="flex items-center">
              <span className="text-3xl mr-3">⚠️</span>
              <p className="text-red-800 font-semibold text-lg">{error}</p>
            </div>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="space-y-8">
            {/* Main Response */}
            <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10 border-2 border-gray-100">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-extrabold text-gray-900 flex items-center">
                  <span className="text-4xl mr-3">💡</span>
                  AI Response
                </h2>
                <span className={`px-5 py-2.5 rounded-full text-sm font-bold border-2 ${
                  response.confidence === 'high' ? 'bg-green-100 text-green-800 border-green-400' :
                  response.confidence === 'medium' ? 'bg-yellow-100 text-yellow-800 border-yellow-400' :
                  'bg-red-100 text-red-800 border-red-400'
                }`}>
                  {response.confidence.toUpperCase()} CONFIDENCE
                </span>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-6 mb-6 border-2 border-blue-100">
                <p className="text-gray-900 text-lg leading-relaxed whitespace-pre-wrap font-medium">
                  {response.response}
                </p>
              </div>

              {/* Feedback Buttons */}
              <div className="flex items-center gap-4 pb-6 mb-6 border-b-2 border-gray-200">
                <span className="text-base font-bold text-gray-700">Was this helpful?</span>
                <button
                  onClick={() => handleFeedback('up')}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-xl transition-all transform hover:scale-105 shadow-lg font-semibold"
                >
                  <span className="text-xl">👍</span>
                  <span>Yes</span>
                </button>
                <button
                  onClick={() => handleFeedback('down')}
                  className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white rounded-xl transition-all transform hover:scale-105 shadow-lg font-semibold"
                >
                  <span className="text-xl">👎</span>
                  <span>No</span>
                </button>
              </div>

              {/* Evidence Section - Top 5 Documents */}
              {response.sources.length > 0 && (
                <div>
                  <h3 className="text-2xl font-extrabold text-gray-900 mb-5 flex items-center">
                    <span className="text-3xl mr-3">📚</span>
                    Evidence from Research Papers (Top {Math.min(5, response.sources.length)})
                  </h3>
                  <div className="space-y-5">
                    {response.sources.slice(0, 5).map((source, idx) => (
                      <div
                        key={idx}
                        className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border-l-4 border-blue-600 hover:shadow-xl transition-all duration-300"
                      >
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-start gap-3 flex-1">
                            <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-extrabold px-3 py-1.5 rounded-full shadow-md">
                              #{idx + 1}
                            </span>
                            <div className="flex-1">
                              <h4 className="font-bold text-gray-900 text-base mb-1.5 leading-snug">
                                {source.source}
                              </h4>
                              <div className="flex items-center gap-3 text-xs text-gray-600">
                                <span className="bg-white px-2.5 py-1 rounded-full font-semibold">
                                  📄 Page {source.page}
                                </span>
                                <span className="bg-white px-2.5 py-1 rounded-full font-semibold">
                                  {source.chunk_type}
                                </span>
                              </div>
                            </div>
                          </div>
                          <div className="ml-3">
                            <span className="bg-gradient-to-r from-green-500 to-emerald-500 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-md whitespace-nowrap">
                              {(source.similarity * 100).toFixed(1)}% match
                            </span>
                          </div>
                        </div>
                        
                        {source.text && (
                          <div className="mt-4 pl-5 border-l-3 border-blue-400">
                            <p className="text-sm font-semibold text-blue-900 mb-2">
                              📖 Excerpt from Document:
                            </p>
                            <div className="bg-white rounded-xl p-4 shadow-inner">
                              <p className="text-gray-800 text-sm leading-relaxed italic">
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
                    <div className="mt-6 p-4 bg-gray-50 rounded-xl border-2 border-gray-200">
                      <p className="text-sm text-gray-600 font-medium text-center">
                        + {response.sources.length - 5} additional sources used in analysis
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Graph Generation */}
            <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10 border-2 border-gray-100">
              <h2 className="text-3xl font-extrabold text-gray-900 mb-6 flex items-center">
                <span className="text-4xl mr-3">📊</span>
                Data Visualizations
              </h2>
              
              <div className="flex flex-col md:flex-row gap-4 mb-6">
                <select
                  value={graphType}
                  onChange={(e) => setGraphType(e.target.value)}
                  className="flex-1 px-5 py-4 border-2 border-gray-300 rounded-xl focus:ring-4 focus:ring-purple-200 focus:border-purple-500 text-base font-semibold"
                >
                  {graphTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>

                <button
                  onClick={handleGenerateGraph}
                  disabled={loadingGraph}
                  className="px-10 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-lg rounded-xl hover:shadow-2xl disabled:opacity-50 transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98]"
                >
                  {loadingGraph ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Generating...
                    </span>
                  ) : (
                    '📈 Generate Graph'
                  )}
                </button>
              </div>

              {graphImage && (
                <div className="border-4 border-gray-200 rounded-2xl overflow-hidden shadow-xl">
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
        <div className="text-center mt-12 space-y-2">
          <div className="inline-flex items-center gap-3 bg-white px-6 py-3 rounded-full shadow-lg border-2 border-gray-200">
            <span className="text-2xl">🔒</span>
            <p className="text-sm font-bold text-gray-700">
              100% Private • All Data Processed Locally • No Internet Access
            </p>
          </div>
          <p className="text-sm text-gray-500 font-medium">
            Built with Landing AI ADE • FAISS Vector DB • OpenRouter LLM • Next.js 14
          </p>
        </div>
      </div>
    </main>
  )
}
