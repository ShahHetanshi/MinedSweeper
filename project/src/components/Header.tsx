import React from 'react';
import { BookOpen } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-indigo-600">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Top">
        <div className="flex w-full items-center justify-between py-6">
          <div className="flex items-center">
            <a href="/" className="flex items-center space-x-3">
              <BookOpen className="h-8 w-8 text-white" />
              <span className="text-2xl font-bold text-white">Minedsweeper</span>
            </a>
          </div>
          {/* <div className="ml-10 space-x-4">
            <a
              href="#"
              className="inline-block rounded-md border border-transparent bg-white py-2 px-4 text-base font-medium text-indigo-600 hover:bg-indigo-50"
            >
              Sign in
            </a>
          </div> */}
        </div>
      </nav>
    </header>
  );
}