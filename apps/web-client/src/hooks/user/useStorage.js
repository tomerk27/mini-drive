/**
 * Hook that fetches the current user's storage usage and quota from the API.
 *
 * Returns both raw byte counts and pre-formatted strings (e.g. "1.2 GB")
 * for easy display in the sidebar. Failures are swallowed silently because
 * the storage bar is decorative and should not break the main UI.
 */

import { useState, useEffect } from 'react';
import { getStorageUsageApi } from '../../api/userApi';

/**
 * Converts a raw byte count into a human-readable string.
 *
 * @param {number} bytes - Size in bytes.
 * @returns {string} Formatted string like "1.2 GB", "500 MB", etc.
 */
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
                // Silently fail — the storage bar in the sidebar is non-critical.
            } finally {
                setLoading(false);
            }
        };
        fetchStorage();
    }, []);

    // usedPercent drives the progress bar width (0–100).
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
