$(document).ready(function() {

  $(".fa-vial").click(function() {
    if ($(this).attr("user_id") != "None") {

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


$(document).ready(function() {
  // Stripe scripts //

  var stripe = Stripe('pk_live_EZhLMGAOseTvlfnVF9o6WvIL');
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  if($(window).width() < 600) {
    var style = {
      base: {
        // Add your base input styles here. For example:
        fontSize: '12px',
        color: "#32325d",
        fontFamily: "Raleway",
        fontSmoothing: 'antialiased',
        iconColor: '#AD5DD6',
      }
    };
  } else {
    var style = {
      base: {
        // Add your base input styles here. For example:
        fontSize: '20px',
        color: "#32325d",
        fontFamily: "Raleway",
        fontSmoothing: 'antialiased',
        iconColor: '#AD5DD6',
      }
    };
  }

  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');

  card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Create a token or display an error when the form is submitted.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the customer that there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  var token_submit = document.getElementById('card_token')
  token_submit.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}

});
