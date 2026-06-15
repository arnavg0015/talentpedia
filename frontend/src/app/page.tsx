'use client';
import { useEffect, useState } from 'react';

type Competition = {
  id: number;
  title: string;
  category: string;
  city: string;
  state: string;
  event_date: string;
  url: string;
  is_virtual: boolean;
  age_min: number;
  age_max: number;
};

const CATEGORIES = ['All', 'STEM', 'Arts', 'Sports', 'Other'];

const CATEGORY_COLORS: Record<string, string> = {
  STEM: 'bg-blue-100 text-blue-800',
  Arts: 'bg-purple-100 text-purple-800',
  Sports: 'bg-green-100 text-green-800',
  Other: 'bg-gray-100 text-gray-800',
};

export default function Home() {
  const [competitions, setCompetitions] = useState<Competition[]>([]);
  const [activeCategory, setActiveCategory] = useState('All');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = activeCategory !== 'All' ? `?category=${activeCategory}` : '';
    fetch(`http://localhost:8000/competitions${params}`)
      .then(res => res.json())
      .then(data => { setCompetitions(data); setLoading(false); });
  }, [activeCategory]);

  return (
    <main className="max-w-3xl mx-auto p-8">
      <h1 className="text-4xl font-bold mb-2">Talentpedia</h1>
      <p className="text-gray-500 mb-8">Discover competitions near you</p>

      {/* Category filters */}
      <div className="flex gap-2 mb-8 flex-wrap">
        {CATEGORIES.map(cat => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors
              ${activeCategory === cat
                ? 'bg-black text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Competition cards */}
      {loading ? (
        <p className="text-gray-400">Loading competitions...</p>
      ) : competitions.length === 0 ? (
        <p className="text-gray-400">No competitions found.</p>
      ) : (
        <div className="space-y-4">
          {competitions.map(c => (
            <a key={c.id} href={c.url} target="_blank" rel="noopener noreferrer"
              className="block border rounded-xl p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="font-semibold text-lg mb-1">{c.title}</h2>
                  <p className="text-gray-500 text-sm">
                    {c.is_virtual ? 'Virtual' : `${c.city}, ${c.state}`}
                    {c.event_date && ` · ${c.event_date}`}
                    {c.age_min && ` · Ages ${c.age_min}–${c.age_max}`}
                  </p>
                </div>
                <span className={`text-xs font-medium px-2 py-1 rounded-full whitespace-nowrap
                  ${CATEGORY_COLORS[c.category] || CATEGORY_COLORS.Other}`}>
                  {c.category}
                </span>
              </div>
            </a>
          ))}
        </div>
      )}
    </main>
  );
}