import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Use internal cluster DNS for API routes (always available at runtime)
    const contestServiceUrl = 'http://contest-service.codeforces.svc.cluster.local:80';
    
    const response = await fetch(`${contestServiceUrl}/api/v1/contests/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
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
      { detail: error.message || 'Failed to fetch contests' },
      { status: 500 }
    );
  }
}
