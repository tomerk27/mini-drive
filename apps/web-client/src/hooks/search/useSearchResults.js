/**
 * Hook that reads the ?q= query param from the URL and fetches matching items.
 *
 * Re-runs the search automatically whenever the URL query changes (e.g. user
 * types a new term and presses Enter from the search page).
 */

import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { searchApi } from "../../api/searchApi";
import handleError from "../../utils/handleError";

const useSearchResults = () => {
    const [searchParams] = useSearchParams();
    const [isSearching, setIsSearching] = useState(false);
    const [error, setError] = useState(null);
    const [searchResults, setSearchResults] = useState(null);

    // Pull the search term directly from the URL so the page is bookmarkable.
    const query = searchParams.get('q');

    useEffect(() => {
        if (!query.trim()) return;

        const performSearch = async () => {
            setError(null);
            setIsSearching(true);

            try {
                const results = await searchApi(query);
                setSearchResults(results);
            } catch (error) {
                handleError(setError, error, "Search failed. Please try again.");
                setSearchResults([]);
            } finally {
                setIsSearching(false);
            }
        };

        performSearch();
    }, [query]); // Re-run whenever the query param changes.

    return { query, searchResults, isSearching, error };
};

export default useSearchResults;