import { Box, InputBase } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const Search = ({ searchTerm, onSearchTermChange, onKeyDown }) => {
  return (
    <Box
      sx={{
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
      <Box
        sx={{
          px: 2,
          height: '100%',
          position: 'absolute',
          pointerEvents: 'none',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'text.secondary',
        }}
      >
        <SearchIcon fontSize="small" />
      </Box>
      <InputBase
        value={searchTerm}
        onChange={onSearchTermChange}
        placeholder="Search your files and folders"
        inputProps={{ 'aria-label': 'search' }}
        onKeyDown={onKeyDown}
        sx={{
          color: 'inherit',
          width: '100%',
          '& .MuiInputBase-input': {
            py: 1.2,
            pr: 1,
            pl: 'calc(1em + 32px)',
            fontSize: '0.95rem',
            width: '100%',
          },
        }}
      />
    </Box>
  );
};

export default Search;