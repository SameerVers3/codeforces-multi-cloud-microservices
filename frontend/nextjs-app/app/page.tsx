'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Home() {
  const [contests, setContests] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchContests()
  }, [])

  const fetchContests = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_CONTEST_SERVICE_URL}/api/v1/contests/`)
      setContests(response.data)
    } catch (error) {
      console.error('Error fetching contests:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="container mx-auto p-4">Loading...</div>
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Contests</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {contests.map((contest: any) => (
          <div key={contest.id} className="border p-4 rounded-lg hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold">{contest.title}</h2>
            <p className="text-gray-600">{contest.description}</p>
            <p className="text-sm text-gray-500 mt-2">
              Starts: {new Date(contest.start_time).toLocaleString()}
            </p>
            <a
              href={`/contests/${contest.id}`}
              className="mt-4 inline-block text-blue-600 hover:text-blue-800"
            >
              View Details →
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}

