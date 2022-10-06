const breakpoint_phone = 768
const breakpoint_desktop = 1020

window.addEventListener("DOMContentLoaded", init)

function init() {
    setup_text_copier()
    setup_organise_form()
    setup_multiple_select()
    setup_form_popup()
    setup_help_icons()
    setup_errored_inputs()
    setup_phone_toggle_menu()
    setup_profile_toggle_menu()
    setup_slideshow()
}

/* Setup text copiers */

function setup_text_copier(){
    let text_copier_buttons = document.querySelectorAll(".text_copier button") as NodeListOf<HTMLElement>
    for(let i=0; i<text_copier_buttons.length; i++){
        text_copier_buttons[i].addEventListener("click",copy_text_to_clipboard)
    }
}

function copy_text_to_clipboard(e: MouseEvent){
    let text_copy_button = e.target as HTMLElement
    let text_copy_div = text_copy_button.closest(".text_copier") as HTMLElement
    let text_copy_input = text_copy_div.querySelector("input") as HTMLInputElement
    navigator.clipboard.writeText(text_copy_input.value);
    alert("Link copied to clipboard")
}


/* Setup organise form */

function setup_organise_form(){
    let star_rating_ui = document.querySelector(".star_rating") as HTMLElement
    if (!!star_rating_ui){
        star_rating_ui.addEventListener("click", update_rating)
        star_rating_ui.classList.remove("inactive")
    }
    let album_list_ui = document.querySelector(".out_of_form.checkbox_container")
    if (!!album_list_ui){
        album_list_ui.classList.remove("inactive")
        let album_list_checkboxes = album_list_ui.querySelectorAll("input")
        for(let i=0; i < album_list_checkboxes.length; i++){
            album_list_checkboxes[i].addEventListener("change", update_albums)
        }
        
    }
}

function update_rating(e: MouseEvent){
    let star_rating_element = e.target as HTMLElement
    let element_x = star_rating_element.getBoundingClientRect().left
    let click_x_pos_pixels = e. clientX - element_x
    let precise_percentage = click_x_pos_pixels / star_rating_element.getBoundingClientRect().width * 100
    let percentage_rounded = Math.round(precise_percentage/5)*5
    let star_visual = star_rating_element.querySelector(".star_visual") as HTMLElement
    star_visual.style.background = "linear-gradient(to right, #f0e464 0%,#f0e464 "+ percentage_rounded +"%,rgba(255, 255, 255, 0.75) "+ percentage_rounded +"%,rgba(255, 255, 255, 0.75) 100%)"
    
    let form_rating = document.getElementById("id_rating") as HTMLInputElement
    form_rating.value = percentage_rounded.toString()
}

