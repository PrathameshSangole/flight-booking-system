// frontend/src/pages/Home.jsx
import React, { useEffect, useState } from "react";
import SearchBar from "../components/SearchBar.jsx";
import FlightCard from "../components/FlightCard.jsx";
import BookingModal from "../components/BookingModal.jsx";
import { useWallet } from "../context/WalletContext.jsx";
import axios from "axios";

export default function Home() {
  const [flights, setFlights] = useState([]);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [loadingBooking, setLoadingBooking] = useState(false);

  // NEW context API
  const { user, wallet, bookFlight, refreshWallet } = useWallet();

  // --------------------------------------------------------------------
  // FETCH FLIGHTS
  // --------------------------------------------------------------------
  const fetchFlights = async (filters = {}) => {
    try {
      const params = {
        ...(filters.departure_city ? { departure_city: filters.departure_city } : {}),
        ...(filters.arrival_city ? { arrival_city: filters.arrival_city } : {}),
      };

      const res = await axios.get("http://127.0.0.1:8000/flights", { params });
      setFlights(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching flights:", error);
      alert("Could not fetch flights. Check backend connection.");
    }
  };

  useEffect(() => {
    fetchFlights();
  }, []);

  // --------------------------------------------------------------------
  // BOOKING HANDLER
  // --------------------------------------------------------------------
  const handleBooking = async (passengerName) => {
    if (!passengerName) return alert("Please enter passenger name");
    if (!selectedFlight) return alert("No flight selected");

    if (!user) {
      alert("Please login before booking a flight.");
      return;
    }

    const finalPrice = selectedFlight.price ?? selectedFlight.base_price;

    if (Number(wallet) < Number(finalPrice)) {
      alert("Insufficient wallet balance!");
      return;
    }

    setLoadingBooking(true);

    try {
      // Using the new WalletContext API call
      const booking = await bookFlight({
        passenger_name: passengerName,
        flight_id: selectedFlight.id,
      });

      await refreshWallet();

      alert(`Booking successful! PNR: ${booking.pnr}`);

      // Auto-open ticket PDF
      const pdfUrl = `http://127.0.0.1:8000/bookings/ticket/${booking.pnr}?user_id=${user.id}`;
      window.open(pdfUrl, "_blank");

      setSelectedFlight(null);
    } catch (err) {
      console.error("Booking error:", err);
      const message =
        err?.response?.data?.detail ||
        err?.message ||
        "Booking failed";
      alert(`Booking failed: ${message}`);
    } finally {
      setLoadingBooking(false);
    }
  };

  // --------------------------------------------------------------------
  // RENDER UI
  // --------------------------------------------------------------------
  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <header className="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-primary">
            Search Flights
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Fast, responsive booking with surge pricing enabled.
          </p>
        </div>

        {/* Wallet Card */}
        <div className="bg-white border border-gray-200 rounded-lg px-4 py-2 shadow-sm">
          <div className="text-xs text-gray-500">Wallet Balance</div>
          <div className="text-lg font-semibold">
            ₹{Number(wallet).toLocaleString()}
          </div>
        </div>
      </header>

      {/* Search Bar */}
      <SearchBar onSearch={fetchFlights} />

      {/* Flights List */}
      <section className="mt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {flights.length === 0 ? (
            <div className="p-8 bg-white rounded-lg shadow text-center text-gray-500 col-span-full">
              No flights found. Try other cities.
            </div>
          ) : (
            flights.map((flight) => (
              <FlightCard
                key={flight.id}
                flight={flight}
                onBookClick={() => setSelectedFlight(flight)}
              />
            ))
          )}
        </div>
      </section>

      {/* Booking Modal */}
      {selectedFlight && (
        <BookingModal
          flight={selectedFlight}
          onClose={() => setSelectedFlight(null)}
          onConfirm={handleBooking}
          loading={loadingBooking}
        />
      )}
    </div>
  );
}
