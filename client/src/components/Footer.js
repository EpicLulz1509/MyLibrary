import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-links">
          <a
            href="https://github.com/EpicLulz1509"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            GitHub
          </a>
          <span className="footer-separator">•</span>
          <a
            href="https://www.goodreads.com/user/show/33805951-epiclulz1509"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            Goodreads
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
