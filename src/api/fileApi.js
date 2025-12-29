export const filesUploaderApi = async (filesArray) => {
    const formData = new FormData();

    filesArray.forEach(file => {
        formData.append("file", file);
    });

    //try {
    //    const response = await fetch("/upload", {
    //        body: formData,
    //        method: "POST",
    //    });
//
    //    if (!response.ok) {
    //        throw new Error('Server error: ${response.status}');
    //    }
//
    //    return await response.json();
    //}
    //catch (error) {
    //    console.error('API error:', error)
    //    throw error
    //}
};