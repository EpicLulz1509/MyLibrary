# My Library

A modern, intuitive personal library application built with React and Node.js. Track your books, save favorite quotes, and keep your Goodreads reviews all in one place.

## Features

- **Books Page**: Browse your entire book collection with search and filter capabilities
- **Quotes Page**: View all your favorite quotes organized by book
- **Reviews Page**: Read your Goodreads reviews in a clean, organized interface
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile devices
- **Modern UI**: Smooth animations and intuitive navigation

## Tech Stack

- **Frontend**: React with React Router
- **Backend**: Node.js with Express
- **Data Source**: Goodreads (scraped data)
- **Styling**: Custom CSS with responsive design

## Installation

### Prerequisites

- Node.js (v14 or higher)
- Python 3 (for scraping)
- npm or yarn

### Setup

1. **Install Backend Dependencies**

```bash
npm install
```

2. **Install Frontend Dependencies**

```bash
cd client
npm install
cd ..
```

3. **Install Python Dependencies** (for scraping)

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

#### Development Mode (recommended)

Run both backend and frontend with hot-reload:

```bash
npm run dev:full
```

Or run them separately:

```bash
# Terminal 1 - Backend
npm run dev

# Terminal 2 - Frontend
npm run client
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

#### Production Mode

1. Build the React app:
```bash
npm run build
```

2. Start the server:
```bash
npm start
```

Visit http://localhost:5000

### Updating Your Data

#### Quick Refresh (Recommended)

Update everything with a single command:

```bash
python refresh_data.py
```

This will automatically:
- Update books and ratings from Goodreads export (if `goodreads_library_export.csv` exists)
- Process Kindle clippings for quotes (if `My Clippings.txt` exists)
- Match quotes with correct authors using fuzzy matching

**Preparation:**
1. **For books/reviews:** Export from https://www.goodreads.com/review/import and save as `goodreads_library_export.csv`
2. **For quotes:** Copy `My Clippings.txt` from your Kindle to the project folder

Then run `python refresh_data.py` and restart your server!

#### Manual Update (Alternative)

If you prefer to run steps individually:

**Books and Reviews:**
```bash
python convert_csv.py
```

**Quotes:**
```bash
python clippings.py
```

**Note**: Web scraping with `scraping.py` is no longer recommended due to Goodreads anti-scraping measures.

## Project Structure

```
MyLibrary/
├── client/                 # React frontend
│   ├── public/
│   └── src/
│       ├── components/    # Reusable components
│       ├── pages/        # Page components
│       └── App.js        # Main app component
├── server.js             # Express backend
├── scraping.py          # Goodreads scraper
├── clippings.py         # Kindle clippings processor
├── books.json           # Book data
├── clippings.json       # Quotes data
└── reviews.json         # Reviews data
```

## API Endpoints

- `GET /api/books` - Returns all books
- `GET /api/quotes` - Returns quotes organized by book
- `GET /api/reviews` - Returns all reviews

## Customization

### Changing Colors

Edit the gradient background in [client/src/index.css](client/src/index.css):

```css
body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Updating Goodreads User ID

In [scraping.py](scraping.py), update the user ID in the base URL:

```python
base_url = "https://www.goodreads.com/review/list/YOUR_USER_ID?shelf=read&page="
```

## Contributing

This is a personal project, but feel free to fork and customize for your own use!

## License

ISC

---

**Enjoy your personal library!**
