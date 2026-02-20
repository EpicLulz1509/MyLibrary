const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Helper function to normalize titles for better matching
function normalizeTitle(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s]/g, '') // Remove punctuation
    .replace(/\s+/g, ' ')     // Normalize whitespace
    .trim();
}

// Calculate similarity score between two strings (0 to 1)
function calculateSimilarity(str1, str2) {
  const longer = str1.length > str2.length ? str1 : str2;
  const shorter = str1.length > str2.length ? str2 : str1;

  if (longer.length === 0) return 1.0;

  // Check if one string contains the other
  if (longer.includes(shorter)) {
    return 0.9; // High similarity if one contains the other
  }

  // Token-based matching - split into words and compare
  const tokens1 = str1.split(' ');
  const tokens2 = str2.split(' ');
  const commonTokens = tokens1.filter(token => tokens2.includes(token));
  const tokenSimilarity = (2.0 * commonTokens.length) / (tokens1.length + tokens2.length);

  return tokenSimilarity;
}

function findMatchingBook(bookTitle, books) {
  const normalizedClippingTitle = normalizeTitle(bookTitle);

  // Try exact match first
  let book = books.find(b => normalizeTitle(b.title) === normalizedClippingTitle);

  if (book) return book;

  // Use fuzzy matching to find best match
  let bestMatch = null;
  let bestScore = 0;
  const threshold = 0.6; // Minimum similarity threshold

  for (const b of books) {
    const normalizedBookTitle = normalizeTitle(b.title);
    const score = calculateSimilarity(normalizedClippingTitle, normalizedBookTitle);

    if (score > bestScore && score >= threshold) {
      bestScore = score;
      bestMatch = b;
    }
  }

  return bestMatch || {
    title: bookTitle,
    author: 'Unknown',
    cover_url: ''
  };
}

// API Routes
app.get('/api/books', (req, res) => {
  try {
    const books = JSON.parse(fs.readFileSync(path.join(__dirname, 'books.json'), 'utf8'));
    res.json(books);
  } catch (error) {
    res.status(500).json({ error: 'Failed to load books' });
  }
});

app.get('/api/quotes', (req, res) => {
  try {
    const quotes = JSON.parse(fs.readFileSync(path.join(__dirname, 'clippings.json'), 'utf8'));
    const books = JSON.parse(fs.readFileSync(path.join(__dirname, 'books.json'), 'utf8'));

    // Combine quotes with book information using improved matching
    const quotesWithBooks = Object.entries(quotes).map(([bookTitle, bookQuotes]) => {
      const book = findMatchingBook(bookTitle, books);

      return {
        ...book,
        quotes: bookQuotes
      };
    });

    res.json(quotesWithBooks);
  } catch (error) {
    res.status(500).json({ error: 'Failed to load quotes' });
  }
});

app.get('/api/reviews', (req, res) => {
  try {
    const reviewsPath = path.join(__dirname, 'reviews.json');
    if (fs.existsSync(reviewsPath)) {
      const reviews = JSON.parse(fs.readFileSync(reviewsPath, 'utf8'));
      res.json(reviews);
    } else {
      res.json([]);
    }
  } catch (error) {
    res.status(500).json({ error: 'Failed to load reviews' });
  }
});

app.get('/api/random-quote', (req, res) => {
  try {
    const clippingsPath = path.join(__dirname, 'clippings.json');

    // Check if clippings.json exists
    if (!fs.existsSync(clippingsPath)) {
      return res.status(404).json({ error: 'No quotes available' });
    }

    const quotes = JSON.parse(fs.readFileSync(clippingsPath, 'utf8'));
    const books = JSON.parse(fs.readFileSync(path.join(__dirname, 'books.json'), 'utf8'));

    // Flatten all quotes into a single array with book info
    const allQuotes = [];
    Object.entries(quotes).forEach(([bookTitle, bookQuotes]) => {
      // Find matching book for metadata using fuzzy matching
      const book = findMatchingBook(bookTitle, books);

      bookQuotes.forEach(quote => {
        allQuotes.push({
          quote: quote,
          book: book.title,
          author: book.author,
          cover_url: book.cover_url
        });
      });
    });

    if (allQuotes.length === 0) {
      return res.status(404).json({ error: 'No quotes available' });
    }

    // Select random quote
    const randomIndex = Math.floor(Math.random() * allQuotes.length);
    const randomQuote = allQuotes[randomIndex];

    res.json(randomQuote);
  } catch (error) {
    res.status(500).json({ error: 'Failed to load random quote' });
  }
});

// Serve static files from React app in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'client/build')));

  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
