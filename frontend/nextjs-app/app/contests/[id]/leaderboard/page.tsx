'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import axios from 'axios';
// WebSocket connection will be handled via native WebSocket API

interface LeaderboardEntry {
  rank: number;
  user_id: string;
  total_score: number;
  total_submissions: number;
  total_accepted: number;
  last_submission_at: string | null;
}

export default function LeaderboardPage() {
  const params = useParams();
  const contestId = params.id as string;
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();

    // Connect to WebSocket for real-time updates
    const wsUrl = process.env.NEXT_PUBLIC_LEADERBOARD_SERVICE_URL?.replace('http', 'ws') || 'ws://localhost:8006';
    const socket = new WebSocket(`${wsUrl}/ws/leaderboard/${contestId}`);
    
    socket.onopen = () => {
      console.log('Connected to leaderboard updates');
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (Array.isArray(data)) {
          setLeaderboard(data);
        }
      } catch (error) {
        console.error('Error parsing leaderboard update:', error);
      }
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      socket.close();
    };
  }, [contestId]);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_LEADERBOARD_SERVICE_URL}/api/v1/leaderboard/contest/${contestId}`
      );
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container mx-auto p-4">Loading leaderboard...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Leaderboard</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 border">Rank</th>
              <th className="px-4 py-2 border">User ID</th>
              <th className="px-4 py-2 border">Score</th>
              <th className="px-4 py-2 border">Submissions</th>
              <th className="px-4 py-2 border">Accepted</th>
              <th className="px-4 py-2 border">Last Submission</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry) => (
              <tr key={entry.user_id} className="hover:bg-gray-50">
                <td className="px-4 py-2 border text-center font-bold">{entry.rank}</td>
                <td className="px-4 py-2 border">{entry.user_id}</td>
                <td className="px-4 py-2 border text-center">{entry.total_score.toFixed(2)}</td>
                <td className="px-4 py-2 border text-center">{entry.total_submissions}</td>
                <td className="px-4 py-2 border text-center">{entry.total_accepted}</td>
                <td className="px-4 py-2 border text-sm">
                  {entry.last_submission_at 
                    ? new Date(entry.last_submission_at).toLocaleString()
                    : 'N/A'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

