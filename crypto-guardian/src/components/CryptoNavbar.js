import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import styles from './styles/CryptoNavbar.module.css';
import logo from '../assets/logo.svg';

const CryptoNavbar = ({ activeSection, setActiveSection }) => {
  return (
    <Navbar expand="lg" fixed="top" className={styles.navbar}>
      <Container>
        <Navbar.Brand href="#" className={styles.brand}>
          <img
            src={logo}
            alt="CryptoGuardian Logo"
            className={styles.logo}
          />
          <span className={`${styles.brandText} ${styles.glowText}`}>CryptoGuardian</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link
              onClick={() => setActiveSection('ethereum')}
              className={`${styles.navLink} ${activeSection === 'ethereum' ? styles.activeLink : ''}`}
            >
              Ethereum Prediction
            </Nav.Link>
            <Nav.Link
              onClick={() => setActiveSection('tokenPriceTracker')}
              className={`${styles.navLink} ${activeSection === 'tokenPriceTracker' ? styles.activeLink : ''}`}
            >
              Token Price Tracker
            </Nav.Link>
            <Nav.Link
              onClick={() => setActiveSection('news')}
              className={`${styles.navLink} ${activeSection === 'news' ? styles.activeLink : ''}`}
            >
              Crypto News
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default CryptoNavbar;
