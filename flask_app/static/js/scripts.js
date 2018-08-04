$(document).ready(function() {

  $(".fa-vial").click(function() {
    $(this).toggleClass("coloured");
    $(this).next().toggleClass("coloured");
    //Add a for loop to add and subtract votes as the user clicks

    $.post("/tubes/" + $(this).attr("project_id") + "/" + $(this).attr("user_id"), {
                user_id: $(this).attr("user_id"),
                project_id: $(this).attr("project_id")
            });
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
