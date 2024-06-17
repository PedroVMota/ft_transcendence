export class HTML_PROPS{
    constructor(){
        this.element = undefined
    }
    createElement(element){
        this.element = document.createElement(element);
    }
    appendChild(child){
        this.element.appendChild(child);
    }
    addEventListener(event, callback){
        this.element.addEventListener(event, callback);
    }
    addClass(className){
        
        this.element.classList.add(className);
    }
    removeClass(className){
        this.element.classList.remove(className);
    }
    remove(){
        this.element.remove();
    }
    get(){
        return this.element;
    }
    clear(){
        this.element.innerHTML = '';
    }
    setInnerHTML(html){
        this.element.innerHTML = html;
    }
    setAttribute(attribute, value){
        this.element.setAttribute(attribute, value);
    }
    getAttribute(attribute){
        return this.element.getAttribute(attribute);
    }
    setId(id){
        this.element.id = id;
    }
    getId(){
        return this.element.id;
    }
    setStyle(style){
        this.element.style = style;
    }
    getStyle(){
        return this.element.style;
    }
    setParent(parent){
        parent.appendChild(this.element);
    }


}

export class li extends HTML_PROPS{
    constructor(styleString){
        super();
        this.createElement('li');
        this.element.classList.add(styleString);
    }
}

export class ul extends HTML_PROPS{
    constructor(){
        super();
        this.createElement('ul');
    }

    setElement(element){
        this.element = element;
    }



}