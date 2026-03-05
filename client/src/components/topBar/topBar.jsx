import { Box, AppBar, Toolbar, Typography, InputBase, IconButton } from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import GridViewOutlinedIcon from '@mui/icons-material/GridViewOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import CloudOutlinedIcon from '@mui/icons-material/CloudOutlined';

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.black, 0.04),
  border: '1px solid transparent',
  '&:hover': {
    backgroundColor: '#ffffff',
    borderColor: theme.palette.primary.light,
    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
  },
  '&:focus-within': {
    backgroundColor: '#ffffff',
    borderColor: theme.palette.primary.main,
    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
  },
  marginRight: theme.spacing(2),
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
  flexGrow: 1,
  maxWidth: 640,
  transition: theme.transitions.create(['background-color', 'border-color', 'box-shadow']),
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
    padding: theme.spacing(1.2, 1, 1.2, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    fontSize: '0.95rem',
  },
}));

const TopBar = () => {
  return (
    <AppBar 
      position="fixed" 
      color="inherit" 
      elevation={0} 
      sx={{ 
        borderBottom: '1px solid #f1f5f9', 
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: alpha('#ffffff', 0.95),
        backdropFilter: 'blur(8px)'
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', px: { xs: 2, sm: 4 }, minHeight: 72 }}>
        
        {/* Left side: Logo & Name */}
        <Box sx={{ display: 'flex', alignItems: 'center', width: 240, flexShrink: 0 }}>
          <Box 
            sx={{ 
              backgroundColor: 'primary.main', 
              borderRadius: 2.5, 
              width: 40, 
              height: 40, 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              mr: 1.5,
              color: 'white',
              boxShadow: '0 4px 6px -1px rgb(99 102 241 / 0.4)'
            }}
          >
            <CloudOutlinedIcon />
          </Box>
          <Typography 
            variant="h6" 
            color="text.primary" 
            sx={{ 
              display: { xs: 'none', sm: 'block' }, 
              fontWeight: 700,
              letterSpacing: '-0.025em',
              fontSize: '1.25rem'
            }}
          >
            My Drive
          </Typography>
        </Box>

        {/* Middle: Search bar */}
        <Search>
          <SearchIconWrapper>
            <SearchIcon fontSize="small" />
          </SearchIconWrapper>
          <StyledInputBase
            placeholder="Search your files and folders"
            inputProps={{ 'aria-label': 'search' }}
          />
        </Search>

        {/* Right side: Actions & Profile */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, flexShrink: 0 }}>
          <IconButton size="medium" color="inherit" sx={{ color: 'text.secondary' }}>
            <SettingsOutlinedIcon fontSize="small" />
          </IconButton>
          <IconButton size="medium" color="inherit" sx={{ color: 'text.secondary' }}>
            <GridViewOutlinedIcon fontSize="small" />
          </IconButton>
          <Box sx={{ ml: 1, borderLeft: '1px solid #e2e8f0', pl: 1 }}>
            <IconButton size="medium" edge="end" color="inherit">
              <AccountCircleOutlinedIcon fontSize="large" sx={{ color: 'text.secondary' }} />
            </IconButton>
          </Box>
        </Box>

      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
