function menuFunction() {
    var x = document.getElementById("nav_menu_item");
    if (x.className === "nav_menu_item") {
        x.className += " responsive";
    } else {
        x.className = "nav_menu_item";
    }
}

$(document).ready(function(){

  $("name").click(function(){
    $("i").toggleClass("fa-caret-up");
    $(".update-form").slideToggle("medium");
    $(".update-button").slideToggle("medium");
  });

  $(".fa-vial").click(function(){
    $(this).toggleClass("coloured");
    $(this).next().toggleClass("coloured");
  });

});