function update_albums(e: Event){
    let checkbox = e.target as HTMLInputElement
    let checkbox_value = checkbox.value
    let checkbox_checked = checkbox.checked
    
    let equivalent_checkbox = document.querySelector("form input[type=checkbox][value='"+ checkbox_value + "']") as HTMLInputElement
    equivalent_checkbox.checked = checkbox_checked
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

function toggle_multiple_select(e: MouseEvent){
    if(e.buttons === 1){
        e.preventDefault()
        let option = e.target as HTMLOptionElement
        // let multiple_select = option.closest("select")
        if(option.selected){
            option.selected = false
        }else{
            option.selected = true
        }
    }
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
    let form_popup_close_buttons = document.querySelectorAll(".popup .close_button") as NodeListOf<HTMLElement>
    for(let i=0; i<form_popup_close_buttons.length; i++){
        form_popup_close_buttons[i].addEventListener("click", close_button_close_form_popup)
    }
}

function open_form_popup(){
    let form_popup = document.querySelector(".form_popup") as HTMLElement
    let backgroundUI = document.querySelectorAll(".main, .navbar_wrapper") as NodeListOf<HTMLElement>
    form_popup.classList.add("open");
    for(let i=0; i< backgroundUI.length; i++){
        backgroundUI[i].inert = true
        console.log(backgroundUI[i])
    }
}

function close_button_close_form_popup(e: MouseEvent){
    let close_button = e.target as HTMLElement
    let backgroundUI = document.querySelectorAll(".main, .navbar_wrapper") as NodeListOf<HTMLElement>
    let popup = close_button.closest(".popup") as HTMLElement
    popup.classList.remove("open")
    for(let i=0; i< backgroundUI.length; i++){
        backgroundUI[i].inert = false
    }
}

/* Setup slideshow */

function setup_slideshow() {
    let slideshow = document.querySelector(".slideshow_presentation") as HTMLElement
    if(!!slideshow){
        set_slide_timeout()
    }
}

function set_slide_timeout(){
    setTimeout(change_slide, ((window as any).seconds_between_slides as number)*1000);
}

function change_slide(){
    let previous_slide = document.querySelector(".slideshow_presentation .slide.previous") as HTMLElement
    if (!!previous_slide)
        previous_slide.classList.remove("previous")

    let current_slide = document.querySelector(".slideshow_presentation .slide.current") as HTMLElement
    current_slide.classList.add("previous")
    current_slide.classList.remove("current")

    let slides = document.querySelectorAll(".slideshow_presentation .slide")
    let amount_slides = slides.length;
    let current_slide_number = Array.prototype.indexOf.call(slides, current_slide)
    let new_slide_number = current_slide_number+1
    if(new_slide_number == amount_slides){
        new_slide_number = 0
    }
    let new_slide = slides[new_slide_number]
    new_slide.classList.add("current")

    set_slide_timeout()
}

/* Toggling the profile menu */

function setup_profile_toggle_menu() {
    let menu_icon = document.querySelector(".profile_icon") as HTMLElement
    if(!!menu_icon){
        menu_icon.addEventListener("click", menu_icon_toggle_profile_menu)
        let profile_list_links = document.querySelectorAll("ul.profile_list li a");
        for (let i=0; i < profile_list_links.length; i++) {
            profile_list_links[i].addEventListener("focus", link_focus_open_profile_menu)
            profile_list_links[i].addEventListener("blur", link_blur_close_profile_menu)
        }    
    }
}

function menu_icon_toggle_profile_menu(e: MouseEvent){
    let profile_list = document.querySelector(".profile_list") as HTMLElement
    toggle_menu(profile_list)
}

function link_focus_open_profile_menu(e: Event){
    close_open_nav_bar_menus()
    let link = e.target as HTMLElement
    let menu = link.closest("ul") as HTMLElement
    menu.classList.add("open")
}

function link_blur_close_profile_menu(e: Event){
    let link = e.target as HTMLElement
    let menu = link.closest("ul") as HTMLElement
    menu.classList.remove("open")
}

/* Toggling the phone menu */

function setup_phone_toggle_menu() {
    window.addEventListener('resize', resize_close_phone_toggle_menu_if_not_phone)
    let menu_icon = document.querySelector(".menu_icon")
    if(!!menu_icon){
        menu_icon.addEventListener('click', toggle_phone_menu)
        let item_list_links = document.querySelectorAll("ul.item_list li a");
        for (let i=0; i < item_list_links.length; i++) {
            item_list_links[i].addEventListener("focus", link_focus_open_phone_menu_if_phone)
            item_list_links[i].addEventListener("blur", link_blur_close_phone_menu)
        }
    }
}

function link_focus_open_phone_menu_if_phone(e: Event) {
    close_open_nav_bar_menus()
    if (window.innerWidth <= breakpoint_phone) {
        let link = e.target as HTMLElement
        let menu = link.closest("ul") as HTMLElement
        menu.classList.add("open")
    }
}

function link_blur_close_phone_menu(e: Event) {
    let link = e.target as HTMLElement
    let menu = link.closest("ul") as HTMLElement
    menu.classList.remove("open")
}

function toggle_phone_menu() {
    let item_list = document.querySelector(".item_list") as HTMLElement;
    toggle_menu(item_list)
}

function resize_close_phone_toggle_menu_if_not_phone() {
    let open_item_list = document.querySelector(".item_list.open");
    
    if (!!open_item_list && window.innerWidth > breakpoint_phone){
        open_item_list.classList.remove("open");
    }
}

/* Menu functions */

function toggle_menu(menu: HTMLElement) {
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
    let errored_inputs = document.querySelectorAll(".field_has_error input, .field_has_error textarea") as NodeListOf<HTMLInputElement>

    for(let i =0; i < errored_inputs.length; i++) {
        errored_inputs[i].addEventListener("change", remove_field_error)
    }
}

function remove_field_error(e: Event) {
    let errored_input = e.target as HTMLInputElement;
    let form_input_container = errored_input.closest(".form_element_container") as HTMLElement
    form_input_container.classList.remove("field_has_error")
}

/* Allow help icons to show information on hover */

function setup_help_icons() {
    let help_icons_elements = document.getElementsByClassName("help_text_icon") as HTMLCollectionOf<HTMLElement>
    
    for(let i = 0; i < help_icons_elements.length; i++) {
        help_icons_elements[i].addEventListener("mouseover", reveal_help_text)
        help_icons_elements[i].addEventListener("mouseout", hide_help_text)
    }
}

function reveal_help_text(e: MouseEvent) {
    let help_text = getHelpText(e)
    help_text.classList.add("help_text_open")
}

function hide_help_text(e: MouseEvent) {
    let help_text = getHelpText(e)
    help_text.classList.remove("help_text_open")
}

function getHelpText(e: Event):HTMLElement {
    let help_icon_element = e.target as HTMLElement
    let form_element_container = help_icon_element.closest(".form_element_container") as HTMLElement
    let help_text = form_element_container.getElementsByClassName("help_text")[0] as HTMLElement
    return help_text
}