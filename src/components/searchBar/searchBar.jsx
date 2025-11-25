import { memo } from 'react';
import './searchBar.css';

const SearchBar = memo(() => {
    return(
<form className="search-form">
      <label htmlFor="search" className="sr-only">
        Search
      </label>
      <div className="search-wrapper">
        <div className="search-icon">
          <svg
            className="icon"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth="2"
              d="m21 21-3.5-3.5M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
            />
          </svg>
        </div>
        <input
          type="search"
          id="search"
          className="search-input"
          placeholder="Search"
          required
        />
        <button type="button" className="search-button">
          Search
        </button>
      </div>
    </form>
    );
});

export default SearchBar