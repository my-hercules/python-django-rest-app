
$(document).ready(function() 
{
    $( "form" ).keydown(function( event ) {
      if ( event.which == 13 ) {
        if (!$(document.activeElement).is('textarea'))
            event.preventDefault();
      }
    });
    $('form').submit(function () {
      if ($(document.activeElement).attr('type') == 'submit')
         return true;
      else return false;
    });
});

function nextTab(pTab)
{
    if(pTab == 2)
    {
        $('#h2-signin').attr('class', 'h2-signup');
        $('#h2-signup').attr('class','h2-signin');
        $('#signup').removeClass('sign-margin');
        $('#signup').removeClass('sign-margin-left');
        $('#signin').addClass('sign-margin');
        $('#signin').addClass('sign-margin-right');
        $('#signup-content').addClass('sign-content');
        $('#signin-content').removeClass('sign-content');
        $('#stripe-blue-left').css('visibility','hidden');
        $('#stripe-blue-right').css('visibility','visible');

        $('#btn-list').css('visibility','hidden');
        $('#text-company').css('visibility','hidden');

        $('#sign-submit-button').text('SIGN IN');
        $('#sign-submit-button').attr('name',"signin");
        //$('#signform').attr('action','/loginuser/')
    }
    else
    {
        $('#h2-signin').attr('class', 'h2-signin');
        $('#h2-signup').attr('class','h2-signup');
        $('#signup').addClass('sign-margin');
        $('#signup').addClass('sign-margin-left');
        $('#signin').removeClass('sign-margin');
        $('#signin').removeClass('sign-margin-right');
        $('#signin-content').addClass('sign-content');
        $('#signup-content').removeClass('sign-content');
        $('#stripe-blue-left').css('visibility','visible');
        $('#stripe-blue-right').css('visibility','hidden');

        $('#btn-list').css('visibility','visible');
        $('#text-company').css('visibility','visible');
        $('#sign-submit-button').text('SIGN UP');
        $('#sign-submit-button').attr('name',"signup");
        //$('#signform').attr('action','/register/')
    }
}