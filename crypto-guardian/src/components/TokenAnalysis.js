import React, { useState } from 'react';
import { Card, Nav } from 'react-bootstrap';
import TokenPriceTracker from './TokenPriceTracker';
import EthereumChart from './EthereumChart';
import styles from './styles/TokenAnalysis.module.css';

const TokenAnalysis = () => {
  const [activeSection, setActiveSection] = useState('ethereum');

  return (
    <div className={styles.analysisContainer}>
      <Card className={styles.chartCard}>
        <Card.Header>
          <Nav variant="tabs" className={styles.navTabs}>
            <Nav.Item>
              <Nav.Link
                className={`${styles.navLink} ${activeSection === 'ethereum' ? styles.active : ''}`}
                onClick={() => setActiveSection('ethereum')}
              >
                Ethereum Prediction
              </Nav.Link>
            </Nav.Item>
            <Nav.Item>
              <Nav.Link
                className={`${styles.navLink} ${activeSection === 'tokens' ? styles.active : ''}`}
                onClick={() => setActiveSection('tokens')}
              >
                Token Tracker
              </Nav.Link>
            </Nav.Item>
          </Nav>
        </Card.Header>
        <Card.Body className={styles.chartBody}>
          {activeSection === 'ethereum' ? <EthereumChart /> : <TokenPriceTracker />}
        </Card.Body>
      </Card>
    </div>
  );
};

export default TokenAnalysis;
