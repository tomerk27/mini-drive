import { memo } from 'react';
import './searchBar.css';
import SearchIcon from '../../../assets/icons/searchIcon';

const SearchBar = memo(() => {
  	return(
    	<form className="search-form">
    	  	<label htmlFor="search" className="sr-only">
    	    	Search
    	  	</label>
    	  	<div className="search-wrapper">
    	  	  <div className="search-icon">
    	  	    <SearchIcon />
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