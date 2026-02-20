import React, { useState, useEffect } from 'react';
import './Reviews.css';

function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRating, setFilterRating] = useState('all');

  useEffect(() => {
    fetch('/api/reviews')
      .then(res => res.json())
      .then(data => {
        setReviews(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading reviews:', err);
        setLoading(false);
      });
  }, []);

  const filteredReviews = reviews.filter(review => {
    const matchesSearch = review.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         review.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (review.review && review.review.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesRating = filterRating === 'all' || review.rating === filterRating;
    return matchesSearch && matchesRating;
  });

  if (loading) {
    return <div className="loading">Loading reviews...</div>;
  }

  if (reviews.length === 0) {
    return (
      <div className="reviews-page">
        <header className="page-header">
          <h1>My Book Reviews</h1>
        </header>
        <div className="no-reviews">
          <p>No reviews found. Run the scraper to fetch reviews from Goodreads!</p>
          <code className="command-hint">python scraping.py</code>
        </div>
      </div>
    );
  }

  return (
    <div className="reviews-page">
      <header className="page-header">
        <h1>My Book Reviews</h1>
        <p className="review-count">{filteredReviews.length} reviews</p>
      </header>

      <div className="filters">
        <input
          type="text"
          placeholder="Search reviews, books, or authors..."
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select
          className="rating-filter"
          value={filterRating}
          onChange={(e) => setFilterRating(e.target.value)}
        >
          <option value="all">All Ratings</option>
          <option value="5/5">⭐⭐⭐⭐⭐ (5/5)</option>
          <option value="4/5">⭐⭐⭐⭐ (4/5)</option>
          <option value="3/5">⭐⭐⭐ (3/5)</option>
          <option value="2/5">⭐⭐ (2/5)</option>
          <option value="1/5">⭐ (1/5)</option>
        </select>
      </div>

      <div className="reviews-container">
        {filteredReviews.map((review, index) => (
          <div key={index} className="review-card">
            <div className="review-header">
              {review.cover_url && (
                <a href={review.url} target="_blank" rel="noopener noreferrer">
                  <img
                    src={review.cover_url}
                    alt={review.title}
                    className="review-cover"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = 'https://via.placeholder.com/120x180?text=No+Cover';
                    }}
                  />
                </a>
              )}
              <div className="review-header-info">
                <h2 className="review-title">
                  <a href={review.url} target="_blank" rel="noopener noreferrer">
                    {review.title}
                  </a>
                </h2>
                <p className="review-author">by {review.author}</p>
                <div className="review-rating">
                  <span className="rating-label">My Rating:</span>
                  <span className="rating-value">{review.rating}</span>
                </div>
              </div>
            </div>

            {review.review && (
              <div className="review-content">
                <div
                  className="review-text"
                  dangerouslySetInnerHTML={{
                    __html: review.review
                      .replace(/<br\/>/g, '<br/>')
                      .replace(/\n/g, '<br/>')
                  }}
                />
              </div>
            )}
          </div>
        ))}
      </div>

      {filteredReviews.length === 0 && (
        <div className="no-results">
          <p>No reviews found matching your search.</p>
        </div>
      )}
    </div>
  );
}

export default Reviews;
