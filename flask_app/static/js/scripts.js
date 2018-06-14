function myFunction() {
    var x = document.getElementById("nav_menu_item");
    if (x.className === "nav_menu_item") {
        x.className += " responsive";
    } else {
        x.className = "nav_menu_item";
    }
}
