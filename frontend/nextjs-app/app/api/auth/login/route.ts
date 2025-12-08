import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Get the content type from the request
    const contentType = request.headers.get('content-type') || '';
    
    // Use internal cluster DNS for API routes (always available at runtime)
    const authServiceUrl = 'http://auth-service.codeforces.svc.cluster.local:80';
    
    let body;
    let headers: Record<string, string> = {};
    
    // Handle form data (application/x-www-form-urlencoded)
    if (contentType.includes('application/x-www-form-urlencoded')) {
      body = await request.text();
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else {
      // Handle JSON
      const jsonBody = await request.json();
      body = JSON.stringify(jsonBody);
      headers['Content-Type'] = 'application/json';
    }
    
    const response = await fetch(`${authServiceUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers,
      body,
    });

    const responseContentType = response.headers.get('content-type');
    let data;

    if (responseContentType?.includes('application/json')) {
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
