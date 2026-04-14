import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useSearch = () => {
    const [term, setTerm] = useState('');
    const navigate = useNavigate();

    const handleSearch = () => {
        if (!term.trim()) {
            navigate(`/dashboard`);
            return;
        }
        navigate(`/search?q=${term}`);
    };

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