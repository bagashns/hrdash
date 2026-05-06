'use client';

export default function ReportsPage() {
  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50/50 overflow-y-auto">
      <div className="bg-white px-8 py-6 border-b border-slate-200 flex justify-between items-center sticky top-0 z-10 shadow-sm">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Laporan AI</h1>
          <p className="text-slate-500 mt-1 text-sm font-medium">Lihat ringkasan kinerja rekrutmen dan wawasan yang dihasilkan oleh AI.</p>
        </div>
      </div>
      <div className="p-8 max-w-7xl mx-auto w-full flex-1 flex flex-col items-center justify-center">
        <div className="w-24 h-24 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-12 h-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
        </div>
        <h3 className="text-2xl font-black text-slate-900 mb-3 tracking-tight">Segera Hadir</h3>
        <p className="text-slate-500 max-w-md mx-auto leading-relaxed text-center">Modul visualisasi analitik dan pelaporan data pelamar berbasis AI akan tersedia pada rilis versi berikutnya.</p>
      </div>
    </div>
  );
}
