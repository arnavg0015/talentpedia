'use client';
import { useEffect, useState } from 'react';

type Competition = {
  id: number;
  title: string;
  category: string;
  location: string;
};

export default function Home() {
  const [competitions, setCompetitions] = useState<Competition[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/competitions')
      .then(res => res.json())
      .then(data => setCompetitions(data));
  }, []);

  return (
    <main className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Competition Finder</h1>
      <div className="space-y-4">
        {competitions.map(c => (
          <div key={c.id} className="border rounded-lg p-4">
            <h2 className="font-semibold text-lg">{c.title}</h2>
            <p className="text-gray-500">{c.category} · {c.location}</p>
          </div>
        ))}
      </div>
    </main>
  );
}