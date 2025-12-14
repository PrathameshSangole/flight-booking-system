// frontend/src/components/FlightCard.jsx
import React from "react";
import { motion } from "framer-motion";

export default function FlightCard({ flight, onBookClick }) {
  if (!flight) return null;

  const airline = flight.airline || "Unknown Airline";
  const flightId = flight.flight_id || flight.id || "N/A";
  const price = flight.price || flight.base_price || 0;
  const basePrice = flight.base_price || price;
  const departure = flight.departure_city || flight.from || "Unknown";
  const arrival = flight.arrival_city || flight.to || "Unknown";

  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-white shadow-card rounded-xl p-5 border border-gray-100 
                 hover:shadow-xl hover:scale-[1.02] cursor-pointer transition-transform"
    >
      <div className="flex justify-between items-center">
        {/* Airline & ID */}
        <div>
          <h2 className="text-xl font-semibold text-primary">{airline}</h2>
          <p className="text-gray-600 text-sm">Flight ID: {flightId}</p>
        </div>

      {/* Pricing */}
        <div className="text-right">
          <p className="text-2xl font-bold text-secondary">₹{price}</p>
          <p className="text-sm text-gray-500">Base: ₹{basePrice}</p>
        </div>
      </div>

      {/* Route */}
      <div className="my-4 flex items-center justify-between">
        <div className="text-gray-700 font-medium">{departure}</div>
        <div className="text-gray-500">→</div>
        <div className="text-gray-700 font-medium">{arrival}</div>
      </div>

      {/* Booking Button */}
      <button
        onClick={() => onBookClick(flight)}
        className="w-full bg-primary text-white py-2 rounded-lg hover:bg-blue-700 
                   transition shadow-md font-medium"
      >
        Book Now
      </button>
    </motion.div>
  );
}
