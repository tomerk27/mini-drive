/**
 * @file topBar.jsx
 * Fixed top application bar rendered on every authenticated page. Composes
 * LogoAndName, the Search input, and ActionsAndProfile into a single toolbar.
 * Search state is managed by the useSearch hook and passed down as props.
 */

import { AppBar, Toolbar } from '@mui/material';
import { alpha } from '@mui/material/styles';
import Search from './Search';
import LogoAndName from './LogoAndName';
import ActionsAndProfile from './ActionsAndProfile';
import useSearch from '../../hooks/search/useSearch';

/**
 * Fixed top navigation bar that sits above the sidebar and main content.
 *
 * @returns {JSX.Element} A full-width MUI AppBar containing the logo, search field, and actions.
 */
const TopBar = () => {
    // useSearch owns the search term and handles keyboard (Enter) + button submit.
    const { term, setTerm, handleKeyDown, handleSearch } = useSearch();
    return (
        <AppBar
            position="fixed"
            color="inherit"
            elevation={0}
            sx={{
                borderBottom: '1px solid #f1f5f9',
                zIndex: (theme) => theme.zIndex.drawer + 1,
                backgroundColor: alpha('#ffffff', 0.95),
                backdropFilter: 'blur(8px)'
            }}
        >
            <Toolbar sx={{ justifyContent: 'space-between', px: { xs: 2, sm: 4 }, minHeight: 72 }}>

                <LogoAndName />

                <Search
                    searchTerm={term}
                    onSearchTermChange={(e) => setTerm(e.target.value)}
                    onKeyDown={handleKeyDown}
                    onSearch={handleSearch}
                /> 

                <ActionsAndProfile />

            </Toolbar>
        </AppBar>
    );
};

export default TopBar;
