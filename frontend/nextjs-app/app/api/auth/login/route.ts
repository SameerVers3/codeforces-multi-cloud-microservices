import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Use internal cluster DNS for API routes (always available at runtime)
    const authServiceUrl = 'http://auth-service.codeforces.svc.cluster.local:80';
    
    const response = await fetch(`${authServiceUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const contentType = response.headers.get('content-type');
    let data;

    if (contentType?.includes('application/json')) {
      data = await response.json();
    } else {
      const text = await response.text();
      return NextResponse.json(
        { detail: `Backend returned non-JSON response: ${text.substring(0, 200)}` },
        { status: 502 }
      );
    }
    
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { detail: error.message || 'Login failed' },
      { status: 500 }
    );
  }
}
