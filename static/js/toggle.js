jQuery(document).ready(function() {
  jQuery("#comments").hide();
  //toggle the componenet with class msg_body
  jQuery(".unread").click(function()
  {
    jQuery(this).next("#comments").slideToggle(500); 
	
	if( $("#task-box-wrapper").height() < 340) {
		jQuery("#task-box-wrapper").height(340);}
	
	else if( $("#task-box-wrapper").height() == 340) {
		jQuery("#task-box-wrapper").height(190);}
		
	if ( $("#task-checkboxBox").height() < 350) {
		jQuery("#task-checkboxBox").height(350);}
	
	else if( $("#task-checkboxBox").height() == 350) {
		jQuery("#task-checkboxBox").height(200);}
		
	
  });
 
});