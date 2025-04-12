import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import styles from './styles/EthereumChart.module.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const EthereumChart = () => {
  const [historicalData, setHistoricalData] = useState([]);
  const [predictionData, setPredictionData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const historicalResponse = await axios.get('https://api.binance.com/api/v3/klines', {
          params: {
            symbol: 'ETHUSDT',
            interval: '1d',
            limit: 7,
          },
        });

        if (!historicalResponse.data || !Array.isArray(historicalResponse.data)) {
          throw new Error('Invalid historical data format from Binance');
        }

        const formattedHistoricalData = historicalResponse.data.map(item => ({
          timestamp: new Date(item[0]).toISOString(),
          price: parseFloat(item[4]),
        }));

        setHistoricalData(formattedHistoricalData);

        try {
          const predictionResponse = await axios.get(`http://20.199.80.240:5020/predict`);
          setPredictionData(predictionResponse.data.predicted_close_prices);
        } catch {}

        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return <div className={styles.loadingContainer}>Loading price data...</div>;
  }

  if (error && !historicalData.length) {
    return <div className={styles.errorContainer}>{error}</div>;
  }

  if (!historicalData.length) {
    return <div className={styles.errorContainer}>No price data available</div>;
  }

  const lastHistoricalDate = new Date(historicalData[historicalData.length - 1].timestamp);
  const futureDates = Array.from({ length: 7 }, (_, i) => {
    const futureDate = new Date(lastHistoricalDate);
    futureDate.setDate(futureDate.getDate() + (i + 1));
    return futureDate.toLocaleDateString('en-US', { weekday: 'short' });
  });

  const chartLabels = [
    ...historicalData.map(d => new Date(d.timestamp).toLocaleDateString('en-US', { weekday: 'short' })),
    ...futureDates
  ];

  const historicalPrices = historicalData.map(d => d.price);
  const predictionPrices = predictionData;

  const chartData = {
    labels: chartLabels,
    datasets: [
      {
        label: 'Historical Price',
        data: [...historicalPrices, ...Array(predictionData.length).fill(null)],
        borderColor: '#64FFDA',
        backgroundColor: 'rgba(100, 255, 218, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'AI Prediction',
        data: [
          ...Array(historicalPrices.length - 1).fill(null),
          historicalPrices[historicalPrices.length - 1],
          ...predictionPrices
        ],
        borderColor: '#FF6B6B',
        backgroundColor: 'rgba(255, 107, 107, 0.1)',
        fill: true,
        tension: 0.4,
        borderDash: [5, 5],
      },
    ],
  };

  return (
    <div className={styles.chartWrapper}>
      <h2 className={styles.chartTitle}>
        <span className={styles.titleText}>Ethereum Price Prediction</span>
        <span className={styles.subtitleText}>AI-Powered Price Forecast</span>
      </h2>
      <div className={styles.chartContainer}>
        <Line options={{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { color: '#e0e0e0', font: { size: 12, family: "'Poppins', sans-serif" } } },
            tooltip: {
              titleColor: '#e0e0e0', bodyColor: '#e0e0e0', backgroundColor: 'rgba(26, 27, 30, 0.9)',
              callbacks: { label: (context) => `$${context.parsed.y.toFixed(2)}` },
            },
            title: { display: true, text: 'Ethereum Price Prediction', color: '#e0e0e0', font: { size: 16, weight: '600', family: "'Poppins', sans-serif" } },
          },
          scales: {
            x: { grid: { color: 'rgba(68, 68, 68, 0.5)', drawBorder: false }, ticks: { color: '#e0e0e0', maxRotation: 45, minRotation: 45, font: { size: 10, family: "'Poppins', sans-serif" } } },
            y: { grid: { color: 'rgba(68, 68, 68, 0.5)', drawBorder: false }, ticks: { color: '#e0e0e0', callback: (value) => `$${value.toFixed(2)}`, font: { size: 10, family: "'Poppins', sans-serif" } } },
          },
        }} data={chartData} />
        {predictionData?.metrics && (
          <div className={styles.metricsContainer}>
            <div className={styles.metric}><span>Model Accuracy:</span><span>{(predictionData.metrics.accuracy * 100).toFixed(2)}%</span></div>
            <div className={styles.metric}><span>Confidence Level:</span><span>{(predictionData.metrics.confidence * 100).toFixed(2)}%</span></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EthereumChart;
