addPeople = function(){
for(i = 0; i < 5; i++){
$('#activityFeed').append(
"    <div class='container'>"+
"        <div class='media'>"+
"            <a class='pull-left' href='#'>"+
"                <div class='media-object' alt='pumpkinstin'></div>"+
"            </a>"+
"            <div class='media-body'>"+
"                <h4 class='media-heading media-heading-bold'>John Pumpkinstin</h4>"+
"                I like to eat pumpkins."+
"                <h5 class='activityFeedDate'>January 18th, 2014</h5>"+
"            </div>"+
"        </div>"+
"    </div>"
)
}
}
$(document).ready(function(){
    addPeople();
})
