import { Box, InputBase, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

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