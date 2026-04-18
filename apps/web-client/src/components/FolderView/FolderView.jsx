import ItemsView from '../itemsView/itemsView';

const FolderView = ({ items, loading, error, refreshFolder, onFolderClick}) => {
    return (
        <ItemsView
            items={items}
            loading={loading}
            error={error}
            refreshFolder={refreshFolder}
            emptyMessage="This folder is empty"
            onFolderClick={onFolderClick}
        />
    );
};

export default FolderView;
