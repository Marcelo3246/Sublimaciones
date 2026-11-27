import { useState } from "react";

export function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 border border-slate-700 rounded-xl p-8 shadow-xl text-center">
        <h1 className="text-3xl font-bold tracking-tight text-white mb-2">
          DLL Sublimados
        </h1>
        <p className="text-sm text-slate-400 mb-6">
          Frontend SPA (React 19 + JavaScript + Vite + Tailwind CSS v4)
        </p>

        <div className="bg-slate-900/60 rounded-lg p-4 mb-6 border border-slate-700/50 text-left text-xs font-mono text-slate-300">
          <p className="text-emerald-400 font-semibold mb-1">● Backend API:</p>
          <p>Proxy configurado en /api → http://localhost:8000</p>
        </div>

        <button
          onClick={() => setCount((c) => c + 1)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white font-medium rounded-lg transition-colors cursor-pointer"
        >
          Contador: {count}
        </button>

        <p className="mt-6 text-xs text-slate-500">
          Plantilla base lista para el desarrollo del Grupo de Frontend.
        </p>
      </div>
    </div>
  );
}

export default App;

