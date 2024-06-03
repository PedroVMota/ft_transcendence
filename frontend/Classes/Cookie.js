export class Cookie { 
    constructor() { }
    isSessionLoggedIn() { return document.cookie.includes('csrftoken'); }
    getSession() { return document.cookie; }
    getCSRFToken() { return document.cookie.split('=')[1]; }



    static delete(name) {
        console.log({
            "Message": `Deleting cookie: ${name}`
        })
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }

    static deleteLocalStorage() {
        localStorage.clear();
    }
}
