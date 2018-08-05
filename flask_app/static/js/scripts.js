$(document).ready(function() {

  $(".fa-vial").click(function() {
    if ($(this).attr("user_id") != "not_authenticated") {

      var project_identity = $(this).attr("project_id")

      if ($(this).next().attr("class") == "coloured" ) {
        var current_score = parseInt($(this).next().text())
        subtract_score = current_score - 1
        $(this).next().text(subtract_score)
        $([project_id = project_identity]).next().text(subtract_score)
      } else {
        var current_score = parseInt($(this).next().text())
        add_score = current_score + 1
        $(this).next().text(add_score)
      }

      $(this).toggleClass("coloured");
      $(this).next().toggleClass("coloured");

      $.post("/tubes/" + $(this).attr("project_id") + "/" + $(this).attr("user_id"), {
                  user_id: $(this).attr("user_id"),
                  project_id: $(this).attr("project_id")
              });
      }
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
