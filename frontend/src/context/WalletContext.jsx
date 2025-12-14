// frontend/src/context/WalletContext.jsx

import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const WalletContext = createContext(null);

export function WalletProvider({ children }) {
  const API = "http://localhost:8000";

  // ============================================================
  // LOAD USER FROM LOCAL STORAGE (Fix logout on navigation)
  // ============================================================
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  // sync user to localStorage whenever it changes
  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);


  // ============================================================
  // AUTHENTICATION
  // ============================================================

  const login = async (email, password) => {
    try {
      const res = await axios.post(`${API}/users/login`, { email, password });

      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data)); // persist login

      return res.data;
    } catch (err) {
      console.error("Login error:", err);
      throw new Error(err.response?.data?.detail || "Login failed");
    }
  };


  const registerUser = async (payload) => {
    try {
      const res = await axios.post(`${API}/users/register`, payload);

      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data)); // persist

      return res.data;
    } catch (err) {
      console.error("Registration error:", err);
      throw new Error(err.response?.data?.detail || "Registration failed");
    }
  };


  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };


  // ============================================================
  // WALLET FUNCTIONS
  // ============================================================

  const refreshWallet = async () => {
    if (!user) return;

    try {
      const res = await axios.get(`${API}/users/${user.id}`);
      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data)); // update storage
    } catch (err) {
      console.error("Refresh wallet error:", err);
    }
  };


  const topUpWallet = async (amount) => {
    if (!user) throw new Error("Login required");

    try {
      await axios.post(`${API}/users/${user.id}/topup?amount=${amount}`);
      await refreshWallet();
    } catch (err) {
      console.error("Top-up error:", err);
      throw new Error(err.response?.data?.detail || "Top-up failed");
    }
  };


  // ============================================================
  // BOOKINGS
  // ============================================================

  const bookFlight = async ({ passenger_name, flight_id }) => {
    if (!user) throw new Error("Login required");

    try {
      const res = await axios.post(`${API}/bookings`, {
        passenger_name,
        flight_id,
        user_id: user.id,
      });

      await refreshWallet(); // wallet reduces
      return res.data;
    } catch (err) {
      console.error("Booking error:", err);
      throw new Error(err.response?.data?.detail || "Booking failed");
    }
  };


  const fetchBookings = async () => {
    if (!user) throw new Error("Login required");

    try {
      const res = await axios.get(`${API}/bookings?user_id=${user.id}`);
      return res.data;
    } catch (err) {
      console.error("Fetch bookings error:", err);
      throw new Error("Unable to load bookings");
    }
  };


  // ============================================================
  // CONTEXT EXPORT
  // ============================================================

  const value = {
    user,
    wallet: user?.wallet_balance || 0,

    login,
    registerUser,
    logout,

    refreshWallet,
    topUpWallet,

    bookFlight,
    fetchBookings,
  };

  return (
    <WalletContext.Provider value={value}>
      {children}
    </WalletContext.Provider>
  );
}


// Hook
export function useWallet() {
  const ctx = useContext(WalletContext);
  if (!ctx) {
    throw new Error("useWallet must be used inside <WalletProvider>");
  }
  return ctx;
}
