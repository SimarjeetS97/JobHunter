import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ExtractedProfile } from '@/types/resume';

export function ProfilePreview({ profile }: { profile: ExtractedProfile | null }) {
  if (!profile) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Extracted Profile Preview</CardTitle>
      </CardHeader>
      <CardContent className='space-y-4 text-sm'>
        <section>
          <h3 className='font-semibold'>{profile.fullName}</h3>
          <p>{profile.email}</p>
          {profile.phone ? <p>{profile.phone}</p> : null}
        </section>

        <section>
          <h4 className='font-medium'>Skills</h4>
          <ul className='mt-2 flex flex-wrap gap-2'>
            {profile.skills.map((skill) => (
              <li key={skill} className='rounded bg-slate-100 px-2 py-1 text-xs'>
                {skill}
              </li>
            ))}
          </ul>
        </section>
      </CardContent>
    </Card>
  );
}
