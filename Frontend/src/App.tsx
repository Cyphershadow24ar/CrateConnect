import React from 'react';
import { ScanPage } from './pages/ScanPage';
import './App.css';

export const App: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-lg font-bold text-white shadow-sm">
              🥗
            </span>
            <div>
              <span className="text-base font-bold text-slate-900">Food Rescue</span>
              <span className="ml-2 rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-semibold text-emerald-800">
                Phase 7 Scanner
              </span>
            </div>
          </div>
          <div className="text-xs text-slate-500 font-medium">
            Demo Tenant Active
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1">
        <ScanPage />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-400">
        AI-Powered Food Waste Management Platform &bull; Rapid Barcode/QR Inventory System
      </footer>
    </div>
  );
};

export default App;
