import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { searchApi } from "../../api/searchApi";
import handleError from "../../utils/handleError";


const useSearchResults = () => {
    const [searchParams] = useSearchParams();
    const [isSearching, setIsSearching] = useState(false);
    const [error, setError] = useState(null);
    const [searchResults, setSearchResults] = useState(null);

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
                handleError(setError, error, "Failed to fetch search results");
                setSearchResults([]);
            } finally {
                setIsSearching(false);
            }
        };

        performSearch();
    }, [query]);

    return { query, searchResults, isSearching, error };
};

export default useSearchResults;