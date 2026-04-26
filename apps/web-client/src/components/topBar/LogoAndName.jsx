import { Box, Typography } from '@mui/material';
import CyberDriveMark from './CyberDriveMark';

const LogoAndName = () => {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', width: 240, flexShrink: 0 }}>
      <Box sx={{ mr: 1.5, lineHeight: 0, filter: 'drop-shadow(0 4px 6px rgb(99 102 241 / 0.4))' }}>
        <CyberDriveMark size={40} />
      </Box>
      <Typography
        variant="h6"
        color="text.primary"
        sx={{
          display: { xs: 'none', sm: 'block' },
          fontWeight: 700,
          letterSpacing: '-0.025em',
          fontSize: '1.25rem',
        }}
      >
        Cyber<Box component="span" sx={{ fontWeight: 400, color: 'text.secondary' }}> Drive</Box>
      </Typography>
    </Box>
  );
};

export default LogoAndName;