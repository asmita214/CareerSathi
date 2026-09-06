import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Explore from './pages/Explore';
import Tools from './pages/Tools';
import Resources from './pages/Resources';
import About from './pages/About';
import './index.css';

export default function App() {
  return (
    <Router>
      <Navbar />
      <main>
        <Routes>
          <Route path="/"          element={<Home />} />
          <Route path="/explore"   element={<Explore />} />
          <Route path="/tools"     element={<Tools />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/about"     element={<About />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
}
