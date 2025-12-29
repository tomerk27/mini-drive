import './fileItem'
import fileIcon from "../../assets/icons/fileIcon.svg";
const FileItem = ({fileName}) => {
    return (
        <div className='file-card'>
            <img src={fileIcon} alt='file' className='fileIcon' />
            <span className='file-name' title={fileName} >
                {fileName}
            </span>
        </div>
    )
    
};

export default FileItem;