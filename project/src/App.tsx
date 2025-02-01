import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { OutputOptions } from './components/OutputOptions';

function App() {
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-gray-100' : 'bg-gradient-to-br from-indigo-50 to-white text-gray-900'}`}>
      <Header />
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="absolute top-4 right-4 p-3 bg-indigo-600 text-white rounded-full hover:bg-indigo-800 transition shadow-md"
      >
        {darkMode ? '☀️' : '🌙'}
      </button>
      <main className="flex-grow container mx-auto px-6 py-12 sm:px-10 lg:px-16">
        <div className={`shadow-lg rounded-2xl p-8 transition-transform transform hover:scale-105 ${darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white text-gray-900'}`}>          
          {/* <h2 className="text-3xl font-extrabold text-center mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}">Upload Your Research Paper</h2> */}
          <UploadSection />
        </div>
        <div className={`mt-10 shadow-lg rounded-2xl p-8 transition-transform transform hover:scale-105 ${darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white text-gray-900'}`}>          
          {/* <h2 className="text-3xl font-extrabold text-center mb-6 ${darkMode ? 'text-white' : 'text-gray-900'}">Choose Your Output Format</h2> */}
          <OutputOptions />
        </div>
      </main>
      
      <footer className={`mt-auto py-6 text-center text-base font-semibold rounded-t-2xl shadow-lg ${darkMode ? 'bg-gray-800 text-gray-300' : 'bg-indigo-700 text-white'}`}>        
        <p className="tracking-wide">&copy; {new Date().getFullYear()} Minedsweeper. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
