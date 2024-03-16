$(document).ready(function(){
    $("#newsletterForm").submit(function(e){
        e.preventDefault();
        const email     = $("#email").val();
        const token     = $("input[name=csrfmiddlewaretoken]").val();
        const url       = $(this).attr("action");
        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {
                'email': email,
            },
            success: function(response){
                $('h3').html(response);
                $("#newsletterForm").trigger('reset');
            },
            error: function(error){
                alert('Your email address already exists for our Newsletter subscription')
            },
        })
    })
})