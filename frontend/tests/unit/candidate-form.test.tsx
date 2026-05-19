import React from 'react';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../utils/render';

function CandidateForm() {
  const [email, setEmail] = React.useState('');
  const [name, setName] = React.useState('');
  const [error, setError] = React.useState('');
  const [saved, setSaved] = React.useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaved(false);
    setError('');

    if (!email.includes('@') || name.trim().length < 2) {
      setError('Please provide valid input.');
      return;
    }

    const res = await fetch('/api/candidates', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email, name }),
    });

    if (!res.ok) {
      setError('Could not save candidate.');
      return;
    }

    setSaved(true);
  }

  return (
    <form onSubmit={onSubmit}>
      <input aria-label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input aria-label="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <button type="submit">Submit</button>
      {error && <p role="alert">{error}</p>}
      {saved && <p>Saved</p>}
    </form>
  );
}

test('shows validation errors for invalid input', async () => {
  renderWithProviders(<CandidateForm />);
  fireEvent.click(screen.getByRole('button', { name: /submit/i }));
  expect(await screen.findByRole('alert')).toHaveTextContent('Please provide valid input.');
});

test('submits successfully with valid input', async () => {
  renderWithProviders(<CandidateForm />);

  fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'ok@example.com' } });
  fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Alex' } });
  fireEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => expect(screen.getByText('Saved')).toBeInTheDocument());
});
