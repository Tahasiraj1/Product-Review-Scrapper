import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { url } = await request.json();

    if (!url || typeof url !== 'string') {
      return NextResponse.json({ detail: 'Invalid or missing URL' }, { status: 400 });
    }

    const response = await fetch('http://127.0.0.1:8000/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { detail: errorData.detail || 'Backend error' },
        { status: response.status }
      );
    }

    const data = await response.json();
    if (!Array.isArray(data)) {
      return NextResponse.json(
        { detail: 'Invalid response from backend: Expected an array' },
        { status: 500 }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { detail: 'Server error: Unable to process request' },
      { status: 500 }
    );
  }
}