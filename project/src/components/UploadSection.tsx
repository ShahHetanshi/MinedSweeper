import React, { useState, useEffect } from 'react';
import { Upload } from 'lucide-react';

export function UploadSection() {
  const [file, setFile] = useState<File | null>(null);
  const [showLanguageOptions, setShowLanguageOptions] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  useEffect(() => {
    if (error) {
      setShowLanguageOptions(false);
      setIsProcessing(false);
      setIsSuccess(false); // Reset success state on error
    }
  }, [error]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIsSuccess(false); // Reset success state when a new file is selected
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setShowLanguageOptions(true);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  const handleLanguageSelect = (language: string) => {
    setSelectedLanguage(prev => (prev === language ? null : language));
  };

  const handleFileUpload = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault(); // Prevent form submission
    event.stopPropagation(); // Extra safety

    if (!file || !selectedLanguage) return;

    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', selectedLanguage);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setSummary(data.summary);
        setIsSuccess(true);
      } else {
        setError(data.error || 'Unknown error occurred');
      }
    } catch (err) {
      setError('Failed to upload file');
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-gray-50 py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Upload Your Research Paper
        </h2>
        <p className="mt-3 text-xl text-gray-500 sm:mt-4">
          Convert your research into multiple engaging formats
        </p>
      </div>

      <div className="mt-10 flex justify-center">
        <label
          htmlFor="file-upload"
          className="flex flex-col items-center justify-center w-full max-w-lg p-6 bg-white border border-gray-300 rounded-lg shadow-md cursor-pointer hover:border-indigo-500"
        >
          <Upload className="h-12 w-12 text-indigo-600" />
          <span className="mt-2 text-lg font-medium text-gray-900">Upload a PDF file</span>
          <input
            id="file-upload"
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={handleFileChange}
          />
          <p className="mt-1 text-sm text-gray-500">Only PDF files, up to 10MB</p>
        </label>
      </div>

      {showLanguageOptions && !isProcessing && (
        <div className="mt-6 text-center">
          <p className="text-lg font-semibold text-gray-900">Select Languages:</p>
          <div className="mt-2 flex justify-center space-x-4">
            {['English', 'Hindi', 'Gujarati'].map((language) => (
              <button
                key={language}
                type="button" // Prevent form submission
                onClick={() => handleLanguageSelect(language.toLowerCase())}
                className={`px-4 py-2 rounded-lg ${
                  selectedLanguage === language.toLowerCase()
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700'
                }`}
              >
                {language}
              </button>
            ))}
          </div>
          <button
            type="button" // Prevent form submission
            onClick={handleFileUpload}
            className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Process PDF
          </button>
        </div>
      )}

      {isProcessing && (
        <div className="mt-6 text-center">
          <button
            type="button" // Prevent form submission
            disabled
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg cursor-not-allowed"
          >
            Processing...
          </button>
        </div>
      )}

      {summary && (
        <div className="mt-6 mx-auto max-w-4xl p-4 bg-gray-100 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold">Summary:</h3>
          <p className="mt-2 text-gray-700">{summary}</p>
        </div>
      )}

      {isSuccess && !isProcessing && (
        <div className="mt-6 text-center">
          <p className="text-2xl font-bold text-green-600">Hooray 🎉 Uploaded successfully!</p>
        </div>
      )}
    </div>
  );
}