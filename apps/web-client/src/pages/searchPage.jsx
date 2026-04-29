/**
 * searchPage.jsx
 *
 * Protected page rendered at /search.  Reads the current search query from
 * useSearchResults (which pulls it from the URL query string) and displays
 * matching items in a flat ItemsView — no folder navigation needed here.
 */
import { Box, Typography } from '@mui/material';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import useSearchResults from '../hooks/search/useSearchResults';
import ItemsView from '../components/itemsView/itemsView';

const SearchPage = () => {
    const { query, searchResults, isSearching, error } = useSearchResults();

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />
            
            <SideBar />

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary', letterSpacing: '-0.025em' }}>
                        Results for "{query}"
                    </Typography>
                </Box>

                <Box sx={{ 
                    bgcolor: 'background.paper', 
                    borderRadius: 4, 
                    p: 3, 
                    minHeight: 'calc(100vh - 200px)',
                    border: '1px solid #f1f5f9',
                    boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
                }}>
                    <ItemsView 
                        items={searchResults}
                        loading={isSearching}
                        error={error}
                        emptyMessage="No results found"
                        emptySubMessage="Try different seach term"
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default SearchPage;
