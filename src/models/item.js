class Item{
    constructor({ id, name, createdAt, path}){
        this.id = id;
        this.name = name;
        this.createdAt = createdAt;
        this.path = path;
    }

    rename(name) {
        this.name = name;
    }

    updatePath(path) {
        this.path = path;
    }
}

export default Item