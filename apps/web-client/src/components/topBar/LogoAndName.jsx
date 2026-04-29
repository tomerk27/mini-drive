/**
 * @file LogoAndName.jsx
 * Displays the CyberDrive logo mark alongside the "Cyber Drive" wordmark.
 * Occupies the left slot of the TopBar and is hidden on extra-small screens.
 */

import { Box, Typography } from '@mui/material';
import CyberDriveMark from './CyberDriveMark';

/**
 * Logo mark + app name lockup for the top-left corner of the app bar.
 *
 * @returns {JSX.Element} A fixed-width flex container with the SVG logo and styled text.
 */
const LogoAndName = () => {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', width: 240, flexShrink: 0 }}>
      <Box sx={{ mr: 1.5, lineHeight: 0, filter: 'drop-shadow(0 4px 6px rgb(99 102 241 / 0.4))' }}>
        <CyberDriveMark size={40} />
      </Box>
      {/* "Cyber" is bold; "Drive" drops to a lighter weight for visual contrast. */}
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