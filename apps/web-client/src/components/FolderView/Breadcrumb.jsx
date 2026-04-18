import { Box, Typography } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

const Breadcrumb = ({ breadcrumb, rootLabel, onRootClick, onItemClick }) => {
    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, flexWrap: 'wrap' }}>
            <Typography
                variant="h5"
                sx={{
                    fontWeight: 700,
                    letterSpacing: '-0.025em',
                    color: 'primary.main',
                    cursor: 'pointer',
                    '&:hover': { textDecoration: 'underline' }
                }}
                onClick={onRootClick}
            >
                {rootLabel}
            </Typography>

            {breadcrumb?.map((crumb, index) => {
                const isLast = index === breadcrumb.length - 1;
                return (
                    <Box key={crumb.id} sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <NavigateNextIcon sx={{ fontSize: 24, color: 'text.secondary' }} />
                        <Typography
                            variant="h5"
                            sx={{
                                fontWeight: isLast ? 700 : 500,
                                color: isLast ? 'text.primary' : 'primary.main',
                                cursor: isLast ? 'default' : 'pointer',
                                '&:hover': isLast ? {} : { textDecoration: 'underline' }
                            }}
                            onClick={() => !isLast && onItemClick?.(crumb)}
                        >
                            {crumb.name}
                        </Typography>
                    </Box>
                );
            })}
        </Box>
    );
};

export default Breadcrumb;
