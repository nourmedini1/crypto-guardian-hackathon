import React from 'react';
import { Container } from 'react-bootstrap';
import styles from './styles/Footer.module.css';

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <Container>
        <p className={styles.text}>
          &copy; {new Date().getFullYear()} <span>CryptoGuardian</span>. All rights reserved.
        </p>
      </Container>
    </footer>
  );
};

export default Footer;
