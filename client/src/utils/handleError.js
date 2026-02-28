const handleError = (setError, error, defaultMassage) => {
    const detail = error.response?.data?.detail;
    setError(typeof detail === 'string' ? detail : defaultMassage);
}

export default handleError;