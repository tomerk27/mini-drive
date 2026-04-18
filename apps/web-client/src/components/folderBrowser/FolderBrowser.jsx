import { Box } from '@mui/material';
import Breadcrumb from '../FolderView/Breadcrumb';
import ItemsView from '../itemsView/itemsView';
import useFolderBrowser from '../../hooks/folder/useFolderBrowser';

const FolderBrowser = ({
    rootItems,
    rootLabel,
    onRefresh,
    emptyMessage,
    emptySubMessage
}) => {
    const {
        currentItems,
        breadcrumb,
        loading,
        error,
        handleFolderClick,
        navigateTo,
        refreshCurrent,
    } = useFolderBrowser(rootItems, rootLabel, onRefresh);

    return (
        <Box>
            <Breadcrumb
                rootLabel={rootLabel}
                onRootClick={() => navigateTo(0)}
                breadcrumb={breadcrumb}
                onItemClick={(crumb) => navigateTo(crumb.index)}
            />
            <Box sx={{
                bgcolor: 'background.paper',
                borderRadius: 4,
                p: 3,
                mt: 4,
                minHeight: 'calc(100vh - 200px)',
                border: '1px solid #f1f5f9',
                boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
            }}>
                <ItemsView
                    items={currentItems}
                    loading={loading}
                    error={error}
                    refreshFolder={refreshCurrent}
                    onFolderClick={handleFolderClick}
                    emptyMessage={emptyMessage}
                    emptySubMessage={emptySubMessage}
                />
            </Box>
        </Box>
    );
};

export default FolderBrowser;
