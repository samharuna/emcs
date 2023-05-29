$(document).ready(function(){
    // START COMMENT
    $('.commentlikes-form').submit(function (e){
        e.preventDefault();
        const commentlikes_id = $(".likes-btn").val();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const url = $(this).attr('action');
        
        $.ajax({
            method: "POST",
            url: url,
            headers: { "X-CSRFToken": token },
            data: {"commentlikes_id": commentlikes_id },
            success: function(response){
                if(response.liked === true){
                    $(".likes-icon").addClass("text-success");
                }
                else{
                    $(".likes-icon").removeClass("text-success")
                };
                likes = $(".likes-count").text(response.likes_count)
                parseInt(likes)
            },
            error: function(response){
                console.log('Failed', response);
            }
        });
    });

    $('.commentdislikes-form').submit(function(e){
        e.preventDefault();
        const commentdislike_id = $('.dislikes-btn').val();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const url = $(this).attr('action')

        $.ajax({
            method: "POST",
            url: url,
            headers: {"X-CSRFToken": token },
            data: {'commentdislike_id': commentdislike_id},
            success: function(response){
                if(response.disliked === true){
                    $(".dislikes-icon").addClass('text-danger');
                }
                else{
                    $(".dislikes-icon").removeClass("text-danger");
                }
                dislikes = $(".dislikes-count").text(response.dislikes_Count)
                parseInt(dislikes)
            },
            error: function(response){
                console.log('Failed', response)
            },
        });
    });
    // END COMMENT

    // START REPLY
    $(".replylikes-form").submit(function(e){
        e.preventDefault();
        const replylikes_id = $(".replylikes-btn").val();
        const token = $("input[name=csrfmiddlewaretoken]").val();
        const url = $(this).attr('action')
        
        $.ajax({
            method: "POST",
            url: url,
            headers: { "X-CSRFToken": token},
            data: { replylikes_id: replylikes_id},
            success: function(response){
                if(response.replylikes === true){
                    $(".replylikes-icon").addClass('text-success');
                }else{
                    $(".replylikes-icon").removeClass("text-success");
                };
                
                replylikes = $(".replylikes-count").text(response.replylikes_count)
                parseInt(replylikes)
            },
            error: function(response){
                console.log("Failed", response);
            },
        });
    });

    $(".replydislikes-form").submit(function(e){
        e.preventDefault();
        const dislikesreply_id = $(".dislikes-reply-btn").val();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const url = $(this).attr('action')
        
        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {'dislikesreply_id':dislikesreply_id},
            success: function(response){
                if(response.replydislikes === true){
                    $(".dislikesreply-icon").addClass('text-danger');
                }else{
                    $(".dislikesreply-icon").removeClass("text-danger");
                }
                console.log('Suceess', response);
                replydislikes = $(".replydislikes-count").text(response.replydislikes_count)
                parseInt(replydislikes)
            },
            error: function(response){
                console.log("Failed", response);
            },
        });
    });
    // END REPLY

});

