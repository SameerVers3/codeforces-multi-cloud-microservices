import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const contestServiceUrl = process.env.CONTEST_SERVICE_URL || 'http://contest-service.codeforces.svc.cluster.local:80';
    
    const response = await fetch(`${contestServiceUrl}/api/v1/contests/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { detail: error.message || 'Failed to fetch contests' },
      { status: 500 }
    );
  }
}
