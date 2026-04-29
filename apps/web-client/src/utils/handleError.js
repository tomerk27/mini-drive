/**
 * Extracts a user-friendly error message from an Axios error response.
 *
 * The API server always returns errors as { detail: "..." }. If the detail
 * field is present and a string, it is shown directly. Otherwise the caller's
 * default message is used as a fallback.
 *
 * @param {Function} setError - State setter to display the error in the UI.
 * @param {Error} error - The Axios error object caught in a try/catch.
 * @param {string} defaultMassage - Fallback message if no API detail is available.
 */
const handleError = (setError, error, defaultMassage) => {
    const detail = error.response?.data?.detail;
    setError(typeof detail === 'string' ? detail : defaultMassage);
};

export default handleError;