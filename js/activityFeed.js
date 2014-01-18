addPeople = function(){
for(i = 0; i < 5; i++){
$('#activityFeed').append(
"    <div class='container'>"+
"        <div class='media'>"+
"            <a class='pull-left' href='#'>"+
"                <img class='media-object' src='/img/john.jpeg' alt='pumpkinstin'>"+
"            </a>"+
"            <div class='media-body'>"+
"                <h4 class='media-heading'>John Pumpkinstin</h4>"+
"                I like to eat pumpkins."+
"            </div>"+
"        </div>"+
"    </div>"
)
}
}
$(document).ready(function(){
    addPeople();
})
