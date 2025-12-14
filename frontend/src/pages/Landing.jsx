import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import FlightCard from "../components/FlightCard.jsx";

/**
 * Landing.jsx
 * A full landing / home page that shows hero, features, flight cards and CTA.
 * It expects `flights` prop (array) OR will fetch minimal featured dataset itself.
 *
 * Usage:
 * - Import in App.jsx route: <Route path="/" element={<Landing flights={flights} />} />
 * - Or call without flights prop and it will show demo cards.
 */

const palette = {
  primary: "bg-[#0f72f6]",
  primaryText: "text-[#0f72f6]",
  accent: "bg-gradient-to-r from-[#0f72f6] to-[#0b4ca3]",
};

const demoFlights = [
  { flight_id: "AI-101", airline: "Air India", base_price: 2300.58, price: 2300.58, departure_city: "Mumbai", arrival_city: "Delhi" },
  { flight_id: "6E-303", airline: "IndiGo", base_price: 2520.96, price: 2520.96, departure_city: "Mumbai", arrival_city: "Bengaluru" },
  { flight_id: "UK-505", airline: "Vistara", base_price: 2059.01, price: 2059.01, departure_city: "Hyderabad", arrival_city: "Delhi" }
];

function Feature({ title, desc, icon }) {
  return (
    <motion.div whileHover={{ y: -6 }} className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-lg bg-primary flex items-center justify-center text-white text-xl">{icon}</div>
        <div>
          <div className="font-semibold">{title}</div>
          <div className="text-sm text-gray-500 mt-1">{desc}</div>
        </div>
      </div>
    </motion.div>
  );
}

export default function Landing({ flights = demoFlights }) {
  return (
    <main className="min-h-screen bg-gradient-to-b from-white to-slate-50">
      {/* Hero */}
      <section className="pt-16 pb-10 max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 }}
              className="text-4xl md:text-5xl font-extrabold leading-tight"
            >
              Smart flight booking — fast, fair pricing, instant tickets.
            </motion.h1>

            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.12 }} className="mt-4 text-gray-600 max-w-xl">
              Search flights across major Indian airlines, see surge indicators, pay from your in-app wallet, and download secure PDF tickets instantly.
            </motion.p>

            <div className="mt-6 flex flex-col sm:flex-row gap-3">
              <Link to="/search" className={`inline-flex items-center gap-3 px-6 py-3 rounded-lg text-white font-medium ${palette.primary}`}>
                Book a Flight
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none"><path d="M5 12h14" stroke="white" strokeWidth="2" strokeLinecap="round"/><path d="M13 6l6 6-6 6" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
              </Link>

              <a href="#features" className="px-6 py-3 rounded-lg border border-gray-200 text-gray-700 inline-flex items-center justify-center">
                Learn more
              </a>
            </div>

            <div className="mt-6 flex flex-wrap gap-3 items-center text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <span className="inline-block w-3 h-3 rounded-full bg-green-400"></span> Secure payments
              </div>
              <div className="flex items-center gap-2">
                <span className="inline-block w-3 h-3 rounded-full bg-yellow-300"></span> Dynamic pricing
              </div>
              <div className="flex items-center gap-2">
                <span className="inline-block w-3 h-3 rounded-full bg-sky-300"></span> Instant PDF tickets
              </div>
            </div>
          </div>

          {/* Hero illustration + mini cards */}
          <div>
            <div className="p-6 rounded-2xl bg-white shadow-lg border border-gray-100">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-xs text-gray-500">Wallet</div>
                  <div className="text-xl font-semibold">₹50,000</div>
                </div>
                <div className="text-sm text-gray-500">Member • Demo</div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {flights.slice(0, 3).map((f) => (
                  <motion.div key={f.flight_id} whileHover={{ scale: 1.01 }} className="p-3 rounded-lg bg-slate-50 border border-slate-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-sm font-medium">{f.airline}</div>
                        <div className="text-xs text-gray-500">{f.departure_city} → {f.arrival_city}</div>
                      </div>
                      <div className="text-sm font-semibold">₹{Number(f.price).toFixed(2)}</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            <div className="mt-5 text-sm text-gray-500">Trusted by students & small businesses across India.</div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-12 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <h3 className="text-2xl font-semibold mb-6">Why choose us</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Feature
              icon="⚡"
              title="Fast search & results"
              desc="Lightning-fast flight search with DB-backed results and low-latency UI."
            />
            <Feature
              icon="📈"
              title="Smart pricing"
              desc="Surge indicators and dynamic pricing rules ensure fair fares during high demand."
            />
            <Feature
              icon="🧾"
              title="PDF tickets"
              desc="Download secure PDF tickets with PNR and booking metadata instantly."
            />
          </div>
        </div>
      </section>

      {/* Featured flights grid */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-semibold">Featured flights</h3>
            <a href="/search" className="text-sm text-primary">View all flights →</a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {flights.map((f) => (
              <motion.div key={f.flight_id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
                <FlightCard flight={f} onBookClick={() => { /* user navigates to search or booking modal */ window.location.href = "/search"; }} />
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-12 bg-gradient-to-r from-[#f8fafc] to-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="rounded-xl p-8 md:p-10 flex flex-col md:flex-row items-center justify-between bg-white shadow-card border border-gray-100">
            <div>
              <h4 className="text-xl font-semibold">Ready to book your next trip?</h4>
              <p className="text-gray-500 mt-1">Search flights now and get an instant ticket with secure payment and wallet support.</p>
            </div>

            <div className="mt-6 md:mt-0">
              <Link to="/search" className={`inline-flex items-center gap-3 px-6 py-3 rounded-lg text-white font-medium ${palette.primary}`}>
                Start searching
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-white border-t border-gray-100 mt-12">
        <div className="max-w-7xl mx-auto px-6 text-sm text-gray-500 flex flex-col md:flex-row justify-between items-center gap-4">
          <div>© {new Date().getFullYear()} Flight Booking System</div>
          <div className="flex gap-6">
            <a href="#" className="text-gray-500 hover:text-gray-700">Privacy</a>
            <a href="#" className="text-gray-500 hover:text-gray-700">Terms</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
