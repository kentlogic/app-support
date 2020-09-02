function modalSwitcher(id){
    var modal = document.getElementById(id)

    if(modal.classList.contains("is-active")){
        modal.classList.remove("is-active")
    }
    else{
        modal.classList.add("is-active")
    }
}
