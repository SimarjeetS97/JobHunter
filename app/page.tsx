'use client';

import { Dropzone } from '@/components/resume/Dropzone';
import { ProfilePreview } from '@/components/resume/ProfilePreview';
import { UploadStatus } from '@/components/resume/UploadStatus';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useResumeUpload } from '@/hooks/useResumeUpload';

export default function HomePage() {
  const { error, profile, progress, state, uploadResume, isPending } = useResumeUpload();

  return (
    <main className='mx-auto grid min-h-screen max-w-5xl gap-6 p-4 md:grid-cols-2 md:p-8'>
      <Card className='h-fit'>
        <CardHeader>
          <CardTitle>Upload Resume</CardTitle>
        </CardHeader>
        <CardContent className='space-y-4'>
          <Dropzone onFileSelect={uploadResume} disabled={isPending} />
          <UploadStatus state={state} progress={progress} />
          {error ? (
            <p role='alert' className='rounded-md bg-red-50 p-3 text-sm text-red-700'>
              {error}
            </p>
          ) : null}
        </CardContent>
      </Card>

      <ProfilePreview profile={profile} />
    </main>
  );
}
