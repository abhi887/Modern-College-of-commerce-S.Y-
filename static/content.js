document.addEventListener('DOMContentLoaded',function(){
    history.pushState({}, '');
})

window.addEventListener('popstate',function(){
    window.location.href='/?lstate=True'
})