'use client';

import { useState } from 'react';
import ReviewTable from '@/components/ReviewTable';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);


export default function Home() {
  const [reviews, setReviews] = useState([]);
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await response.json();
      setReviews(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  type Sentiment = 'positive' | 'neutral' | 'negative';
  type Review = { sentiment: Sentiment; };
  
  const sentimentCounts = reviews.reduce<Record<Sentiment, number>>((acc, review: Review) => {
    acc[review.sentiment] = (acc[review.sentiment] || 0) + 1;
    return acc;
  }, {
    positive: 0,
    neutral: 0,
    negative: 0
  });

  const chartData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
      label: 'Sentiment Distribution',
      data: [
        sentimentCounts.positive || 0,
        sentimentCounts.neutral || 0,
        sentimentCounts.negative || 0
      ],
      backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
    }]
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
          className="border p-2 mr-2"
        />
        <button
          onClick={handleScrape}
          disabled={loading}
          className="bg-blue-500 text-white p-2 rounded"
        >
          {loading ? 'Scraping...' : 'Scrape Reviews'}
        </button>
      </div>
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