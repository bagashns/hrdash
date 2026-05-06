'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [companyName, setCompanyName] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (companyName.trim().length < 3) {
      alert('Nama perusahaan harus diisi minimal 3 karakter!');
      return;
    }
    if (password.length < 4) {
      alert('Password minimal 4 karakter!');
      return;
    }

    setIsLoading(true);
    const nameToSave = companyName.trim();

    try {
      // Import supabase dynamically to avoid issues
      const { supabase } = await import('@/utils/supabase');
      
      // Check if company exists
      let { data: company, error: fetchError } = await supabase
        .from('companies')
        .select('id, name')
        .ilike('name', nameToSave)
        .single();

      if (fetchError && fetchError.code !== 'PGRST116') {
        throw fetchError; // Error selain 'not found'
      }

      if (isLogin) {
        // FLOW LOGIN
        if (!company) {
          alert('Akun perusahaan belum terdaftar. Silakan registrasi terlebih dahulu.');
          setIsLoading(false);
          return;
        }
      } else {
        // FLOW REGISTER
        if (company) {
          alert('Perusahaan ini sudah terdaftar. Silakan langsung login.');
          setIsLoading(false);
          return;
        }

        // Create new company
        const { data: newCompany, error: insertError } = await supabase
          .from('companies')
          .insert([{ name: nameToSave }])
          .select()
          .single();
          
        if (insertError) throw insertError;
        company = newCompany;
        alert('Registrasi berhasil! Mengarahkan ke Dashboard...');
      }

      // Save to localStorage
      localStorage.setItem('hrdash_company_id', company.id);
      localStorage.setItem('hrdash_company', company.name);
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      alert('Terjadi kesalahan: ' + err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex w-full">
      {/* KIRI: Form Area */}
      <div className="flex-1 flex flex-col justify-center py-12 px-8 sm:px-12 lg:px-24 xl:px-32 relative z-10">
        <div className="w-full max-w-[420px] mx-auto">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 text-white flex items-center justify-center font-black text-sm shadow-md shadow-indigo-200">
              HR
            </div>
            <div className="font-black text-2xl tracking-tight text-slate-900">
              HR<span className="text-indigo-600">Dash</span>
            </div>
          </div>

          <div>
            <h2 className="text-3xl font-black text-slate-900 tracking-tight">
              {isLogin ? 'Selamat Datang Kembali' : 'Mulai Bersama HRDash'}
            </h2>
            <p className="mt-3 text-base text-slate-500">
              {isLogin 
                ? 'Masuk ke portal HR perusahaan Anda untuk melanjutkan proses rekrutmen berbasis AI.' 
                : 'Daftarkan perusahaan Anda dan rasakan kemudahan menyeleksi ratusan CV dalam hitungan detik.'}
            </p>
          </div>

          <div className="mt-10">
            <form className="space-y-6" onSubmit={handleSubmit}>
              <div>
                <label className="block text-sm font-bold text-slate-900 mb-2">
                  Nama Perusahaan
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
                  </div>
                  <input
                    type="text"
                    required
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    className="block w-full pl-11 pr-4 py-3.5 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-50/50 hover:bg-white transition-colors"
                    placeholder="Contoh: PT. Teknologi Nusantara"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-slate-900 mb-2">
                  Kata Sandi
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                  </div>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full pl-11 pr-4 py-3.5 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-50/50 hover:bg-white transition-colors"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              {isLogin && (
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="remember-me"
                      name="remember-me"
                      type="checkbox"
                      className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded cursor-pointer"
                    />
                    <label htmlFor="remember-me" className="ml-2 block text-sm text-slate-600 cursor-pointer">
                      Ingat perangkat ini
                    </label>
                  </div>
                  <div className="text-sm">
                    <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
                      Lupa sandi?
                    </a>
                  </div>
                </div>
              )}

              <div>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full flex justify-center py-3.5 px-4 rounded-xl shadow-sm text-sm font-bold text-white bg-slate-900 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 transition-all disabled:opacity-70 flex items-center justify-center gap-2"
                >
                  {isLoading && (
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  )}
                  {isLogin ? 'Masuk ke Dasbor' : 'Daftarkan Perusahaan'}
                </button>
              </div>
            </form>

            <div className="mt-8 text-center">
              <p className="text-sm text-slate-600">
                {isLogin ? 'Belum mendaftarkan perusahaan?' : 'Sudah mendaftarkan perusahaan?'}
                <button
                  onClick={() => setIsLogin(!isLogin)}
                  className="ml-1.5 font-bold text-indigo-600 hover:text-indigo-500 transition-colors"
                >
                  {isLogin ? 'Daftar sekarang' : 'Masuk di sini'}
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* KANAN: Ornamen Visual / Branding */}
      <div className="hidden lg:flex lg:flex-1 relative bg-slate-900 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
        <div className="absolute -top-[20%] -right-[10%] w-[70%] h-[70%] bg-indigo-500 rounded-full mix-blend-multiply filter blur-[120px] opacity-40 animate-blob"></div>
        <div className="absolute -bottom-[20%] -left-[10%] w-[70%] h-[70%] bg-purple-500 rounded-full mix-blend-multiply filter blur-[120px] opacity-40 animate-blob animation-delay-2000"></div>
        
        <div className="relative z-10 w-full h-full flex flex-col justify-center px-16 xl:px-24">
          <h2 className="text-4xl xl:text-5xl font-black text-white leading-tight mb-6">
            Otomatisasi<br/>Rekrutmen dengan<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              Kecerdasan Buatan.
            </span>
          </h2>
          <p className="text-lg text-slate-300 leading-relaxed max-w-lg mb-12">
            HRDash membantu tim HR memangkas waktu seleksi resume hingga 90%. Analisis CV ratusan kandidat dan temukan *Top Talent* yang sesuai dengan kriteria Anda secara otomatis.
          </p>
          
          <div className="flex gap-4">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/10 max-w-[200px]">
              <div className="text-indigo-400 font-bold mb-1">99%</div>
              <div className="text-sm text-slate-300">Akurasi Pencocokan Berbasis Konteks</div>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/10 max-w-[200px]">
              <div className="text-purple-400 font-bold mb-1">10x Lebih Cepat</div>
              <div className="text-sm text-slate-300">Daripada Membaca CV Secara Manual</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
