'use client';

import { useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface DropzoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

const ACCEPTED_TYPES = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

export function Dropzone({ onFileSelect, disabled }: DropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateAndSelect = (file: File | undefined) => {
    if (!file) return;
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError('Please upload a PDF or Word document.');
      return;
    }
    setError(null);
    onFileSelect(file);
  };

  return (
    <div>
      <div
        className={cn(
          'rounded-lg border-2 border-dashed p-8 text-center transition',
          isDragging ? 'border-slate-900 bg-slate-50' : 'border-slate-300',
        )}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          if (disabled) return;
          validateAndSelect(event.dataTransfer.files?.[0]);
        }}
        onDragOver={(event) => {
          event.preventDefault();
          if (!disabled) setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        aria-label='Resume upload dropzone'
      >
        <p className='text-sm text-slate-600'>Drag and drop your resume here</p>
        <p className='my-3 text-xs text-slate-500'>PDF, DOC, or DOCX</p>
        <Button type='button' onClick={() => inputRef.current?.click()} disabled={disabled}>
          Choose File
        </Button>
        <input
          ref={inputRef}
          type='file'
          accept='.pdf,.doc,.docx'
          className='hidden'
          onChange={(event) => validateAndSelect(event.target.files?.[0])}
          disabled={disabled}
        />
      </div>
      {error ? <p className='mt-2 text-sm text-red-600'>{error}</p> : null}
    </div>
  );
}
