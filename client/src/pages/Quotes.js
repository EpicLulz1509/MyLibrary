import React, { useState, useEffect } from 'react';
import './Quotes.css';

function Quotes() {
  const [quotesData, setQuotesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetch('/api/quotes')
      .then(res => res.json())
      .then(data => {
        setQuotesData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading quotes:', err);
        setLoading(false);
      });
  }, []);

  const filteredQuotes = quotesData.filter(book => {
    const matchesSearch = book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         book.quotes.some(quote => quote.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesSearch;
  });

  if (loading) {
    return <div className="loading">Loading quotes...</div>;
  }

  return (
    <div className="quotes-page">
      <header className="page-header">
        <h1>My Favorite Quotes</h1>
        <p className="quote-count">
          {filteredQuotes.reduce((acc, book) => acc + book.quotes.length, 0)} quotes from {filteredQuotes.length} books
        </p>
      </header>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search quotes, books, or authors..."
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="quotes-container">
        {filteredQuotes.map((book, bookIndex) => (
          <div key={bookIndex} className="quote-book-section">
            <div className="book-header">
              {book.cover_url && (
                <img
                  src={book.cover_url}
                  alt={book.title}
                  className="book-thumbnail"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://via.placeholder.com/80x120?text=No+Cover';
                  }}
                />
              )}
              <div className="book-header-info">
                <h2 className="book-title">{book.title}</h2>
                <p className="book-author">by {book.author}</p>
              </div>
            </div>

            <div className="quotes-list">
              {book.quotes.map((quote, quoteIndex) => (
                <div key={quoteIndex} className="quote-item">
                  <p className="quote-text">"{quote}"</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {filteredQuotes.length === 0 && (
        <div className="no-results">
          <p>No quotes found matching your search.</p>
        </div>
      )}
    </div>
  );
}

export default Quotes;
