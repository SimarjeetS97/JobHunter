export type ResumeParsingState = 'idle' | 'uploading' | 'parsing' | 'completed' | 'error';

export interface UploadedResumeResponse {
  uploadId: string;
  status: 'uploaded' | 'parsing' | 'completed' | 'error';
  profile?: ExtractedProfile;
  error?: string;
}

export interface ExtractedProfile {
  fullName: string;
  email: string;
  phone?: string;
  location?: string;
  summary?: string;
  skills: string[];
  experiences: Experience[];
  education: Education[];
}

export interface Experience {
  company: string;
  title: string;
  startDate: string;
  endDate?: string;
  highlights: string[];
}

export interface Education {
  institution: string;
  degree: string;
  graduationDate?: string;
}
