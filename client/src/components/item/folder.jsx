import { useNavigate } from 'react-router-dom';
import { Card, CardActionArea, Typography, Box } from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';

const FolderItem = ({ folder }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(`/dashboard/folder/${folder.id}`);
    };

    return (
        <Card 
            variant="outlined" 
            sx={{ 
                borderRadius: 2,
                borderColor: 'grey.300',
                transition: '0.2s',
                '&:hover': {
                    backgroundColor: 'action.hover',
                    borderColor: 'primary.main',
                    boxShadow: 1
                }
            }}
        >
            <CardActionArea 
                onClick={handleClick}
                sx={{ 
                    p: 1.5,
                    display: 'flex', 
                    justifyContent: 'flex-start',
                    alignItems: 'center',
                    gap: 1.5
                }}
            >
                <FolderIcon 
                    sx={{ 
                        color: 'text.secondary',
                        fontSize: 28 
                    }} 
                />

                {/* שם התיקייה */}
                <Typography 
                    variant="body2" 
                    fontWeight={500}
                    noWrap 
                    title={folder.name}
                >
                    {folder.name}
                </Typography>
            </CardActionArea>
        </Card>
    );
};

export default FolderItem;