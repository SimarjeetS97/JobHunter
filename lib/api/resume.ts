import { UploadedResumeResponse } from '@/types/resume';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? '';

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export async function uploadResume(
  file: File,
  onProgress: (progress: number) => void,
): Promise<UploadedResumeResponse> {
  const formData = new FormData();
  formData.append('resume', file);

  for (let progress = 10; progress <= 90; progress += 20) {
    await sleep(100);
    onProgress(progress);
  }

  const response = await fetch(`${API_BASE}/api/resume-upload`, {
    method: 'POST',
    body: formData,
  });

  onProgress(100);

  if (!response.ok) {
    throw new Error('Failed to upload resume. Please try again.');
  }

  return (await response.json()) as UploadedResumeResponse;
}
