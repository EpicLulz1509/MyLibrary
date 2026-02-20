import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          My Library
        </Link>

        <button
          className="mobile-menu-icon"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? 'X' : '≡'}
        </button>

        <ul className={`nav-menu ${mobileMenuOpen ? 'active' : ''}`}>
          <li className="nav-item">
            <Link
              to="/"
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Books
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/quotes"
              className={`nav-link ${isActive('/quotes') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Quotes
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/reviews"
              className={`nav-link ${isActive('/reviews') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              Reviews
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
