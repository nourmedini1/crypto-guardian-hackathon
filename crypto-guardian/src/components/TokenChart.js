import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import styles from './styles/TokenChart.module.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
);

const TokenChart = ({ symbol, name }) => {
  const [priceData, setPriceData] = useState({
    labels: [],
    prices: [],
    predictions: [],
    predictionLabels: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrices = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get('https://api.binance.com/api/v3/klines', {
          params: {
            symbol: symbol,
            interval: '1d',
            limit: 7,
          },
        });

        const formattedData = response.data.map(item => ({
          timestamp: new Date(item[0]),
          price: parseFloat(item[4]),
        }));

        // Generate next 3 days for predictions
        let mockPredictions = [null, null, null];
        
        if (formattedData.length >= 2) {
          const lastPrice = formattedData[formattedData.length - 1].price;
          const priceChange = formattedData[formattedData.length - 1].price - formattedData[formattedData.length - 2].price;
          const volatility = 0.02;

          mockPredictions = Array(3).fill(null).map((_, index) => {
            const trend = priceChange * (1 + index * 0.5);
            const noise = lastPrice * volatility * (Math.random() * 2 - 1);
            return lastPrice + trend + noise;
          });
        }

        const lastDate = formattedData[formattedData.length - 1].timestamp;
        const futureDates = Array.from({ length: 3 }, (_, i) => {
          const date = new Date(lastDate);
          date.setDate(date.getDate() + i + 1);
          return date;
        });

        setPriceData({
          labels: formattedData.map(item => 
            item.timestamp.toLocaleDateString('en-US', { weekday: 'short' })
          ),
          prices: formattedData.map(item => item.price),
          predictions: mockPredictions,
          predictionLabels: futureDates.map(date =>
            date.toLocaleDateString('en-US', { weekday: 'short' })
          ),
        });
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch price data');
        setLoading(false);
      }
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 300000); // Update every 5 minutes
    return () => clearInterval(interval);
  }, [symbol]);

  const data = {
    labels: priceData.labels,
    datasets: [
      {
        label: 'Historical Price',
        data: priceData.prices,
        fill: true,
        backgroundColor: 'rgba(100, 255, 218, 0.1)',
        borderColor: '#64FFDA',
        borderWidth: 2,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#64FFDA',
        tension: 0.4,
      },
      {
        label: 'Price Prediction',
        data: priceData.prices.length > 0 ? [
          ...Array(priceData.prices.length - 1).fill(null),
          priceData.prices[priceData.prices.length - 1],
          ...priceData.predictions
        ] : [],
        fill: false,
        borderColor: '#FF8C00',
        borderWidth: 2,
        borderDash: [5, 5],
        pointBackgroundColor: '#fff',
        pointBorderColor: '#FF8C00',
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index',
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#e0e0e0',
        },
      },
      tooltip: {
        enabled: true,
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => `$${context.parsed.y.toFixed(2)}`,
        },
      },
      title: {
        display: true,
        text: 'Ethereum Price & 3-Day Prediction',
        color: '#e0e0e0',
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#e0e0e0',
        },
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#e0e0e0',
          callback: (value) => `$${value.toFixed(2)}`,
        },
      },
    },
  };

  if (loading) {
    return (
      <div className={styles.chartContainer}>
        <div className={styles.loadingMessage}>Loading price data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.chartContainer}>
        <div className={styles.errorMessage}>{error}</div>
      </div>
    );
  }

  return (
    <div className={styles.chartWrapper}>
      <div className={styles.chartContainer}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default TokenChart;
