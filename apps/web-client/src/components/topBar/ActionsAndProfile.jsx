import { Box, IconButton } from '@mui/material';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import GridViewOutlinedIcon from '@mui/icons-material/GridViewOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';

const ActionsAndProfile = () => {
  return (
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
  );
};

export default ActionsAndProfile;