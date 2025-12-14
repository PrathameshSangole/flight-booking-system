import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useWallet } from "../context/WalletContext.jsx";

export default function Navbar() {
  const { user, wallet, logout } = useWallet();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handlePreviousBookings = () => {
    setOpen(false);
    if (user) {
      navigate("/bookings");     // FIXED: React Router navigation
    } else {
      navigate("/login");
    }
  };

  return (
    <nav className="bg-white shadow-md p-4 flex justify-between items-center">

      {/* LEFT: LOGO */}
      <Link to="/" className="text-2xl font-bold text-primary">
        Flight Booking
      </Link>

      {/* CENTER: ONLY HOME */}
      <div className="space-x-6 text-lg flex items-center">
        <Link to="/" className="hover:text-primary">Home</Link>
      </div>

      {/* RIGHT: USER PROFILE DROPDOWN */}
      <div className="relative">
        <button
          onClick={() => setOpen(!open)}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700"
        >
          User Profile
        </button>

        {open && (
          <div className="absolute right-0 mt-2 bg-white border shadow-lg rounded-lg w-56 z-50 py-2">

            {/* Wallet Balance */}
            {user && (
              <div className="px-4 py-2 text-gray-700 border-b text-sm">
                Wallet Balance: <strong>₹{wallet}</strong>
              </div>
            )}

            {/* Previous Bookings */}
            <div
              className="block px-4 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={handlePreviousBookings}
            >
              Previous Bookings
            </div>

            {/* Login / Logout */}
            {!user ? (
              <Link
                to="/login"
                className="block px-4 py-2 hover:bg-gray-100"
                onClick={() => setOpen(false)}
              >
                Login
              </Link>
            ) : (
              <button
                className="w-full text-left px-4 py-2 hover:bg-gray-100"
                onClick={() => {
                  logout();
                  setOpen(false);
                  navigate("/"); // redirect after logout
                }}
              >
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
