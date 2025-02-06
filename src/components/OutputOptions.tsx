import React, { useState } from 'react';
import { Film, Headphones, BookText, Layout, BarChart } from 'lucide-react';

// Map icons to their respective components
const IconMap = {
  Film,
  Headphones,
  BookText,
  Layout,
  BarChart,
};

// Define the type for OutputOption
type OutputOption = {
  id: string;
  title: string;
  description: string;
  icon: keyof typeof IconMap;
  content: string;
  fileType: 'audio' | 'video' | 'image' | 'text';
  filePath: string;
  videoSize?: string; // Optional property for video sizes
};

// List of output options
const options: OutputOption[] = [
  {
    id: 'reels',
    title: 'Video',
    description: 'Convert your research into engaging short-form video content',
    icon: 'Film',
    content: 'Watch the generated video reel below:',
    fileType: 'video',
    filePath: '/outputs/video_output.mp4',
    videoSize: '19:6', // Default video size for reels
  },
  {
    id: 'reels-6-19',
    title: 'Video Reels (6:19)',
    description: 'Convert your research into engaging short-form video content in 6:19 aspect ratio',
    icon: 'Film',
    content: 'Watch the generated video reel below:',
    fileType: 'video',
    filePath: '/outputs/video_output.mp4',
    videoSize: '6:19', // Custom video size
  },
  {
    id: 'podcasts',
    title: 'Podcasts',
    description: 'Transform your paper into an audio format for easy listening',
    icon: 'Headphones',
    content: 'Listen to the generated podcast below:',
    fileType: 'audio',
    filePath: '/outputs/final_audio.mp3',
  },
  {
    id: 'blogs',
    title: 'Blog Posts',
    description: 'Create digestible blog content from your research',
    icon: 'BookText',
    content: 'See the generated blog post image below:',
    fileType: 'text',
    filePath: '/outputs/blog.html',
  },
  {
    id: 'ppt',
    title: 'Presentations',
    description: 'Generate PowerPoint slides highlighting key findings',
    icon: 'Layout',
    content: 'This is the detailed content for Presentations...',
    fileType: 'text',
    filePath: '/outputs/output.pptx',
  },
  {
    id: 'graphical',
    title: 'Visualizations',
    description: 'Create data visualizations and infographics',
    icon: 'BarChart',
    content: 'This is the detailed content for Visualizations...',
    fileType: 'text',
    filePath: '/outputs/visual.png',
  },
];

// ✅ Component to Show Selected Output
const SelectedOutput: React.FC<{ option: OutputOption; onClose: () => void }> = ({
  option,
  onClose,
}) => {
  const Icon = IconMap[option.icon];

  // Function to handle PPT to PDF conversion for "View Online"
  const handleViewPptOnline = (event: React.MouseEvent) => {
    event.preventDefault();
    window.open(option.filePath, '_blank');
  };

  // Function to handle viewing content online
  const handleViewOnline = (event: React.MouseEvent, filePath: string) => {
    event.preventDefault();
    window.open(filePath, '_blank');
  };

  // Function to handle downloading content
  const handleDownload = (event: React.MouseEvent, filePath: string, fileName: string) => {
    event.preventDefault();
    const link = document.createElement('a');
    link.href = filePath;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-8 rounded-lg shadow-lg w-96 relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          ✖
        </button>
        <Icon className="h-12 w-12 text-indigo-600 mx-auto" />
        <h3 className="text-2xl font-bold text-gray-900 text-center mt-4">
          {option.title}
        </h3>
        <p className="mt-4 text-gray-700 text-center">{option.content}</p>

        {/* ✅ Render Content Based on File Type */}
        <div className="mt-4 flex justify-center">
          {option.fileType === 'audio' && (
            <audio controls className="w-full">
              <source src={option.filePath} type="audio/mp3" />
              Your browser does not support the audio element.
            </audio>
          )}

          {option.fileType === 'video' && (
            <div>
              <div
                className={`relative w-full ${
                  option.videoSize === '6:19'
                    ? 'aspect-[9/16]' // Portrait aspect ratio (9:16)
                    : option.videoSize === '19:6'
                    ? 'aspect-[16/9]' // Landscape aspect ratio (16:9)
                    : 'aspect-video' // Default aspect ratio
                }`}
              >
                <video
                  controls
                  className="w-full h-full object-cover"
                  style={{
                    objectFit: 'contain', // Ensures the video content is fully visible
                  }}
                >
                  <source src={option.filePath} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
              {option.videoSize && (
                <p className="text-sm text-gray-500 mt-2">
                  Video Size: {option.videoSize}
                </p>
              )}
            </div>
          )}

          {option.fileType === 'image' && (
            <img src={option.filePath} alt={option.title} className="w-full rounded-lg" />
          )}

          {option.fileType === 'text' && (
            <div className="text-center">
              <p className="text-gray-700">Click below to view or download the content:</p>
              <div className="mt-4 space-x-4">
                {/* View Online Button */}
                {option.id === 'ppt' ? (
                  <button
                    onClick={(e) => handleViewPptOnline(e)}
                    className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                  >
                    View Online (PDF)
                  </button>
                ) : option.id === 'blogs' ? (
                  <button
                    onClick={(e) => handleViewOnline(e, option.filePath)}
                    className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                  >
                    View Blog
                  </button>
                ) : option.id === 'graphical' ? (
                  <button
                    onClick={(e) => handleViewOnline(e, option.filePath)}
                    className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                  >
                    View Visualization
                  </button>
                ) : (
                  <button
                    onClick={(e) => handleViewOnline(e, option.filePath)}
                    className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                  >
                    View Online
                  </button>
                )}

                {/* Download Button */}
                <button
                  onClick={(e) =>
                    handleDownload(
                      e,
                      option.filePath,
                      `${option.title}.${
                        option.id === 'ppt'
                          ? 'pptx'
                          : option.id === 'blogs'
                          ? 'html'
                          : option.id === 'graphical'
                          ? 'png'
                          : 'txt'
                      }`
                    )
                  }
                  className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                >
                  Download
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ✅ Main Component
export function OutputOptions() {
  const [selectedOutput, setSelectedOutput] = useState<OutputOption | null>(null);

  return (
    <div className="bg-gray-50 py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Choose Your Output Format
          </h2>
          <p className="mt-3 text-xl text-gray-500 sm:mt-4">
            Transform your research paper into multiple engaging formats
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {options.map((option) => {
              const Icon = IconMap[option.icon];
              return (
                <div
                  key={option.id}
                  className="relative rounded-lg border border-gray-300 bg-white p-6 shadow-sm hover:shadow-md transition-shadow duration-300 ease-in-out"
                >
                  <div>
                    <Icon className="h-8 w-8 text-indigo-600" />
                    <h3 className="mt-4 text-lg font-medium text-gray-900">
                      {option.title}
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      {option.description}
                    </p>
                  </div>
                  <div className="mt-6">
                    <button
                      type="button"
                      onClick={() => setSelectedOutput(option)}
                      className="inline-flex items-center rounded-md border border-transparent bg-indigo-100 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-200"
                    >
                      Learn more
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ✅ Load the SelectedOutput component dynamically */}
      {selectedOutput && (
        <SelectedOutput option={selectedOutput} onClose={() => setSelectedOutput(null)} />
      )}
    </div>
  );
}
