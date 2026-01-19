import { Card, CardActionArea, CardContent, Typography, IconButton, Box } from '@mui/material';
import FileIcon from './itemIcon';
import ActionMenu from './actionMenu';

const Item = ({ fileName, fileType }) => {
  return (
    <Card 
      sx={{ 
        width: 200,          
        borderRadius: 2,  
        position: 'relative', 
        '&:hover': {         
            boxShadow: 6 
        }
      }}
    >
        <Box sx={{ position: 'absolute', top: 5, right: 5, zIndex: 10 }}>
            <ActionMenu />
        </Box>

      <CardActionArea sx={{ height: '100%', pt: 4, pb: 2 }}>
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
            <FileIcon fileType={fileType} />
        </Box>

        <CardContent sx={{ py: 0, px: 2 }}>
          <Typography 
            variant="subtitle1" 
            component="div" 
            noWrap
            title={fileName}
            sx={{ fontWeight: 'bold', fontSize: '0.9rem' }}
          >
            {fileName}
          </Typography>
          
          {/* אפשר להוסיף כאן סוג קובץ או תאריך */}
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
            {fileType || 'File'}
          </Typography>
        </CardContent>

      </CardActionArea>
    </Card>
  );
};

export default Item;