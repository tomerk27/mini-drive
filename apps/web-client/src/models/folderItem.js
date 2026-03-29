import Item from "./item";

class FolderItem extends Item {
    constructor(children = [], ...baseProps) {
        super(baseProps);
        this.children = children;
    }

    addItem(item) {
        this.children.push(item);
    }

    removeItem(itemId) {
        const initialLength = this.children.length;

        this.children = this.children.filter(item => item.id !== itemId);

        if(initialLength === this.children.length) {
            console.warn(`Item ${itemId} not found in ${this.name}`);
        }
    }

    updatePath(path) {
        this.path = path;
        this.children.array.forEach((child) => {
            if (child instanceof FolderItem){
                child.updatePath(this.path + child.name + '/');
            }
            else {
                child.updatePath(this.path + child.name + child.type);
            }
        });
    }
}

export default FolderItem;