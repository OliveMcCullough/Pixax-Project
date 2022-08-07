window.addEventListener("load", init)

function init() {
    let help_icons_elements = document.getElementsByClassName("help_text_icon")
    
    for(let i = 0; i < help_icons_elements.length; i++) {
        help_icons_elements[i].addEventListener("mouseover", reveal_help_text)
        help_icons_elements[i].addEventListener("mouseout", hide_help_text)
    }
}

function reveal_help_text(e) {
    help_text = getHelpText(e)
    help_text.classList.add("help_text_open")
}

function hide_help_text(e) {
    help_text = getHelpText(e)
    help_text.classList.remove("help_text_open")
}

function getHelpText(e) {
    help_icon_element = e.target
    form_element_container = help_icon_element.closest(".form_element_container")
    return help_text = form_element_container.getElementsByClassName("help_text")[0]
}