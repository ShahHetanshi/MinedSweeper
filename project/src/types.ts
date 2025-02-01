export type OutputFormat = 'reels' | 'podcasts' | 'blogs' | 'ppt' | 'graphical';

export interface UploadedFile {
  id: string;
  name: string;
  type: 'pdf' | 'docx';
  uploadedAt: Date;
  status: 'processing' | 'completed' | 'error';
}

export interface OutputOption {
  id: OutputFormat;
  title: string;
  description: string;
  icon: string;
}