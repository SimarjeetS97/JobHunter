import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

export const handlers = [
  http.post('/api/candidates', async ({ request }) => {
    const body = (await request.json()) as { email?: string; name?: string };
    if (!body.email || !body.name) {
      return HttpResponse.json({ detail: 'Missing fields' }, { status: 422 });
    }
    return HttpResponse.json({ id: 'cand_123', ...body }, { status: 201 });
  }),
];

export const server = setupServer(...handlers);
