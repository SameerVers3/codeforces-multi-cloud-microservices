'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import axios from 'axios';
import CodeEditor from '@/components/CodeEditor';

export default function SubmitPage() {
  const params = useParams();
  const router = useRouter();
  const contestId = params.id as string;
  const [problemId, setProblemId] = useState('');
  const [code, setCode] = useState('#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}');
  const [problems, setProblems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProblems();
  }, [contestId]);

  const fetchProblems = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_CONTEST_SERVICE_URL}/api/v1/problems/contest/${contestId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setProblems(response.data);
      if (response.data.length > 0) {
        setProblemId(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching problems:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        `${process.env.NEXT_PUBLIC_SUBMISSION_SERVICE_URL}/api/v1/submissions/`,
        {
          contest_id: contestId,
          problem_id: problemId,
          code: code,
          language: 'cpp'
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      router.push(`/contests/${contestId}/submissions`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Submission failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Submit Solution</h1>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="problem" className="block text-sm font-medium text-gray-700 mb-2">
            Problem
          </label>
          <select
            id="problem"
            value={problemId}
            onChange={(e) => setProblemId(e.target.value)}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
            required
          >
            <option value="">Select a problem</option>
            {problems.map((problem) => (
              <option key={problem.id} value={problem.id}>
                {problem.title} ({problem.points} points)
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Code (C++)
          </label>
          <CodeEditor value={code} onChange={setCode} language="cpp" />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Submitting...' : 'Submit'}
        </button>
      </form>
    </div>
  );
}

