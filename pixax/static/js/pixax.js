const breakpoint_phone = 768
const breakpoint_desktop = 1020

window.addEventListener("load", init)

function init() {
    setup_help_icons()
    setup_errored_inputs()
    setup_phone_toggle_menu()
    setup_profile_toggle_menu()
    setup_slideshow()
}

/* Setup slideshow */

function setup_slideshow() {
    let slideshow = document.querySelector(".slideshow_presentation")
    if(!!slideshow){
        set_slide_timeout()
    }
}

function set_slide_timeout(){
    setTimeout(change_slide, seconds_between_slides*1000);
}

function change_slide(){
    previous_slide = document.querySelector(".slideshow_presentation .slide.previous")
    if (!!previous_slide)
        previous_slide.classList.remove("previous");

    current_slide = document.querySelector(".slideshow_presentation .slide.current")
    current_slide.classList.add("previous")
    current_slide.classList.remove("current")

    slides = document.querySelectorAll(".slideshow_presentation .slide")
    amount_slides = slides.length;
    current_slide_number = Array.prototype.indexOf.call(slides, current_slide)
    new_slide_number = current_slide_number+1
    if(new_slide_number == amount_slides){
        new_slide_number = 0;
    }
    new_slide = slides[new_slide_number];
    new_slide.classList.add("current");

    set_slide_timeout()
}

/* Toggling the profile menu */

function setup_profile_toggle_menu() {
    let menu_icon = document.querySelector(".profile_icon")
    menu_icon.addEventListener("click", toggle_profile_menu)
    let profile_list_links = document.querySelectorAll("ul.profile_list li a");
    for (let i=0; i < profile_list_links.length; i++) {
        profile_list_links[i].addEventListener("focus", open_profile_menu)
        profile_list_links[i].addEventListener("blur", close_profile_menu)
    }
}

function toggle_profile_menu(e){
    let profile_list = document.querySelector(".profile_list")
    toggle_menu(profile_list)
}

function open_profile_menu(e){
    close_open_nav_bar_menus()
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.add("open")
}

function close_profile_menu(e){
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.remove("open")
}

/* Toggling the phone menu */

function setup_phone_toggle_menu() {
    window.addEventListener('resize', close_phone_toggle_menu_if_not_phone)
    let menu_icon = document.querySelector(".menu_icon")
    menu_icon.addEventListener('click', toggle_phone_menu)
    let item_list_links = document.querySelectorAll("ul.item_list li a");
    for (let i=0; i < item_list_links.length; i++) {
        item_list_links[i].addEventListener("focus", open_phone_menu_if_phone)
        item_list_links[i].addEventListener("blur", close_phone_menu)
    }
}

function open_phone_menu_if_phone(e) {
    close_open_nav_bar_menus()
    if (window.innerWidth <= breakpoint_phone) {
        let link = e.target
        let menu = link.closest("ul")
        menu.classList.add("open")
    }
}

function close_phone_menu(e) {
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.remove("open")
}

function toggle_phone_menu() {
    let item_list = document.querySelector(".item_list");
    toggle_menu(item_list)
}

function close_phone_toggle_menu_if_not_phone() {
    open_item_list = document.querySelector(".item_list.open");
    
    if (!!open_item_list && window.innerWidth > breakpoint_phone){
        open_item_list.classList.remove("open");
    }
}

/* Menu functions */

function toggle_menu(menu) {
    if (menu.classList.contains("open")) {
        menu.classList.remove("open")
    }
    else {
        close_open_nav_bar_menus();
        menu.classList.add("open")
    }
}

function close_open_nav_bar_menus() {
    let open_menus = document.querySelectorAll(".open")
    for(let i=0; i<open_menus.length; i++){
        open_menus[i].classList.remove("open");
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