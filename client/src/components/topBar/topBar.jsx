import { Box, AppBar, Toolbar, Typography, InputBase, IconButton } from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import SettingsIcon from '@mui/icons-material/Settings';
import AppsIcon from '@mui/icons-material/Apps';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius * 4,
  backgroundColor: alpha(theme.palette.common.black, 0.05),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.black, 0.1),
    boxShadow: '0 1px 1px rgba(0,0,0,0.1)'
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
  flexGrow: 1,
  maxWidth: 720,
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.text.secondary
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1.5, 1, 1.5, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
  },
}));

const TopBar = () => {
  return (
    <AppBar position="fixed" color="inherit" elevation={0} sx={{ borderBottom: '1px solid #e0e0e0', zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar sx={{ justifyContent: 'space-between', px: { xs: 1, sm: 3 } }}>
        
        {/* Left side: Logo & Name */}
        <Box sx={{ display: 'flex', alignItems: 'center', width: 240, flexShrink: 0 }}>
          <img src="https://upload.wikimedia.org/wikipedia/commons/1/12/Google_Drive_icon_%282020%29.svg" alt="Drive Logo" style={{ width: 40, height: 40, marginRight: 8 }} />
          <Typography variant="h6" color="text.primary" sx={{ display: { xs: 'none', sm: 'block' }, fontWeight: 400 }}>
            Drive
          </Typography>
        </Box>

        {/* Middle: Search bar */}
        <Search>
          <SearchIconWrapper>
            <SearchIcon />
          </SearchIconWrapper>
          <StyledInputBase
            placeholder="Search in Drive"
            inputProps={{ 'aria-label': 'search' }}
          />
        </Search>

        {/* Right side: Actions & Profile */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexShrink: 0 }}>
          <IconButton size="large" color="inherit" sx={{ display: { xs: 'none', md: 'inline-flex' } }}>
            <SettingsIcon />
          </IconButton>
          <IconButton size="large" color="inherit" sx={{ display: { xs: 'none', md: 'inline-flex' } }}>
            <AppsIcon />
          </IconButton>
          <IconButton size="large" edge="end" color="inherit">
            <AccountCircleIcon fontSize="large" />
          </IconButton>
        </Box>

      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
