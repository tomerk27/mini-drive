import { Box, Typography } from '@mui/material';
import CloudOutlinedIcon from '@mui/icons-material/CloudOutlined';

const LogoAndName = () => {
  return (
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
  );
};

export default LogoAndName;