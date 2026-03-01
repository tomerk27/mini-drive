import ItemsView from '../itemsView/itemsView';

const FolderView = ({ childFiles, childFolders, loading, error, refreshFolder}) => {
    const items = [...childFolders, ...childFiles];

    return (
        <ItemsView 
            items={items}
            loading={loading}
            error={error}
            refreshFolder={refreshFolder}
            emptyMessage="This folder is empty"
        />
    );
};

export default FolderView;
