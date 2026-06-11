import React, { useState } from 'react';

export default function App() {
  // Application State Control
  const [file, setFile] = useState(null);
  const [sensitiveCol, setSensitiveCol] = useState('');
  const [targetCol, setTargetCol] = useState('');
  const [predCol, setPredCol] = useState('');
  const [privilegedValue, setPrivilegedValue] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [auditData, setAuditData] = useState(null);

  const [availableColumns, setAvailableColumns] = useState([]);

  const handleFileChange = async (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setAvailableColumns([]);
      setError(null);
      
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/inspect', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();
        if (data.success && data.columns.length > 0) {
          setAvailableColumns(data.columns);
          
          // Auto-assign the first 3 columns directly to the respective form inputs
          setSensitiveCol(data.columns[0]);                      // First column as Sensitive Attribute
          setTargetCol(data.columns[1] || data.columns[0]);       // Second column as Ground Truth
          setPredCol(data.columns[2] || data.columns[0]);         // Third column as Prediction Array
          setPrivilegedValue('');                                 // Clear reference to let user define baseline group
        }
      } catch (err) {
        console.error("Automated header inspection pipeline failure:", err);
      }
    }
  };

  const runAuditPipeline = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a valid CSV dataset to audit first.");
      return;
    }

    setLoading(true);
    setError(null);
    setAuditData(null);

    // Prepare Multipart Form Data to stream to our FastAPI backend
    const formData = new FormData();
    formData.append('file', file);
    formData.append('sensitive_column', sensitiveCol);
    formData.append('target_column', targetCol);
    formData.append('prediction_column', predCol);
    formData.append('privileged_value', privilegedValue.trim() || "");

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/audit', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned status protocol exception: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.success) {
        setAuditData(data);
      } else {
        throw new Error("Audit execution pipeline reported an unhandled failure state.");
      }
    } catch (err) {
      setError(err.message || "Failed to establish a network connection to the auditing backend engine.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans antialiased">
      {/* Top Navigation Branding Header */}
      <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
            FairShield Core
          </h1>
        </div>
        <span className="text-xs font-mono text-slate-400 bg-slate-800/60 px-3 py-1 rounded-full border border-slate-700">
          v1.0.0 Stable
        </span>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* LEFT COLUMN: Data Configuration Inputs */}
        <section className="lg:col-span-4 bg-slate-950/40 border border-slate-800 rounded-2xl p-6 h-fit backdrop-blur">
          <h2 className="text-lg font-semibold text-white mb-1">Audit Configuration</h2>
          <p className="text-xs text-slate-400 mb-6">Define schema features to isolate bias dimensions.</p>

          <form onSubmit={runAuditPipeline} className="space-y-5">
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-slate-400 mb-2">Select Dataset (.CSV)</label>
              <input 
                type="file" 
                accept=".csv"
                onChange={handleFileChange}
                className="w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 file:cursor-pointer cursor-pointer bg-slate-900/50 border border-slate-800 rounded-xl p-2"
              />
              {file && <p className="text-xs text-emerald-400 mt-1.5 font-mono">✓ Loaded: {file.name}</p>}
            </div>

            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="block text-xs font-medium uppercase tracking-wider text-slate-400 mb-1.5">Sensitive Attribute</label>
                <input type="text" value={sensitiveCol} onChange={(e) => setSensitiveCol(e.target.value)} className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-slate-200" />
              </div>
              <div>
                <label className="block text-xs font-medium uppercase tracking-wider text-slate-400 mb-1.5">Privileged Group Reference</label>
                <input type="text" value={privilegedValue} onChange={(e) => setPrivilegedValue(e.target.value)} className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-slate-200" />
              </div>
              <div>
                <label className="block text-xs font-medium uppercase tracking-wider text-slate-400 mb-1.5">Ground Truth Column</label>
                <input type="text" value={targetCol} onChange={(e) => setTargetCol(e.target.value)} className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-slate-200" />
              </div>
              <div>
                <label className="block text-xs font-medium uppercase tracking-wider text-slate-400 mb-1.5">Prediction Column</label>
                <input type="text" value={predCol} onChange={(e) => setPredCol(e.target.value)} className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500 text-slate-200" />
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className={`w-full py-3 px-4 rounded-xl font-semibold text-sm transition-all duration-200 shadow-lg ${loading ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:from-emerald-400 hover:to-teal-500 shadow-emerald-950/20'}`}
            >
              {loading ? 'Processing Fairlearn Auditing...' : 'Execute Compliance Audit'}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-3 bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs rounded-xl font-mono">
              ⚠️ Error: {error}
            </div>
          )}
        </section>

        {/* RIGHT COLUMN: Interactive Charts & Generative Audit Report Results */}
        <section className="lg:col-span-8 space-y-6">
          {!auditData && !loading && (
            <div className="border border-dashed border-slate-800 rounded-2xl p-20 text-center bg-slate-950/10 backdrop-blur">
              <div className="mx-auto h-12 w-12 text-slate-600 mb-4 text-3xl">📊</div>
              <h3 className="text-lg font-medium text-slate-300 mb-1">Awaiting Assessment Payload</h3>
              <p className="text-sm text-slate-500 max-w-sm mx-auto">Upload your local audit-ready dataset and parameters on the left to review metrics and compliance text reports.</p>
            </div>
          )}

          {loading && (
            <div className="border border-slate-800 rounded-2xl p-20 text-center bg-slate-950/20 backdrop-blur space-y-4">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-emerald-500 border-t-transparent" />
              <p className="text-sm text-slate-400 font-mono">Analyzing demographic distribution curves & querying LLM framework...</p>
            </div>
          )}

          {auditData && (
            <div className="space-y-6 animate-fadeIn">
              {/* Scorecard Hero Ribbons */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                  <span className="text-xs font-medium text-slate-400 block uppercase tracking-wider mb-1">Disparate Impact Ratio</span>
                  <div className="text-2xl font-bold text-white font-mono">{auditData.metrics.summary.disparate_impact_ratio}</div>
                  <span className="text-[10px] text-slate-500 mt-1 block">Legal Threshold Target: ≥ 0.80</span>
                </div>
                <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-4">
                  <span className="text-xs font-medium text-slate-400 block uppercase tracking-wider mb-1">Statistical Parity Diff</span>
                  <div className="text-2xl font-bold text-white font-mono">{auditData.metrics.summary.statistical_parity_difference}</div>
                  <span className="text-[10px] text-slate-500 mt-1 block">Optimal Bias Parity Value: 0.00</span>
                </div>
                <div className={`border rounded-xl p-4 ${auditData.metrics.summary.is_four_fifths_compliant ? 'bg-emerald-950/30 border-emerald-800/50' : 'bg-rose-950/30 border-rose-800/50'}`}>
                  <span className="text-xs font-medium text-slate-400 block uppercase tracking-wider mb-1">Compliance Ruling</span>
                  <div className={`text-xl font-bold font-mono mt-1 ${auditData.metrics.summary.is_four_fifths_compliant ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {auditData.metrics.summary.is_four_fifths_compliant ? '✓ LAWFUL COMPLIANT' : '✕ BIASED / NON-COMPLIANT'}
                  </div>
                  <span className="text-[10px] text-slate-500 mt-1 block">Evaluated via Universal Algorithmic Parity Standard</span>
                </div>
              </div>

              {/* Demographic Group Metric Breakdown Table */}
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-5">
                <h3 className="text-sm font-semibold text-white mb-3 uppercase tracking-wider">Demographic Distribution Splitting</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse text-xs font-mono">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400">
                        <th className="py-2.5">Demographic Value Group</th>
                        <th className="py-2.5 text-center">Sample Cohort Size</th>
                        <th className="py-2.5 text-center">Selection Rate (Positive Output)</th>
                        <th className="py-2.5 text-center">True Positive Rate (TPR)</th>
                        <th className="py-2.5 text-center">False Positive Rate (FPR)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50 text-slate-300">
                      {Object.entries(auditData.metrics.breakdown).map(([groupName, values]) => (
                        <tr key={groupName} className="hover:bg-slate-900/30">
                          <td className="py-3 font-semibold text-slate-200">{groupName}</td>
                          <td className="py-3 text-center">{values.sample_size}</td>
                          <td className="py-3 text-center text-cyan-400">{(values.selection_rate * 100).toFixed(2)}%</td>
                          <td className="py-3 text-center">{(values.true_positive_rate * 100).toFixed(2)}%</td>
                          <td className="py-3 text-center">{(values.false_positive_rate * 100).toFixed(2)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Generative LLM Governance Written Audit Report Text Panel */}
              <div className="bg-slate-950/60 border border-slate-800 rounded-xl p-6">
                <div className="flex items-center gap-2 mb-4 pb-2 border-b border-slate-800">
                  <span className="text-lg">🤖</span>
                  <h3 className="text-sm font-semibold text-white uppercase tracking-wider">AI GRC Governance Compliance Report</h3>
                </div>
                <div className="text-sm text-slate-300 whitespace-pre-wrap leading-relaxed font-sans max-h-96 overflow-y-auto pr-2">
                  {auditData.report}
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}