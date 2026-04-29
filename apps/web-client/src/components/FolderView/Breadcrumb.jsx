/**
 * Breadcrumb.jsx
 *
 * Renders the folder navigation trail (e.g. "My Files > Projects > 2024").
 * The root label and all intermediate folders are clickable; the last crumb
 * (current folder) is shown as plain text so the user knows they're already there.
 */
import { Box, Typography } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

/**
 * Breadcrumb navigation bar for folder drill-down.
 *
 * @param {Array}    breadcrumb   - Ordered array of { id, name, index } crumb objects.
 * @param {string}   rootLabel    - Display name for the root level (e.g. "My Files").
 * @param {Function} onRootClick  - Called when the user clicks the root label.
 * @param {Function} onItemClick  - Called with a crumb object when an ancestor is clicked.
 */
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
                // The last crumb is the current folder — make it non-clickable
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
