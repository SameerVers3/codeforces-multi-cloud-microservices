import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const authServiceUrl = process.env.AUTH_SERVICE_URL || 'http://auth-service.codeforces.svc.cluster.local:80';
    
    const response = await fetch(`${authServiceUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { detail: error.message || 'Login failed' },
      { status: 500 }
    );
  }
}
