/**
 * @file Search.jsx
 * Controlled search input displayed in the top bar. The parent (TopBar) owns
 * all state and handlers — this component is purely presentational.
 */

import { Box, InputBase, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

/**
 * Search bar with a text field and a clickable search icon button.
 *
 * @param {object} props
 * @param {string}   props.searchTerm          - Current value of the search input.
 * @param {function} props.onSearchTermChange  - Called on every keystroke to update the term.
 * @param {function} props.onKeyDown           - Called on keydown; the hook triggers search on Enter.
 * @param {function} props.onSearch            - Called when the search icon button is clicked.
 * @returns {JSX.Element} A styled input box with an icon button that submits the query.
 */
const Search = ({ searchTerm, onSearchTermChange, onKeyDown, onSearch }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        position: 'relative',
        borderRadius: 1,
        backgroundColor: 'rgba(0,0,0,0.04)',
        border: '1px solid transparent',
        '&:hover': {
          backgroundColor: '#ffffff',
          borderColor: 'primary.light',
          boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        },
        '&:focus-within': {
          backgroundColor: '#ffffff',
          borderColor: 'primary.main',
          boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        },
        mx: { xs: 0, sm: 3 },
        flexGrow: 1,
        maxWidth: 640,
        transition: 'background-color 0.2s, border-color 0.2s, box-shadow 0.2s',
      }}
    >
      <InputBase
        value={searchTerm}
        onChange={onSearchTermChange}
        placeholder="Search your files and folders"
        inputProps={{ 'aria-label': 'search' }}
        onKeyDown={onKeyDown}
        sx={{
          color: 'inherit',
          flexGrow: 1,
          '& .MuiInputBase-input': {
            py: 1.2,
            pl: 2,
            fontSize: '0.95rem',
          },
        }}
      />
      <IconButton onClick={onSearch} size="small" sx={{ mr: 0.5, color: 'text.secondary' }}>
        <SearchIcon fontSize="small" />
      </IconButton>
    </Box>
  );
};

export default Search;