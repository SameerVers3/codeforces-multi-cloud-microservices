'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function CreateContestPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    start_time: '',
    end_time: '',
    duration_minutes: '',
    max_participants: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Please login first');
        router.push('/login');
        return;
      }

      // Calculate duration if not provided
      let duration = parseInt(formData.duration_minutes);
      if (!duration && formData.start_time && formData.end_time) {
        const start = new Date(formData.start_time);
        const end = new Date(formData.end_time);
        duration = Math.round((end.getTime() - start.getTime()) / (1000 * 60));
      }

      const payload = {
        title: formData.title,
        description: formData.description || null,
        start_time: formData.start_time,
        end_time: formData.end_time,
        duration_minutes: duration,
        max_participants: formData.max_participants ? parseInt(formData.max_participants) : null
      };

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_CONTEST_SERVICE_URL}/api/v1/contests/`,
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      router.push(`/contests/${response.data.id}`);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError('You need staff privileges to create contests. Please contact an administrator.');
      } else if (err.response?.status === 401) {
        setError('Please login first');
        router.push('/login');
      } else {
        setError(err.response?.data?.detail || 'Failed to create contest');
      }
    } finally {
      setLoading(false);
    }
  };

  // Set default times (1 hour from now, 3 hours duration)
  const getDefaultStartTime = () => {
    const now = new Date();
    now.setHours(now.getHours() + 1);
    return now.toISOString().slice(0, 16);
  };

  const getDefaultEndTime = () => {
    const now = new Date();
    now.setHours(now.getHours() + 4);
    return now.toISOString().slice(0, 16);
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Create Contest</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Title *
          </label>
          <input
            id="title"
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="e.g., Weekly Contest #1"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            id="description"
            rows={4}
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Contest description..."
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 mb-2">
              Start Time *
            </label>
            <input
              id="start_time"
              type="datetime-local"
              required
              value={formData.start_time || getDefaultStartTime()}
              onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label htmlFor="end_time" className="block text-sm font-medium text-gray-700 mb-2">
              End Time *
            </label>
            <input
              id="end_time"
              type="datetime-local"
              required
              value={formData.end_time || getDefaultEndTime()}
              onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="duration_minutes" className="block text-sm font-medium text-gray-700 mb-2">
              Duration (minutes) *
            </label>
            <input
              id="duration_minutes"
              type="number"
              required
              min="1"
              value={formData.duration_minutes}
              onChange={(e) => setFormData({ ...formData, duration_minutes: e.target.value })}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="180"
            />
          </div>

          <div>
            <label htmlFor="max_participants" className="block text-sm font-medium text-gray-700 mb-2">
              Max Participants (optional)
            </label>
            <input
              id="max_participants"
              type="number"
              min="1"
              value={formData.max_participants}
              onChange={(e) => setFormData({ ...formData, max_participants: e.target.value })}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Unlimited"
            />
          </div>
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating...' : 'Create Contest'}
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="px-6 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

