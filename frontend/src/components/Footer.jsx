import React from 'react';
import './Footer.css';

const Footer = () => (
  <footer className="footer">
    <div className="footer-inner">
      <div className="footer-brand">
        <span className="logo-star">✦</span>
        <div>
          <div className="footer-name">CareerSaathi</div>
          <div className="footer-tag">Explore · Learn · Grow</div>
        </div>
      </div>
      <div className="footer-links">
        {[['Product', ['Tools', 'Resources', 'About']], ['Support', ['Help Center', 'Contact Us', 'Feedback']], ['Legal', ['Privacy Policy', 'Terms of Service', 'Cookie Policy']]].map(([col, items]) => (
          <div key={col} className="fcol">
            <h4>{col}</h4>
            {items.map(item => <a key={item} href="#">{item}</a>)}
          </div>
        ))}
      </div>
    </div>
    <div className="footer-bottom">Made with ❤️ for dreamers everywhere. &nbsp;·&nbsp; CareerSaathi © 2024</div>
  </footer>
);

export default Footer;
