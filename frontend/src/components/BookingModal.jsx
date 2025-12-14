// frontend/src/components/BookingModal.jsx
import React, { useState } from "react";

export default function BookingModal({ flight, onClose, onConfirm, loading }) {
  const [name, setName] = useState("");

  const handleConfirm = () => {
    if (!name.trim()) {
      alert("Enter passenger name");
      return;
    }
    onConfirm(name.trim());
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="relative z-10 w-full max-w-md bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-semibold mb-2">Confirm Booking</h3>
        <div className="text-sm text-gray-600 mb-4">
          {flight.airline} — {flight.flight_id ?? flight.id}
        </div>

        <div className="mb-4">
          <label className="block text-sm text-gray-600 mb-1">Passenger name</label>
          <input
            className="w-full border rounded-md p-3"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Rahul Sharma"
          />
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-gray-500">Final price</div>
            <div className="text-lg font-bold">₹{flight.price ?? flight.base_price}</div>
          </div>

          <div className="flex gap-3">
            <button
              className="px-4 py-2 rounded-md border"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              className="px-4 py-2 rounded-md bg-primary text-white"
              onClick={handleConfirm}
              disabled={loading}
            >
              {loading ? "Booking..." : "Confirm"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
