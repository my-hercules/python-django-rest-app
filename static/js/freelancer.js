function updateHeroDiv()
{
    var aspect_ratio = 1.18; /* or whatever yours is */
    var new_hero_height = ($(".agency_field").width()*aspect_ratio);
    $(".agency_field").height(new_hero_height);
    $(".freelancer_field").height(new_hero_height);
}

function setType(pStr)
{
    $("#mylist-1").html(pStr);
    $("#list-2").html(pStr=='Freelance'?'Company':'Freelance');
    if(pStr == "Company")
        $("#txtcompanyname").css("visibility","visible");
    else{
        $("#txtcompanyname").css("visibility","hidden");
        $("#txtcompanyname").val("");
    }
}

$(document).ready(function() 
{       
    // calls the function on page load
    updateHeroDiv(); 
    nextTab(1);

    $("#list-2").css("visibility","hidden");
    // calls the function on window resize
    $(window).on("resize", function ()
    {
        updateHeroDiv();       
    })
    $("#mylist-1").on("click",function(){
        if($("#list-2").css("visibility")=="visible"){
            $("#list-2").css("visibility","hidden");
            $("#btn-list").css("height","80px");
        }
        else{
            $("#list-2").css("visibility","visible");
            $("#btn-list").css("height","130px");
        }
    })
    $("#list-2").on("click",function()
    {
        var sText = $("#mylist-1").text();
        $("#mylist-1").html($("#list-2").text());
        $("#list-2").html(sText);
        if(sText == "Freelance")
            $("#txtcompanyname").css("visibility","visible");
        else{
            $("#txtcompanyname").css("visibility","hidden");
            $("#txtcompanyname").val("");
        }
    })
    $(document).on('click touchstart', function(e) {
        var mylist = $("#mylist-1");
        if (!mylist.is(e.target) ) {
            $("#list-2").css("visibility","hidden");
            $("#btn-list").css("height","80px");
        }
    })
    //Form Validation
    //$("#sign-submit-button").on("click",function(){
    //    submit();
    //})

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

        $('#sign-submit-button').text('Sign In');
        $('#signform').attr('action','/loginuser/')
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
        $('#sign-submit-button').text('Sign Up');
        $('#signform').attr('action','/register/')
    }
}