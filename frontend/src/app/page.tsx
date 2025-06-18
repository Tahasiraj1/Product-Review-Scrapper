'use client';

import { useState } from 'react';
import ReviewTable from '@/components/ReviewTable';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Review {
  product_name: string;
  review_text: string;
  rating: number;
  sentiment: 'positive' | 'neutral' | 'negative';
}

export default function Home() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [url, setUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch reviews');
      }

      const data = await response.json();
      if (!Array.isArray(data)) {
        throw new Error('Invalid response: Expected an array of reviews');
      }

      setReviews(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      console.error('Error:', err);
      setReviews([]); // Reset reviews on error
    } finally {
      setLoading(false);
    }
  };

  // Calculate sentiment counts safely
  const sentimentCounts = Array.isArray(reviews)
    ? reviews.reduce<Record<'positive' | 'neutral' | 'negative', number>>(
        (acc, review) => {
          acc[review.sentiment] = (acc[review.sentiment] || 0) + 1;
          return acc;
        },
        { positive: 0, neutral: 0, negative: 0 }
      )
    : { positive: 0, neutral: 0, negative: 0 };

  const chartData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        label: 'Sentiment Distribution',
        data: [
          sentimentCounts.positive,
          sentimentCounts.neutral,
          sentimentCounts.negative,
        ],
        backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
      },
    ],
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Product Review Scraper</h1>
      <div className="mb-4">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter Daraz product URL"
          className="border p-2 mr-2 w-64"
        />
        <button
          onClick={handleScrape}
          disabled={loading}
          className="bg-blue-500 text-white p-2 rounded disabled:bg-gray-400"
        >
          {loading ? 'Scraping...' : 'Scrape Reviews'}
        </button>
      </div>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <ReviewTable reviews={reviews} />
      {reviews.length > 0 && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">Sentiment Distribution</h2>
          <Bar data={chartData} />
        </div>
      )}
    </div>
  );
}