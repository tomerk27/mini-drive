import { Box, Typography } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { useNavigate } from 'react-router-dom';

const Breadcrumb = ({ breadcrumb }) => {
    const navigate = useNavigate();

    if (!breadcrumb || breadcrumb.length === 0) return null;

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 2, flexWrap: 'wrap' }}>
            <Typography
                variant="body2"
                sx={{ color: 'primary.main', cursor: 'pointer', fontWeight: 500, '&:hover': { textDecoration: 'underline' } }}
                onClick={() => navigate('/dashboard')}
            >
                My Files
            </Typography>

            {breadcrumb.map((crumb, index) => {
                const isLast = index === breadcrumb.length - 1;
                return (
                    <Box key={crumb.id} sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <NavigateNextIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                        <Typography
                            variant="body2"
                            sx={{
                                fontWeight: isLast ? 600 : 500,
                                color: isLast ? 'text.primary' : 'primary.main',
                                cursor: isLast ? 'default' : 'pointer',
                                '&:hover': isLast ? {} : { textDecoration: 'underline' }
                            }}
                            onClick={() => !isLast && navigate(`/dashboard/${crumb.id}`)}
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
