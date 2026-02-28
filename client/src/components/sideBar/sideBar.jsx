import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Button } from '@mui/material';
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
    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                [`& .MuiDrawer-paper`]: { 
                    width: drawerWidth, 
                    boxSizing: 'border-box',
                    borderRight: 'none',
                    pt: 10, // Push below top bar
                    pl: 2
                },
            }}
        >
            <Box sx={{ mb: 2 }}>
                <Button
                    variant="contained"
                    startIcon={<AddIcon fontSize="large" />}
                    onClick={onNewClick}
                    sx={{
                        borderRadius: 4,
                        py: 1.5,
                        px: 3,
                        bgcolor: 'white',
                        color: 'text.primary',
                        boxShadow: '0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15)',
                        '&:hover': {
                            bgcolor: '#f8f9fa',
                            boxShadow: '0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15)',
                        },
                        textTransform: 'none',
                        fontSize: '1rem',
                        fontWeight: 500
                    }}
                >
                    New
                </Button>
            </Box>

            <List sx={{ pt: 0 }}>
                {[
                    { text: 'My Drive', icon: <HomeIcon />, selected: true },
                    { text: 'Computers', icon: <ComputerIcon /> },
                    { text: 'Shared with me', icon: <PeopleAltIcon /> },
                    { text: 'Recent', icon: <AccessTimeIcon /> },
                    { text: 'Starred', icon: <StarBorderIcon /> },
                ].map((item) => (
                    <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                        <ListItemButton 
                            selected={item.selected}
                            sx={{
                                borderRadius: '0 24px 24px 0',
                                '&.Mui-selected': {
                                    bgcolor: '#c2e7ff',
                                    color: '#001d35',
                                    '&:hover': {
                                        bgcolor: '#b4d7f0',
                                    }
                                }
                            }}
                        >
                            <ListItemIcon sx={{ minWidth: 40, color: item.selected ? '#001d35' : 'inherit' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText primary={item.text} primaryTypographyProps={{ fontWeight: item.selected ? 600 : 400, fontSize: '0.875rem' }} />
                        </ListItemButton>
                    </ListItem>
                ))}

                <Box sx={{ my: 1, borderTop: '1px solid #e0e0e0', mx: 2 }} />

                {[
                    { text: 'Spam', icon: <ReportGmailerrorredIcon /> },
                    { text: 'Trash', icon: <DeleteOutlineIcon /> },
                    { text: 'Storage', icon: <CloudQueueIcon /> },
                ].map((item) => (
                    <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                        <ListItemButton sx={{ borderRadius: '0 24px 24px 0' }}>
                            <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
                            <ListItemText primary={item.text} primaryTypographyProps={{ fontSize: '0.875rem' }} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </Drawer>
    );
};

export default SideBar;
