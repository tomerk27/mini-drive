import Item from "./item";

class FileItem extends Item {
    constructor({size, type, ...baseProps}) {
        super(baseProps);
        this.size = size;
        this.type = type;
    }


}

export default FileItem;