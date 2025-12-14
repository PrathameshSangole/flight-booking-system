// frontend/src/components/SearchBar.jsx
import React from "react";
import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [departure, setDeparture] = useState("");
  const [arrival, setArrival] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // send backend-friendly keys
    onSearch({ departure_city: departure.trim(), arrival_city: arrival.trim() });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 shadow-lg rounded-xl border border-gray-100 mb-6 animate-slideUp"
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <label className="block">
          <div className="text-xs text-gray-500 mb-1">Departure</div>
          <input
            type="text"
            value={departure}
            placeholder="Mumbai"
            onChange={(e) => setDeparture(e.target.value)}
            className="border p-3 rounded-lg focus:ring-2 focus:ring-primary w-full"
          />
        </label>

        <label className="block">
          <div className="text-xs text-gray-500 mb-1">Arrival</div>
          <input
            type="text"
            value={arrival}
            placeholder="Delhi"
            onChange={(e) => setArrival(e.target.value)}
            className="border p-3 rounded-lg focus:ring-2 focus:ring-primary w-full"
          />
        </label>

        <div>
          <button
            type="submit"
            className="w-full bg-primary text-white rounded-lg px-5 py-3 hover:bg-blue-700 transition text-lg font-medium"
          >
            Search Flights
          </button>
        </div>
      </div>
    </form>
  );
}
