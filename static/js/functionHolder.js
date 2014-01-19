$(document).on('click','i.fa-square-o',function(){
    
    $(this).removeClass('fa-square-o');
    $(this).addClass('fa-check-square-o');
    $(this).parent().append(
        "<div id='shareForm"+$(this).attr('id') + "'>"+
        "<textarea class='form-control' placeholder='Say something about this!' rows='3'></textarea>"+
        "<button type='button'  class='btn btn-default btn-brown btn-square'>Share</button>"+
        "<button type='button' id='notNow"+ $(this).attr('id') + "' class='btn btn-default btn-square notNow'>Not Now</button>"+
        "</div>"
    )
});

$(document).on('click','i.fa-check-square-o',function(){
    $(this).removeClass('fa-check-square-o');
    $(this).addClass('fa-square-o');    
    $('#shareForm'+$(this).attr('id')).remove(); 
});

$(document).on('click','button.notNow',function(){
    $(this).parent().parent().parent().remove();
})

$(document).ready(function(){
});
