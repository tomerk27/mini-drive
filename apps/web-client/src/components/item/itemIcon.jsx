import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import ImageIcon from '@mui/icons-material/Image';
import FolderIcon from '@mui/icons-material/Folder';
import DescriptionIcon from '@mui/icons-material/Description';
import VideoFileOutlinedIcon from '@mui/icons-material/VideoFileOutlined';
import ArchiveOutlinedIcon from '@mui/icons-material/ArchiveOutlined';
import CodeOutlinedIcon from '@mui/icons-material/CodeOutlined';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import SlideshowOutlinedIcon from '@mui/icons-material/SlideshowOutlined';
import PublicIcon from '@mui/icons-material/Public'; // For HTML, CSS, JS

const FileIcon = ({ fileType }) => {
    const iconSize = 70;
    const commonColor = '#909090'; // Default color for most icons
    
    // Normalize file type input
    const type = typeof fileType === 'string' ? fileType : (fileType?.file_type || fileType?.type);

    switch (type) {
        case 'folder':
            return <FolderIcon sx={{ fontSize: iconSize, color: '#FFD700' }} />;

        case 'application/pdf':
        case 'pdf':
            return <PictureAsPdfIcon sx={{ fontSize: iconSize, color: '#F40F02' }} />;

        case 'image/png':
        case 'image/jpeg':
        case 'image/gif':
        case 'image/bmp':
        case 'image/webp':
        case 'image': // Generic image type
            return <ImageIcon sx={{ fontSize: iconSize, color: '#B051DE' }} />;

        case 'video/mp4':
        case 'video/mpeg':
        case 'video/quicktime':
        case 'video/x-msvideo': // .avi
        case 'video/x-matroska': // .mkv
        case 'video': // Generic video type
            return <VideoFileOutlinedIcon sx={{ fontSize: iconSize, color: '#FF4500' }} />;

        case 'application/zip':
        case 'application/x-rar-compressed':
        case 'application/x-7z-compressed':
        case 'zip':
        case 'rar':
        case '7z':
            return <ArchiveOutlinedIcon sx={{ fontSize: iconSize, color: '#8B4513' }} />;
            
        case 'text/html':
        case 'text/css':
        case 'application/javascript':
        case 'application/json':
        case 'application/xml':
        case 'text/plain': // text files
        case 'html':
        case 'css':
        case 'js':
        case 'json':
        case 'xml':
        case 'txt':
            return <CodeOutlinedIcon sx={{ fontSize: iconSize, color: '#00BFFF' }} />;

        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': // .xlsx
        case 'application/vnd.ms-excel': // .xls
        case 'text/csv':
        case 'xls':
        case 'xlsx':
        case 'csv':
            return <TableChartOutlinedIcon sx={{ fontSize: iconSize, color: '#228B22' }} />;

        case 'application/vnd.openxmlformats-officedocument.presentationml.presentation': // .pptx
        case 'application/vnd.ms-powerpoint': // .ppt
        case 'ppt':
        case 'pptx':
            return <SlideshowOutlinedIcon sx={{ fontSize: iconSize, color: '#FF1493' }} />;
        
        default:
            return <InsertDriveFileIcon sx={{ fontSize: iconSize, color: commonColor }} />;
    }
}

export default FileIcon;