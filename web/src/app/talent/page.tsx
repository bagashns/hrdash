'use client';

export default function TalentPage() {
  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50/50 overflow-y-auto">
      <div className="bg-white px-8 py-6 border-b border-slate-200 flex justify-between items-center sticky top-0 z-10 shadow-sm">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Database Talent</h1>
          <p className="text-slate-500 mt-1 text-sm font-medium">Jelajahi seluruh profil kandidat yang pernah melamar di perusahaan Anda.</p>
        </div>
      </div>
      <div className="p-8 max-w-7xl mx-auto w-full flex-1 flex flex-col items-center justify-center">
        <div className="w-24 h-24 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-12 h-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
        </div>
        <h3 className="text-2xl font-black text-slate-900 mb-3 tracking-tight">Segera Hadir</h3>
        <p className="text-slate-500 max-w-md mx-auto leading-relaxed text-center">Fitur pencarian dan penyaringan seluruh Database Talent sedang dalam tahap pengembangan. Pantau terus pembaruan selanjutnya!</p>
      </div>
    </div>
  );
}
