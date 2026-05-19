'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { uploadResume } from '@/lib/api/resume';
import { ExtractedProfile, ResumeParsingState } from '@/types/resume';

export function useResumeUpload() {
  const [progress, setProgress] = useState(0);
  const [state, setState] = useState<ResumeParsingState>('idle');
  const [error, setError] = useState<string | null>(null);
  const [profile, setProfile] = useState<ExtractedProfile | null>(null);

  const mutation = useMutation({
    mutationFn: async (file: File) => {
      setError(null);
      setProfile(null);
      setProgress(0);
      setState('uploading');

      const result = await uploadResume(file, setProgress);
      setState('parsing');

      if (result.status === 'error') {
        throw new Error(result.error ?? 'Could not parse resume.');
      }

      if (result.profile) {
        setProfile(result.profile);
      }

      setState('completed');
      return result;
    },
    onError: (err) => {
      setState('error');
      setError(err instanceof Error ? err.message : 'Something went wrong.');
    },
  });

  return {
    progress,
    state,
    error,
    profile,
    uploadResume: mutation.mutate,
    isPending: mutation.isPending,
    reset: () => {
      setProgress(0);
      setState('idle');
      setError(null);
      setProfile(null);
      mutation.reset();
    },
  };
}
