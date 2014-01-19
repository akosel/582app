$(document).on('click','i.fa-square',function(){
    
    $(this).removeClass('fa-square');
    $(this).addClass('fa-check-square');
   
});

$(document).on('click','i.fa-check-square',function(){
    $(this).removeClass('fa-check-square');
    $(this).addClass('fa-square');    
    $('#shareForm'+$(this).attr('id')).remove(); 
});

$(document).on('click','button.notNow',function(){
    $(this).parent().parent().parent().remove();
})

$(document).ready(function(){
});
// JavaScript Document