import React from "react";
import { Routes, Route, Outlet } from "react-router-dom";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import Logs from "./pages/Logs";

// ✅ Correct import with full extension for Docker/Vite
import DockerManagerTab from "./pages/DockerManagerTab.jsx";

import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      {/* Public route */}
      <Route path="/login" element={<Login />} />

      {/* Protected layout */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <div className="min-h-screen flex flex-col">
              <Navbar />
              <div className="flex flex-1">
                <Sidebar />
                <main className="flex-1 bg-slate-100 p-4">
                  <Outlet />
                </main>
              </div>
            </div>
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="alerts" element={<Alerts />} />
        <Route path="logs" element={<Logs />} />

        {/* System Control = Docker Manager */}
        <Route path="system" element={<DockerManagerTab />} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
