import React, { useState, useEffect } from 'react';
import './Books.css';

function Books() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRating, setFilterRating] = useState('all');

  useEffect(() => {
    fetch('/api/books')
      .then(res => res.json())
      .then(data => {
        setBooks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading books:', err);
        setLoading(false);
      });
  }, []);

  const filteredBooks = books.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRating = filterRating === 'all' || book.user_rating === filterRating;
    return matchesSearch && matchesRating;
  });

  if (loading) {
    return <div className="loading">Loading your library...</div>;
  }

  return (
    <div className="books-page">
      <header className="page-header">
        <h1>My Book Collection</h1>
        <p className="book-count">{filteredBooks.length} books</p>
      </header>

      <div className="filters">
        <input
          type="text"
          placeholder="Search books or authors..."
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

      <div className="books-grid">
        {filteredBooks.map((book, index) => (
          <div key={index} className="book-card">
            <a href={book.url} target="_blank" rel="noopener noreferrer" className="book-cover-link">
              <img
                src={book.cover_url}
                alt={book.title}
                className="book-cover"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'https://via.placeholder.com/200x300?text=No+Cover';
                }}
              />
            </a>
            <div className="book-info">
              <h3 className="book-title">{book.title}</h3>
              <p className="book-author">by {book.author}</p>
              <div className="book-ratings">
                <div className="rating">
                  <span className="rating-label">My Rating:</span>
                  <span className="rating-value my-rating">{book.user_rating}</span>
                </div>
                <div className="rating">
                  <span className="rating-label">Avg:</span>
                  <span className="rating-value">{book.avg_rating}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredBooks.length === 0 && (
        <div className="no-results">
          <p>No books found matching your search.</p>
        </div>
      )}
    </div>
  );
}

export default Books;
