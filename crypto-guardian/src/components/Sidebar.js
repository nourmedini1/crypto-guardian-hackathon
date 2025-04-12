  import React, { useState, useEffect } from 'react';
import styles from './styles/Sidebar.module.css';

const Sidebar = () => {
  const [newsHeadlines, setNewsHeadlines] = useState([]);

  useEffect(() => {
    fetch("http://20.199.80.240:5030/news")
      .then((response) => response.json())
      .then((data) => {
        if (data && data.news) {
          // Process and sort news by date
          const processedNews = data.news
            .map(item => ({
              id: item.message_id,
              title: item.text.split("\n")[0].replace(/\*\*/g, "").trim(),
              date: new Date(item.timestamp)
            }))
            .sort((a, b) => b.date - a.date) // Sort by date, newest first
            .slice(0, 3); // Get only the latest 3 headlines

          setNewsHeadlines(processedNews);
        }
      })
      .catch((error) => console.error("Error fetching news:", error));
  }, []);

  const handleClick = (e) => {
    e.preventDefault();
  };

  return (
    <div className={styles.section}>
      <h5 className={styles.cardTitle}>News Headlines</h5>
      <ul className="list-unstyled m-0 p-0">
        {newsHeadlines.map((news) => (
          <li key={news.id} className={styles.newsItem}>
            <a 
              href="#" 
              className={styles.newsLink}
              onClick={handleClick}
              role="button"
            >
              <span className={styles.newsDate}>
                {news.date.toLocaleString('en-US', { 
                  month: 'short', 
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
              <p className={styles.newsTitle}>{news.title}</p>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
