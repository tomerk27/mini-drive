import { useState, useEffect } from 'react';
import { getStorageUsageApi } from '../../api/userApi';

const formatBytes = (bytes) => {
    if (bytes >= 1024 ** 3) return `${(bytes / 1024 ** 3).toFixed(1)} GB`;
    if (bytes >= 1024 ** 2) return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
    if (bytes >= 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${bytes} B`;
};

const useStorage = () => {
    const [usedBytes, setUsedBytes] = useState(0);
    const [maxBytes, setMaxBytes] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStorage = async () => {
            try {
                const data = await getStorageUsageApi();
                setUsedBytes(data.used_bytes);
                setMaxBytes(data.max_bytes);
            } catch {
                // silently fail — sidebar is non-critical
            } finally {
                setLoading(false);
            }
        };
        fetchStorage();
    }, []);

    const usedPercent = maxBytes > 0 ? (usedBytes / maxBytes) * 100 : 0;

    return {
        usedBytes,
        maxBytes,
        usedPercent,
        usedFormatted: formatBytes(usedBytes),
        maxFormatted: formatBytes(maxBytes),
        loading,
    };
};

export default useStorage;
