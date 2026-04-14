import { AppBar, Toolbar } from '@mui/material';
import { alpha } from '@mui/material/styles';
import Search from './Search'; // Import the new Search component
import LogoAndName from './LogoAndName'; // Import the new LogoAndName component
import ActionsAndProfile from './ActionsAndProfile'; // Import the new ActionsAndProfile component
import useSearch from '../../hooks/search/useSearch';


const TopBar = () => {
    const { term, setTerm, handleKeyDown } = useSearch();
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
                /> 

                <ActionsAndProfile />

            </Toolbar>
        </AppBar>
    );
};

export default TopBar;
