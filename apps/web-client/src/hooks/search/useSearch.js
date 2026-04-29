/**
 * Hook for the search bar in the top navigation.
 *
 * Navigates to /search?q=<term> on submit. If the search box is cleared
 * and submitted, it redirects back to the dashboard instead.
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useSearch = () => {
    const [term, setTerm] = useState('');
    const navigate = useNavigate();

    const handleSearch = () => {
        if (!term.trim()) {
            // Empty search — go back to the normal drive view.
            navigate(`/dashboard`);
            return;
        }
        navigate(`/search?q=${term}`);
    };

    /** Submits the search when the user presses Enter in the search field. */
    const handleKeyDown = (e) => {
        if (e.key === "Enter") handleSearch();
    };

    return {
        term,
        setTerm,
        handleKeyDown,
        handleSearch
    };
};

export default useSearch;