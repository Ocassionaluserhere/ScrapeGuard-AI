import React, { useState } from 'react';
import { 
  Activity, ShieldCheck, AlertTriangle, RefreshCw, Cpu, 
  Database, Server, CheckCircle2, XCircle, Play
} from 'lucide-react';

export default function ScrapeGuardDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isScraping, setIsScraping] = useState(false);
  const [demoState, setDemoState] = useState('IDLE');
  const [healthScore, setHealthScore] = useState(94);
  
  const handleRunDemo = () => {
    setIsScraping(true);
    setDemoState('DEGRADED');
    setTimeout(() => {
      setIsScraping(false);
      setHealthScore(42);
    }, 1500);
  };

  const handleTriggerHealing = () => {
    setDemoState('RECOVERING');
    setTimeout(() => {
      setDemoState('RECOVERED');
      setHealthScore(98);
    }, 2500);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col">
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="bg-indigo-600 p-2 rounded-lg text-white shadow-lg shadow-indigo-500/30">
            <ShieldCheck size={24} />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-none tracking-tight text-white">ScrapeGuard AI</h1>
            <p className="text-xs text-slate-400 mt-1">Autonomous Self-Healing Data Extraction</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <span className="flex items-center text-xs font-medium px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></span>
            System Operational
          </span>
          <button 
            onClick={handleRunDemo}
            disabled={isScraping}
            className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition shadow-sm"
          >
            {isScraping ? <RefreshCw size={16} className="animate-spin" /> : <Play size={16} />}
            <span>Run Degradation Demo</span>
          </button>
        </div>
      </header>

      <div className="flex flex-1">
        <aside className="w-64 border-r border-slate-800 bg-slate-900/30 p-4 flex flex-col justify-between">
          <nav className="space-y-1">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'scrapers', label: 'Scrapers', icon: Server },
              { id: 'records', label: 'Extracted Records', icon: Database },
              { id: 'healing', label: 'Healing Center', icon: Cpu, badge: demoState === 'DEGRADED' ? '1 Incident' : null },
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                    activeTab === tab.id 
                      ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' 
                      : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon size={18} />
                    <span>{tab.label}</span>
                  </div>
                  {tab.badge && (
                    <span className="bg-rose-500/20 text-rose-400 text-xs px-2 py-0.5 rounded-full border border-rose-500/30 font-semibold">
                      {tab.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
            <p className="text-xs text-slate-400">Bright Data API Status</p>
            <p className="text-sm font-semibold text-emerald-400 mt-0.5">Connected (Studio)</p>
          </div>
        </aside>

        <main className="flex-1 p-8 overflow-y-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
              <span className="text-xs font-medium text-slate-400">Scraper Health</span>
              <div className="flex items-baseline space-x-2 mt-2">
                <span className={`text-3xl font-extrabold ${healthScore > 80 ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {healthScore}%
                </span>
                <span className="text-xs text-slate-500">weighted avg</span>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
              <span className="text-xs font-medium text-slate-400">Total Extracted Records</span>
              <div className="flex items-baseline space-x-2 mt-2">
                <span className="text-3xl font-extrabold text-white">1,284</span>
                <span className="text-xs text-emerald-400">+12% this week</span>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
              <span className="text-xs font-medium text-slate-400">Schema Pass Rate</span>
              <div className="flex items-baseline space-x-2 mt-2">
                <span className="text-3xl font-extrabold text-indigo-400">
                  {demoState === 'DEGRADED' ? '18.2%' : '98.5%'}
                </span>
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
              <span className="text-xs font-medium text-slate-400">Autonomous Healing Events</span>
              <div className="flex items-baseline space-x-2 mt-2">
                <span className="text-3xl font-extrabold text-amber-400">
                  {demoState === 'RECOVERED' ? 4 : 3}
                </span>
                <span className="text-xs text-slate-500">100% resolved</span>
              </div>
            </div>
          </div>

          {demoState === 'DEGRADED' && (
            <div className="mb-8 bg-rose-500/10 border border-rose-500/30 rounded-xl p-6 flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-rose-500/20 text-rose-400 rounded-xl">
                  <AlertTriangle size={24} />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-rose-200">Extraction Degradation Detected</h3>
                  <p className="text-sm text-slate-400 mt-0.5">
                    Field <code className="bg-rose-950 px-1.5 py-0.5 rounded text-rose-300">price</code> completeness dropped from 98% to 15%. Target DOM structure changed.
                  </p>
                </div>
              </div>
              <button 
                onClick={handleTriggerHealing}
                className="bg-rose-600 hover:bg-rose-500 text-white px-5 py-2.5 rounded-lg font-medium text-sm transition shadow-lg shadow-rose-600/20"
              >
                Trigger Self-Healing
              </button>
            </div>
          )}

          {(demoState === 'RECOVERING' || demoState === 'RECOVERED') && (
            <div className="mb-8 bg-slate-900 border border-slate-800 rounded-xl p-6">
              <h3 className="text-sm font-semibold text-slate-300 mb-6 flex items-center space-x-2">
                <Cpu size={18} className="text-indigo-400" />
                <span>Self-Healing Orchestration Lifecycle</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
                {[
                  { title: '1. Incident Detected', detail: 'Price null rate > 80%', state: 'DONE' },
                  { title: '2. AI Diagnosis', detail: 'Selector .price-tag failed', state: 'DONE' },
                  { title: '3. Repair Generated', detail: 'Patch: span[data-price-val]', state: demoState === 'RECOVERED' ? 'DONE' : 'RUNNING' },
                  { title: '4. Validation Retest', detail: 'Evaluating 20 records', state: demoState === 'RECOVERED' ? 'DONE' : 'WAITING' },
                  { title: '5. Repair Accepted', detail: 'Health restored to 98%', state: demoState === 'RECOVERED' ? 'DONE' : 'WAITING' },
                ].map((step, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-semibold text-slate-400">{step.title}</span>
                      {step.state === 'DONE' ? (
                        <CheckCircle2 size={16} className="text-emerald-400" />
                      ) : step.state === 'RUNNING' ? (
                        <RefreshCw size={16} className="text-indigo-400 animate-spin" />
                      ) : (
                        <div className="w-2 h-2 rounded-full bg-slate-700" />
                      )}
                    </div>
                    <p className="text-xs text-slate-500">{step.detail}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-200">Live Scraped Data Preview</h3>
              <span className="text-xs text-slate-400">Target: Amazon / Electronics Category</span>
            </div>
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950 text-slate-400 text-xs uppercase font-medium border-b border-slate-800">
                <tr>
                  <th className="px-6 py-3">Product Name</th>
                  <th className="px-6 py-3">Price</th>
                  <th className="px-6 py-3">Rating</th>
                  <th className="px-6 py-3">Availability</th>
                  <th className="px-6 py-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {[1, 2, 3, 4, 5].map((item) => (
                  <tr key={item} className="hover:bg-slate-800/30 transition">
                    <td className="px-6 py-4 font-medium text-white">Pro Wireless Headset ANC v{item}</td>
                    <td className="px-6 py-4">
                      {demoState === 'DEGRADED' && item > 1 ? (
                        <span className="text-rose-400 font-mono text-xs bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                          null (FAILED)
                        </span>
                      ) : (
                        <span className="font-mono text-slate-200">$299.99 USD</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-amber-400">★ 4.8</td>
                    <td className="px-6 py-4">
                      <span className="text-xs bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20">
                        In Stock
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {demoState === 'DEGRADED' && item > 1 ? (
                        <XCircle size={16} className="text-rose-400 inline" />
                      ) : (
                        <CheckCircle2 size={16} className="text-emerald-400 inline" />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
}
