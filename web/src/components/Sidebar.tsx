'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Sidebar() {
  const pathname = usePathname();
  const [companyName, setCompanyName] = useState('Perusahaan');

  useEffect(() => {
    // Hanya bisa dijalankan di client-side
    const storedName = localStorage.getItem('hrdash_company');
    if (storedName) {
      setCompanyName(storedName);
    }
  }, [pathname]);

  // Sembunyikan sidebar di halaman login
  if (pathname === '/login') {
    return null;
  }

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col hidden md:flex sticky top-0 h-screen shadow-[4px_0_24px_rgba(0,0,0,0.02)] z-20">
      <div className="p-6 border-b border-slate-100 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 text-white flex items-center justify-center font-black text-sm shadow-sm">
          HR
        </div>
        <div className="font-black text-xl tracking-tight text-slate-900">
          HR<span className="text-indigo-600">Dash</span>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <Link 
          href="/dashboard" 
          className={`flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all ${
            pathname === '/dashboard' || pathname.startsWith('/jobs')
              ? 'text-indigo-700 bg-indigo-50 shadow-sm shadow-indigo-100/50' 
              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
          Manajemen Lowongan
        </Link>
        <Link 
          href="/talent" 
          className={`flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all ${
            pathname.startsWith('/talent')
              ? 'text-indigo-700 bg-indigo-50 shadow-sm shadow-indigo-100/50' 
              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Database Talent
        </Link>
        <Link 
          href="/reports" 
          className={`flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all ${
            pathname.startsWith('/reports')
              ? 'text-indigo-700 bg-indigo-50 shadow-sm shadow-indigo-100/50' 
              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
          Laporan AI
        </Link>
        <Link 
          href="/settings" 
          className={`flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all ${
            pathname.startsWith('/settings')
              ? 'text-indigo-700 bg-indigo-50 shadow-sm shadow-indigo-100/50' 
              : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
          }`}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Pengaturan
        </Link>
      </nav>

      <div className="p-4 border-t border-slate-100">
        <div className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-50 border border-transparent hover:border-slate-100 transition-all cursor-pointer">
          <div className="w-10 h-10 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center font-bold text-sm uppercase tracking-wider">
            {companyName.substring(0, 2)}
          </div>
          <div className="overflow-hidden flex-1">
            <div className="text-sm font-bold text-slate-900 truncate">{companyName}</div>
            <div className="text-xs text-slate-500 truncate">Sistem ATS AI</div>
          </div>
        </div>
        {/* V0.2 Minggu 2 Dihapus sesuai instruksi */}
      </div>
    </aside>
  );
}
