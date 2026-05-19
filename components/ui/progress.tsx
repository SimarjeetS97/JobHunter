import { cn } from '@/lib/utils';

export function Progress({ value }: { value: number }) {
  return (
    <div className='h-2 w-full overflow-hidden rounded-full bg-slate-200' role='progressbar' aria-valuenow={value} aria-valuemin={0} aria-valuemax={100}>
      <div className={cn('h-full bg-slate-900 transition-all')} style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
    </div>
  );
}
