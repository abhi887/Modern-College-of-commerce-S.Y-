document.addEventListener('DOMContentLoaded',function(){
    history.pushState({},'')
})

window.addEventListener('popstate',function(){
    var lstate=document.querySelector("#lstate").innerHTML
    if(lstate !== 'False'){
    window.location.href='home'
    }
})