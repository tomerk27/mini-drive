class Item{
    constructor({ id, name, createdAt}){
        this.id = id;
        this.name = name;
        this.createdAt = createdAt;
    }

    rename(name){
        this.name = name;
    }
}

export default Item