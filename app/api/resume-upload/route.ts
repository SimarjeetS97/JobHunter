import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get('resume');

  if (!(file instanceof File)) {
    return NextResponse.json({ status: 'error', error: 'Resume file is required.' }, { status: 400 });
  }

  if (file.size > 5 * 1024 * 1024) {
    return NextResponse.json({ status: 'error', error: 'Max upload size is 5MB.' }, { status: 413 });
  }

  return NextResponse.json({
    uploadId: crypto.randomUUID(),
    status: 'completed',
    profile: {
      fullName: 'Jane Candidate',
      email: 'jane@example.com',
      phone: '+1 555 0134',
      skills: ['TypeScript', 'React', 'Next.js'],
      experiences: [],
      education: [],
    },
  });
}
