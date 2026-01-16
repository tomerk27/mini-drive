import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import ImageIcon from '@mui/icons-material/Image';
import FolderIcon from '@mui/icons-material/Folder';
import DescriptionIcon from '@mui/icons-material/Description';

const FileIcon = ({ fileType }) => {
    switch (fileType) {
        case 'folder':
            return <FolderIcon sx={{ fontSize: 90, color: '#FFD700' }} />;

        case 'pdf':
            return <PictureAsPdfIcon sx={{ fontSize: 90, color: '#F40F02' }} />;

        case 'png':
        case 'jpg':
        case 'jpeg':
        case 'image':
            return <ImageIcon sx={{ fontSize: 90, color: '#B051DE' }} />;

        case 'doc':
        case 'docx':
        case 'txt':
            return <DescriptionIcon sx={{ fontSize: 90, color: '#4285F4' }} />;

        default:
            return <InsertDriveFileIcon sx={{ fontSize: 90, color: '#909090' }} />;
    }
}

export default FileIcon;