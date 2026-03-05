import { useNavigate, useLocation } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Button, Typography } from '@mui/material';
import { alpha } from '@mui/material/styles';
import HomeIcon from '@mui/icons-material/Home';
import ComputerIcon from '@mui/icons-material/Computer';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import ReportGmailerrorredIcon from '@mui/icons-material/ReportGmailerrorred';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import CloudQueueIcon from '@mui/icons-material/CloudQueue';
import AddIcon from '@mui/icons-material/Add';

const drawerWidth = 256;

const SideBar = ({ onNewClick }) => {
    const navigate = useNavigate();
    const location = useLocation();

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { 
                    width: drawerWidth, 
                    boxSizing: 'border-box',
                    borderRight: '1px solid #f1f5f9',
                    backgroundColor: '#ffffff',
                    pt: 11, // Push below top bar
                    px: 1.5,
                },
            }}
        >
            <Box sx={{ mb: 4, px: 0.5 }}>
                <Button
                    variant="contained"
                    fullWidth
                    startIcon={<AddIcon />}
                    onClick={onNewClick}
                    sx={{
                        borderRadius: 3,
                        py: 1.5,
                        bgcolor: 'primary.main',
                        color: 'white',
                        boxShadow: '0 10px 15px -3px rgb(99 102 241 / 0.3)',
                        '&:hover': {
                            bgcolor: 'primary.dark',
                            boxShadow: '0 20px 25px -5px rgb(99 102 241 / 0.3)',
                        },
                        textTransform: 'none',
                        fontSize: '0.95rem',
                        fontWeight: 600
                    }}
                >
                    Create New
                </Button>
            </Box>

            <List sx={{ pt: 0 }}>
                {[
                    { text: 'My Files', icon: <HomeIcon fontSize="small" />, selected: location.pathname.startsWith('/dashboard'), onClick: () => navigate('/dashboard')},
                    { text: 'Shared', icon: <PeopleAltIcon fontSize="small" />, selected: location.pathname === '/shared', onClick: () => navigate('/shared') },
                    { text: 'Starred', icon: <StarBorderIcon fontSize="small" />, selected: location.pathname === '/starred', onClick: () => navigate('/starred') },
                    { text: 'Recent', icon: <AccessTimeIcon fontSize="small" /> },
                    { text: 'Trash', icon: <DeleteOutlineIcon fontSize="small" /> },
                ].map((item) => (
                    <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                        <ListItemButton 
                            selected={item.selected}
                            sx={{
                                borderRadius: 3,
                                py: 1,
                                px: 2,
                                '&.Mui-selected': {
                                    bgcolor: alpha('#6366f1', 0.08),
                                    color: 'primary.main',
                                    '&:hover': {
                                        bgcolor: alpha('#6366f1', 0.12),
                                    },
                                    '& .MuiListItemIcon-root': {
                                        color: 'primary.main',
                                    },
                                },
                                '&:hover': {
                                    bgcolor: '#f8fafc',
                                }
                            }}
                            onClick={item.onClick}
                        >
                            <ListItemIcon sx={{ minWidth: 36, color: 'text.secondary' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText 
                                primary={item.text} 
                                primaryTypographyProps={{ 
                                    fontWeight: item.selected ? 600 : 500, 
                                    fontSize: '0.875rem',
                                    color: 'inherit'
                                }} 
                            />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Box sx={{ mt: 'auto', mb: 4, px: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1, gap: 1 }}>
                    <CloudQueueIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
                    <Typography variant="body2" sx={{ fontWeight: 600, color: 'text.secondary', fontSize: '0.75rem' }}>
                        STORAGE
                    </Typography>
                </Box>
                <Box sx={{ width: '100%', height: 6, bgcolor: '#f1f5f9', borderRadius: 3, mb: 1 }}>
                    <Box sx={{ width: '45%', height: '100%', bgcolor: 'primary.main', borderRadius: 3 }} />
                </Box>
                <Typography variant="caption" sx={{ color: 'text.secondary', fontSize: '0.7rem' }}>
                    1.2 GB of 15 GB used
                </Typography>
            </Box>
        </Drawer>
    );
};

export default SideBar;
