import type { ApiHealthResponse } from "@packages/types";

export class ApiClient {
  constructor(private readonly baseUrl: string) {}

  async healthCheck(): Promise<ApiHealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    return (await response.json()) as ApiHealthResponse;
  }
}
