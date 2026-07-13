"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Activity, Search, ArrowRight, Database } from "lucide-react";

export default function Home() {
  const [ticker, setTicker] = useState("");
  const [provider, setProvider] = useState("openai");
  const [model, setModel] = useState("gpt-4o");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState("");
  const [error, setError] = useState("");

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticker) return;

    setLoading(true);
    setError("");
    setAnalysis("");

    try {
      // In production, you would point this to your deployed FastAPI backend URL
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
      const res = await fetch(`${backendUrl}/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ticker: ticker.toUpperCase(),
          provider: provider,
          model: model,
        }),
      });

      const data = await res.json();
      
      if (!res.ok || data.error) {
        throw new Error(data.error || "Failed to fetch analysis");
      }

      setAnalysis(data.analysis);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-white font-sans overflow-hidden">
      
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 px-8 py-6 flex justify-between items-center bg-[#0f0f0f]/80 backdrop-blur-md">
        <div className="text-xl font-bold tracking-tight flex items-center gap-2">
          <span className="text-[#ff5e00]"><Activity size={24} /></span>
          QuantBlox
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
          <a href="#" className="hover:text-white transition-colors">Home</a>
          <a href="#" className="hover:text-white transition-colors">Agents</a>
          <a href="#" className="hover:text-white transition-colors">Methodology</a>
        </div>
        <div>
          <button className="bg-white text-black px-6 py-2.5 rounded-full text-sm font-bold flex items-center gap-2 hover:bg-gray-200 transition-colors">
            Get in touch <ArrowRight size={16} className="text-[#ff5e00]" />
          </button>
        </div>
      </nav>

      <main className="relative pt-32 pb-20">
        
        {/* Hero Section */}
        <section className="relative px-8 max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between mt-12 mb-32">
          {/* Giant Orange Gradient Blob */}
          <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-[#ff5e00] rounded-full mix-blend-screen filter blur-[150px] opacity-40 -translate-x-1/2 -translate-y-1/4 pointer-events-none"></div>

          <div className="relative z-10 w-full md:w-1/2">
            <p className="text-lg font-medium text-gray-300 mb-4">Hello, I'm your</p>
            <h1 className="text-6xl md:text-8xl font-black leading-[1.1] tracking-tight mb-8">
              AI Financial<br />Director
            </h1>
            <p className="text-gray-400 text-lg mb-12 max-w-md">
              From raw ticker data to complex quantitative modeling, I build deep diagnostic financial reports that connect and convert data into insight.
            </p>
            
            <form onSubmit={handleAnalyze} className="flex flex-col gap-4 w-full max-w-md">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                <input 
                  type="text" 
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="Enter Ticker (e.g. AAPL)" 
                  className="w-full bg-[#1a1a1a] border border-gray-800 rounded-full py-4 pl-12 pr-6 text-white placeholder-gray-500 focus:outline-none focus:border-[#ff5e00] transition-colors uppercase font-medium tracking-wide"
                  required
                />
              </div>
              
              <div className="flex gap-4">
                <select 
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="flex-1 bg-[#1a1a1a] border border-gray-800 rounded-full py-3 px-4 text-gray-300 focus:outline-none focus:border-[#ff5e00] appearance-none"
                >
                  <option value="openai">OpenAI</option>
                  <option value="groq">Groq</option>
                  <option value="gemini">Gemini</option>
                  <option value="ollama">Ollama</option>
                </select>
                <button 
                  type="submit" 
                  disabled={loading}
                  className="bg-[#ff5e00] text-white px-8 py-3 rounded-full font-bold flex items-center justify-center gap-2 hover:bg-[#e05300] transition-colors disabled:opacity-50"
                >
                  {loading ? "Analyzing..." : "Analyze"} <ArrowRight size={18} />
                </button>
              </div>
            </form>
          </div>
        </section>

        {/* Services / Analysis Section */}
        <section className="px-8 max-w-7xl mx-auto relative z-10">
          <div className="mb-12 flex flex-col md:flex-row justify-between items-end">
            <div>
              <p className="text-[#ff5e00] font-bold mb-4 tracking-wide text-sm uppercase">Capabilities</p>
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight">What I Can Help<br />You With</h2>
            </div>
            <p className="text-gray-400 max-w-sm text-sm">
              From time series forecasting to SEC document extraction, I offer tailored quantitative analysis to help your portfolio grow with clarity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#161616] p-8 rounded-2xl border-t-2 border-t-[#ff5e00] hover:-translate-y-1 transition-transform duration-300">
              <p className="text-[#ff5e00] text-xs font-bold uppercase tracking-wider mb-2">Trend Decomposition</p>
              <h3 className="text-2xl font-bold mb-4">Time Series<br />Forecasting</h3>
              <p className="text-gray-400 text-sm">Prophet-based modeling, separating weekly and yearly seasonality from random market noise.</p>
            </div>
            <div className="bg-[#161616] p-8 rounded-2xl border-t-2 border-t-gray-700 hover:-translate-y-1 hover:border-t-[#ff5e00] transition-all duration-300">
              <p className="text-[#ff5e00] text-xs font-bold uppercase tracking-wider mb-2">Common-Size Statements</p>
              <h3 className="text-2xl font-bold mb-4">Vertical<br />Analysis</h3>
              <p className="text-gray-400 text-sm">Converting raw financial metrics into percentages to expose hidden operational inefficiencies.</p>
            </div>
            <div className="bg-[#161616] p-8 rounded-2xl border-t-2 border-t-gray-700 hover:-translate-y-1 hover:border-t-[#ff5e00] transition-all duration-300">
              <p className="text-[#ff5e00] text-xs font-bold uppercase tracking-wider mb-2">Automated Research</p>
              <h3 className="text-2xl font-bold mb-4">MD&A Document<br />Extraction</h3>
              <p className="text-gray-400 text-sm">Scraping SEC 10-K filings to causally link quantitative metric changes to management's qualitative statements.</p>
            </div>
          </div>
        </section>

        {/* Results Area */}
        {(analysis || loading || error) && (
          <section className="px-8 max-w-7xl mx-auto mt-24 relative z-10">
            <div className="bg-[#161616] rounded-3xl p-10 border border-gray-800">
              
              {loading && (
                <div className="flex flex-col items-center justify-center py-20">
                  <div className="w-12 h-12 border-4 border-gray-800 border-t-[#ff5e00] rounded-full animate-spin mb-6"></div>
                  <h3 className="text-2xl font-bold mb-2 text-white">Synthesizing Report...</h3>
                  <p className="text-gray-400">Executing ReAct agents, crunching Prophet models, and extracting MD&A context.</p>
                </div>
              )}

              {error && (
                <div className="py-10 text-center">
                  <p className="text-red-500 font-bold mb-2">Error generating report</p>
                  <p className="text-gray-400">{error}</p>
                </div>
              )}

              {analysis && !loading && (
                <div className="prose prose-invert prose-lg max-w-none prose-headings:text-white prose-a:text-[#ff5e00] prose-strong:text-white prose-code:bg-gray-800 prose-code:text-[#ff5e00] prose-code:px-1 prose-code:rounded">
                  <ReactMarkdown>{analysis}</ReactMarkdown>
                </div>
              )}
            </div>
          </section>
        )}

      </main>
    </div>
  );
}
