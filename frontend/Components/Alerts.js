// using bootstrap  

export function ErrorCompoentJavaScriptVanilla(data){
    let error = document.createElement('div');
    error.className = 'alert alert-danger';
    error.innerHTML = JSON.stringify(data);
    return error;
}

