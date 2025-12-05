'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import axios from 'axios';

interface Submission {
  id: string;
  problem_id: string;
  status: string;
  score: number;
  execution_time_ms: number | null;
  submitted_at: string;
}

export default function SubmissionsPage() {
  const params = useParams();
  const contestId = params.id as string;
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubmissions();
  }, [contestId]);

  const fetchSubmissions = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_SUBMISSION_SERVICE_URL}/api/v1/submissions/`,
        {
          params: { contest_id: contestId },
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setSubmissions(response.data);
    } catch (error) {
      console.error('Error fetching submissions:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      accepted: 'text-green-600',
      wrong_answer: 'text-red-600',
      time_limit_exceeded: 'text-yellow-600',
      runtime_error: 'text-orange-600',
      compilation_error: 'text-red-600',
      pending: 'text-gray-600',
      running: 'text-blue-600'
    };
    return colors[status] || 'text-gray-600';
  };

  if (loading) {
    return <div className="container mx-auto p-4">Loading submissions...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">My Submissions</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 border">ID</th>
              <th className="px-4 py-2 border">Problem</th>
              <th className="px-4 py-2 border">Status</th>
              <th className="px-4 py-2 border">Score</th>
              <th className="px-4 py-2 border">Time (ms)</th>
              <th className="px-4 py-2 border">Submitted</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((submission) => (
              <tr key={submission.id} className="hover:bg-gray-50">
                <td className="px-4 py-2 border text-sm">{submission.id.substring(0, 8)}</td>
                <td className="px-4 py-2 border">{submission.problem_id.substring(0, 8)}</td>
                <td className={`px-4 py-2 border font-medium ${getStatusColor(submission.status)}`}>
                  {submission.status.replace('_', ' ').toUpperCase()}
                </td>
                <td className="px-4 py-2 border">{submission.score.toFixed(2)}</td>
                <td className="px-4 py-2 border">{submission.execution_time_ms || 'N/A'}</td>
                <td className="px-4 py-2 border text-sm">
                  {new Date(submission.submitted_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

