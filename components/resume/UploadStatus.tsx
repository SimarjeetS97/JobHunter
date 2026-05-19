import { Progress } from '@/components/ui/progress';
import { ResumeParsingState } from '@/types/resume';

export function UploadStatus({ state, progress }: { state: ResumeParsingState; progress: number }) {
  if (state === 'idle') return null;

  return (
    <div className='space-y-2'>
      {(state === 'uploading' || state === 'parsing') && <Progress value={progress} />}
      <p className='text-sm text-slate-700'>
        {state === 'uploading' && `Uploading resume... ${progress}%`}
        {state === 'parsing' && 'Parsing resume and extracting profile...'}
        {state === 'completed' && 'Resume successfully parsed.'}
        {state === 'error' && 'Upload failed.'}
      </p>
    </div>
  );
}
