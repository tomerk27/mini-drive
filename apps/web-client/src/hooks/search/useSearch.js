import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useSearch = () => {
    const [term, setTerm] = useState('');
    const navigate = useNavigate();

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {

            if (!term.trim()) {
                navigate(`/dashboard`);
                return;
            };

            navigate(`/search?q=${term}`);
        };
    };

    return {
        term,
        setTerm,
        handleKeyDown
    };
};

export default useSearch;