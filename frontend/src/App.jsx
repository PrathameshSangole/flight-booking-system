import React, { useEffect, useState } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import axios from "axios";

import Home from "./pages/Home.jsx";
import Bookings from "./pages/Bookings.jsx";
import Landing from "./pages/Landing.jsx";
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";

import Navbar from "./components/Navbar.jsx";

export default function App() {
  const location = useLocation();
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(true);

  // ------------------------------------------------------
  // Fetch flights from backend
  // ------------------------------------------------------
  useEffect(() => {
    let mounted = true;

    async function loadFlights() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/flights");

        if (mounted && Array.isArray(res.data)) {
          setFlights(res.data);
        }
      } catch (err) {
        console.error("Failed to fetch flights:", err);
        if (mounted) setFlights([]);
      } finally {
        if (mounted) setLoading(false);
      }
    }

    loadFlights();
    return () => {
      mounted = false;
    };
  }, []);

  // ------------------------------------------------------
  // Loading screen
  // ------------------------------------------------------
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mb-4">
            <svg
              className="animate-spin mx-auto h-10 w-10 text-blue-700"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8H4z"
              ></path>
            </svg>
          </div>
          <div className="text-gray-600 text-lg">Loading flights…</div>
        </div>
      </div>
    );
  }

  // ------------------------------------------------------
  // Main App
  // ------------------------------------------------------
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Navbar />

      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -18 }}
          transition={{ duration: 0.35, ease: "easeOut" }}
        >
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<Landing flights={flights} />} />
            <Route path="/search" element={<Home />} />
            <Route path="/bookings" element={<Bookings />} />

            {/* Authentication pages */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Fallback → home */}
            <Route path="*" element={<Landing flights={flights} />} />
          </Routes>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
