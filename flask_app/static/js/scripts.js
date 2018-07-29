$(document).ready(function() {

  $("name").click(function() {
    $("i").toggleClass("fa-caret-up");
    $(".update-form").slideToggle("medium");
    $(".update-button").slideToggle("medium");
  });

  $(".fa-vial").click(function() {
    $(this).toggleClass("coloured");
    $(this).next().toggleClass("coloured");
  });

  $(".fa-plus").click(function() {
    $(this).toggleClass("coloured");
    $(".plus_circle").toggle();
    $(".create_dropdown").toggle();
  });

  $(".fa-user-circle").click(function() {
    $(this).toggleClass("coloured");
    $(".account_circle").toggle();
    $(".account_dropdown").toggle();
  });

  $(".user_img").click(function() {
    $(this).toggleClass("coloured");
    $(".account_circle").toggle();
    $(".account_dropdown").toggle();
  });

  $("body").click(function(e) {
     if(!$(e.target).hasClass("fa-plus") )
     {
         $(".create_dropdown").hide();
         $(".plus_circle").hide();
         $(".fa-plus").removeClass("coloured")
     }
  });

  $("body").click(function(e) {
     if(!$(e.target).hasClass("click_user") )
     {
         $(".account_dropdown").hide();
         $(".account_circle").hide();
         $(".user_img").removeClass("coloured")
     }
  });

});

$('.wrapper').css('padding-bottom', $('footer').height());
$('footer').css('margin-top', -$('footer').height());
