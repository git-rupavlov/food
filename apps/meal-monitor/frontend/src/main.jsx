import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'

function App() {
  const [query, setQuery] = useState('')
  const [foods, setFoods] = useState([])

  async function searchFoods() {
    const response = await fetch(`http://localhost:8000/foods/search?q=${encodeURIComponent(query)}`)
    const data = await response.json()
    setFoods(data)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Meal Monitor</h1>

      <div style={{ display: 'flex', gap: '1rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search food"
        />

        <button onClick={searchFoods}>Search</button>
      </div>

      <ul>
        {foods.map((food) => (
          <li key={food.fdc_id}>
            {food.description} ({food.data_type})
          </li>
        ))}
      </ul>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
