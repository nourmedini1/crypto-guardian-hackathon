import React, { useState, useEffect } from 'react';
import { Form } from 'react-bootstrap';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import styles from './styles/TokenPriceTracker.module.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const MAX_DATA_POINTS = 30;

const TokenPriceTracker = () => {
  const [selectedToken, setSelectedToken] = useState('SHIBUSDT');
  const [currentPrice, setCurrentPrice] = useState(null);
  const [priceChange, setPriceChange] = useState(0);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const tokens = [
    { symbol: 'SHIBUSDT', name: 'Shiba Inu (SHIB)', category: 'Meme' },
    { symbol: 'DOGEUSDT', name: 'Dogecoin (DOGE)', category: 'Meme' },
    { symbol: 'PEPEUSDT', name: 'Pepe (PEPE)', category: 'Meme' },
    { symbol: 'FLOKIUSDT', name: 'Floki (FLOKI)', category: 'Meme' },
    { symbol: 'LINKUSDT', name: 'Chainlink (LINK)', category: 'ERC-20' },
    { symbol: 'UNIUSDT', name: 'Uniswap (UNI)', category: 'ERC-20' },
    { symbol: 'AAVEUSDT', name: 'Aave (AAVE)', category: 'ERC-20' },
    { symbol: 'MKRUSDT', name: 'Maker (MKR)', category: 'ERC-20' },
    { symbol: 'SNXUSDT', name: 'Synthetix (SNX)', category: 'ERC-20' },
    { symbol: 'COMPUSDT', name: 'Compound (COMP)', category: 'ERC-20' }
  ];

  const updatePrice = async () => {
    try {
      const [priceResponse, changeResponse] = await Promise.all([
        axios.get('https://api.binance.com/api/v3/ticker/price', {
          params: { symbol: selectedToken }
        }),
        axios.get('https://api.binance.com/api/v3/ticker/24hr', {
          params: { symbol: selectedToken }
        })
      ]);

      const newPrice = parseFloat(priceResponse.data.price);
      setCurrentPrice(newPrice);
      setPriceChange(parseFloat(changeResponse.data.priceChangePercent));

      setChartData(prevData => {
        if (!prevData) return null;

        const newLabels = [...prevData.labels.slice(1), 
          new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
        ];
        const newPrices = [...prevData.datasets[0].data.slice(1), newPrice];

        return {
          labels: newLabels,
          datasets: [{
            ...prevData.datasets[0],
            data: newPrices,
          }]
        };
      });

      return true;
    } catch (error) {
      console.error('Error updating price:', error);
      return false;
    }
  };

  useEffect(() => {
    let timeoutId;

    const fetchInitialData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [klineResponse, priceResponse] = await Promise.all([
          axios.get('https://api.binance.com/api/v3/klines', {
            params: {
              symbol: selectedToken,
              interval: '1m',
              limit: MAX_DATA_POINTS,
            }
          }),
          axios.get('https://api.binance.com/api/v3/ticker/24hr', {
            params: { symbol: selectedToken }
          })
        ]);

        const formattedData = klineResponse.data.map(item => ({
          timestamp: new Date(item[0]),
          price: parseFloat(item[4]),
        }));

        setCurrentPrice(parseFloat(priceResponse.data.lastPrice));
        setPriceChange(parseFloat(priceResponse.data.priceChangePercent));

        setChartData({
          labels: formattedData.map(item => 
            item.timestamp.toLocaleTimeString('en-US', { 
              hour: '2-digit',
              minute: '2-digit'
            })
          ),
          datasets: [{
            label: 'Price',
            data: formattedData.map(item => item.price),
            fill: true,
            backgroundColor: 'rgba(100, 255, 218, 0.1)',
            borderColor: '#64FFDA',
            borderWidth: 2,
            pointRadius: 1,
            pointHoverRadius: 5,
            tension: 0.4,
          }]
        });

        setLoading(false);

        // Start updating prices
        const update = async () => {
          const success = await updatePrice();
          timeoutId = setTimeout(update, success ? 2000 : 5000); // Retry more slowly on failure
        };
        
        update();
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load price data');
        setLoading(false);
      }
    };

    fetchInitialData();

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [selectedToken]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 0
    },
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: tokens.find(t => t.symbol === selectedToken)?.name || selectedToken,
        color: '#e0e0e0',
        font: { size: 16, weight: '600' }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        titleColor: '#e0e0e0',
        bodyColor: '#e0e0e0',
        backgroundColor: 'rgba(26, 27, 30, 0.9)',
        callbacks: {
          label: (context) => `$${context.parsed.y.toFixed(8)}`,
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#e0e0e0',
          maxRotation: 45,
          minRotation: 45,
          font: { size: 10 }
        }
      },
      y: {
        position: 'right',
        grid: {
          color: 'rgba(68, 68, 68, 0.5)',
        },
        ticks: {
          color: '#e0e0e0',
          callback: (value) => `$${value.toFixed(8)}`,
          font: { size: 10 }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    }
  };

  return (
    <div className={styles.trackerContainer}>
      <div className={styles.trackerHeader}>
        <div className={styles.priceInfo}>
          <h3>Token Price Tracker</h3>
          {currentPrice && (
            <div className={styles.currentPrice}>
              <span className={styles.price}>${currentPrice.toFixed(8)}</span>
              <span className={`${styles.change} ${priceChange >= 0 ? styles.positive : styles.negative}`}>
                {priceChange >= 0 ? '+' : ''}{priceChange.toFixed(2)}%
              </span>
            </div>
          )}
        </div>
        <Form.Group className={styles.selectGroup}>
          <Form.Label>Select Token</Form.Label>
          <select
            value={selectedToken}
            onChange={(e) => setSelectedToken(e.target.value)}
            className={styles.tokenSelect}
          >
            <optgroup label="Meme Coins">
              {tokens
                .filter(token => token.category === 'Meme')
                .map(token => (
                  <option key={token.symbol} value={token.symbol}>
                    {token.name}
                  </option>
                ))
              }
            </optgroup>
            <optgroup label="ERC-20 Tokens">
              {tokens
                .filter(token => token.category === 'ERC-20')
                .map(token => (
                  <option key={token.symbol} value={token.symbol}>
                    {token.name}
                  </option>
                ))
              }
            </optgroup>
          </select>
        </Form.Group>
      </div>
      <div className={styles.chartContainer}>
        {loading ? (
          <div className={styles.loadingMessage}>Loading price data...</div>
        ) : error ? (
          <div className={styles.errorMessage}>{error}</div>
        ) : chartData && (
          <Line data={chartData} options={options} />
        )}
      </div>
    </div>
  );
};

export default TokenPriceTracker;