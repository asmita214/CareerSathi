import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { FiSearch, FiSun, FiGlobe, FiUser, FiMenu, FiX } from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchVal, setSearchVal] = useState('');

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="nav-inner">
        {/* Logo */}
        <NavLink to="/" className="nav-logo">
          <span className="logo-star">✦</span>
          <div>
            <div className="logo-name">CareerSaathi</div>
            <div className="logo-tagline">Explore · Learn · Grow</div>
          </div>
        </NavLink>

        {/* Center links */}
        <div className={`nav-links ${mobileOpen ? 'open' : ''}`}>
          {['/', '/explore', '/tools', '/resources', '/about'].map((path, i) => {
            const label = ['Home', 'Explore', 'Tools', 'Resources', 'About'][i];
            return (
              <NavLink
                key={path}
                to={path}
                end={path === '/'}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={() => setMobileOpen(false)}
              >
                {label}
              </NavLink>
            );
          })}
        </div>

        {/* Right actions */}
        <div className="nav-actions">
          <div className="lang-btn"><FiGlobe /><span>EN</span></div>
          <div className="search-pill">
            <FiSearch />
            <input
              placeholder="Search careers, skills, tools..."
              value={searchVal}
              onChange={e => setSearchVal(e.target.value)}
            />
          </div>
          <div className="avatar-btn"><FiUser /></div>
          <button className="mobile-toggle" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
