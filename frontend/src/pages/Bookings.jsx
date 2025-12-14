// frontend/src/pages/Bookings.jsx
import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useWallet } from "../context/WalletContext.jsx";

export default function Bookings() {
  const { user, fetchBookings } = useWallet();

  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  // -----------------------------------------
  // BLOCK ACCESS IF USER NOT LOGGED IN
  // -----------------------------------------
  if (!user) {
    return (
      <div className="p-10 text-center text-gray-600 text-lg">
        <h2 className="text-3xl font-bold text-primary mb-3">
          Booking History
        </h2>
        <p>You must login to view your previous bookings.</p>
      </div>
    );
  }

  // -----------------------------------------
  // Fetch Bookings From Backend
  // -----------------------------------------
  const loadBookings = async () => {
    try {
      const data = await fetchBookings(); // Calls GET /bookings?user_id=ID
      setBookings(data);
    } catch (err) {
      console.error("Failed to load bookings:", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadBookings();
  }, [user]);

  // -----------------------------------------
  // Download Ticket PDF
  // -----------------------------------------
  const handleDownload = (pnr) => {
    const url = `http://localhost:8000/bookings/ticket/${pnr}?user_id=${user.id}`;
    window.open(url, "_blank");
  };

  // -----------------------------------------
  // LOADING UI
  // -----------------------------------------
  if (loading) {
    return (
      <div className="p-10 text-center text-gray-500 text-lg">
        Loading your bookings...
      </div>
    );
  }

  // -----------------------------------------
  // IF NO BOOKINGS FOUND
  // -----------------------------------------
  if (bookings.length === 0) {
    return (
      <div className="p-10 text-center text-gray-600">
        <h2 className="text-3xl font-bold text-primary mb-3">
          Booking History
        </h2>
        <p>No previous bookings found.</p>
      </div>
    );
  }

  // -----------------------------------------
  // MAIN UI — SHOW BOOKINGS
  // -----------------------------------------
  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold text-primary mb-6 text-center">
        Your Previous Bookings
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {bookings.map((b, index) => {
          const f = b.flight;

          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white p-6 rounded-xl shadow-md border hover:shadow-xl transition"
            >
              {/* FLIGHT HEADER */}
              <h2 className="text-xl font-bold text-primary mb-2">
                {f.airline} — {f.flight_id}
              </h2>

              <p><strong>Passenger:</strong> {b.passenger_name}</p>
              <p><strong>PNR:</strong> {b.pnr}</p>

              <p>
                <strong>Route:</strong> {f.departure_city} → {f.arrival_city}
              </p>

              <p><strong>Price:</strong> ₹{b.final_price}</p>

              <p>
                <strong>Date:</strong>{" "}
                {new Date(b.booking_time).toLocaleString()}
              </p>

              {/* DOWNLOAD TICKET */}
              <button
                onClick={() => handleDownload(b.pnr)}
                className="mt-4 w-full bg-primary text-white py-2 rounded-lg hover:bg-blue-700"
              >
                Download Ticket
              </button>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
