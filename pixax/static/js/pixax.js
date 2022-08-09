breakpoint_phone = 768
breakpoint_desktop = 1020

window.addEventListener("load", init)

function init() {
    setup_help_icons()
    setup_errored_inputs()
    setup_phone_toggle_menu()
}

/* Toggling the phone menu */

function setup_phone_toggle_menu() {
    window.addEventListener('resize', close_phone_toggle_menu_if_not_phone)
    let menu_icon = document.querySelector(".menu_icon");
    menu_icon.addEventListener('click', toggle_phone_menu);
    let item_list_links = document.querySelectorAll("ul.item_list li a");
    for (let i=0; i < item_list_links.length; i++) {
        item_list_links[i].addEventListener("focus", open_toggle_phone_menu_if_phone)
    }
}

function open_toggle_phone_menu_if_phone(e) {
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.add("open")
}

function toggle_phone_menu() {
    let item_list = document.querySelector(".item_list");
    if (item_list.classList.contains("open")) {
        item_list.classList.remove("open")
    }
    else {
        item_list.classList.add("open")
    }
}

function close_phone_toggle_menu_if_not_phone() {
    open_item_list = document.querySelector(".item_list_open");
    
    if (!!open_item_list && window.innerWidth > breakpoint_phone){
        open_item_list.classList.remove("item_list_open");
    }
}

/* Updating forms that are corrected */

function setup_errored_inputs() {
    let errored_inputs = document.querySelectorAll(".field_has_error input, .field_has_error textarea")

    for(let i =0; i < errored_inputs.length; i++) {
        errored_inputs[i].addEventListener("change", remove_field_error)
    }
}

function remove_field_error(e) {
    errored_input = e.target;
    form_input_container = errored_input.closest(".form_element_container")
    form_input_container.classList.remove("field_has_error")
}

/* Allow help icons to show information on hover */

function setup_help_icons() {
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