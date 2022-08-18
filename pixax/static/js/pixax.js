const breakpoint_phone = 768
const breakpoint_desktop = 1020

window.addEventListener("load", init)

function init() {
    setup_multiple_select()
    setup_file_inputs()
    setup_form_popup()
    setup_help_icons()
    setup_errored_inputs()
    setup_phone_toggle_menu()
    setup_profile_toggle_menu()
    setup_slideshow()
}

/* Setup select inputs */

function setup_multiple_select(){
    let multiple_selects = document.querySelectorAll("select[multiple]")
    for(let i=0; i<multiple_selects.length; i++){
        multiple_selects[i]
        let options = multiple_selects[i].querySelectorAll("option");
        for (let j = 0; j < options.length; j++) {
            options[j].addEventListener("mousedown", toggle_multiple_select)
        }
        multiple_selects[i].classList.add("enabled")
    }
}

function toggle_multiple_select(e){
    if(e.buttons === 1){
        e.preventDefault()
        option = e.target
        multiple_select = option.closest("select")
        if(option.selected){
            option.selected = false
        }else{
            option.selected = true
        }
    }
}

/* Setup file inputs */

function setup_file_inputs(){
    let file_inputs = document.querySelectorAll("input[type=file]")
    for(let i=0; i<file_inputs.length; i++){
        file_inputs[i].addEventListener("change", file_input_display)
    }
}

function file_input_display(e){
    console.log(e.target)
}

/* Setup form popup button */

function setup_form_popup(){
    let popup_form_with_error = document.querySelector(".popup_has_error")
    if(popup_form_with_error){
        open_form_popup()
    }
    let form_popup_button = document.querySelector(".form_popup_button")
    if(!!form_popup_button){
        form_popup_button.addEventListener("click", open_form_popup)
    }
    let form_popup_close_buttons = document.querySelectorAll(".popup .close_button")
    for(let i=0; i<form_popup_close_buttons.length; i++){
        form_popup_close_buttons[i].addEventListener("click", close_button_close_form_popup)
    }
}

function open_form_popup(){
    let form_popup = document.querySelector(".form_popup")
    let backgroundUI = document.querySelectorAll(".main, .navbar_wrapper")
    form_popup.classList.add("open");
    for(let i=0; i< backgroundUI.length; i++){
        backgroundUI[i].inert = true
        console.log(backgroundUI[i])
    }
}

function close_button_close_form_popup(e){
    let close_button = e.target;
    let backgroundUI = document.querySelectorAll(".main, .navbar_wrapper")
    let popup = close_button.closest(".popup")
    popup.classList.remove("open")
    for(let i=0; i< backgroundUI.length; i++){
        backgroundUI[i].inert = false
        console.log(backgroundUI[i])
    }
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
    if(!!menu_icon){
        menu_icon.addEventListener("click", menu_icon_toggle_profile_menu)
        let profile_list_links = document.querySelectorAll("ul.profile_list li a");
        for (let i=0; i < profile_list_links.length; i++) {
            profile_list_links[i].addEventListener("focus", link_focus_open_profile_menu)
            profile_list_links[i].addEventListener("blur", link_blur_close_profile_menu)
        }    
    }
}

function menu_icon_toggle_profile_menu(e){
    let profile_list = document.querySelector(".profile_list")
    toggle_menu(profile_list)
}

function link_focus_open_profile_menu(e){
    close_open_nav_bar_menus()
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.add("open")
}

function link_blur_close_profile_menu(e){
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.remove("open")
}

/* Toggling the phone menu */

function setup_phone_toggle_menu() {
    window.addEventListener('resize', resize_close_phone_toggle_menu_if_not_phone)
    let menu_icon = document.querySelector(".menu_icon")
    menu_icon.addEventListener('click', toggle_phone_menu)
    let item_list_links = document.querySelectorAll("ul.item_list li a");
    for (let i=0; i < item_list_links.length; i++) {
        item_list_links[i].addEventListener("focus", link_focus_open_phone_menu_if_phone)
        item_list_links[i].addEventListener("blur", link_blur_close_phone_menu)
    }
}

function link_focus_open_phone_menu_if_phone(e) {
    close_open_nav_bar_menus()
    if (window.innerWidth <= breakpoint_phone) {
        let link = e.target
        let menu = link.closest("ul")
        menu.classList.add("open")
    }
}

function link_blur_close_phone_menu(e) {
    let link = e.target
    let menu = link.closest("ul")
    menu.classList.remove("open")
}

function toggle_phone_menu() {
    let item_list = document.querySelector(".item_list");
    toggle_menu(item_list)
}

function resize_close_phone_toggle_menu_if_not_phone() {
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
    let open_menus = document.querySelectorAll(".navbar .open")
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