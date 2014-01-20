addPeople = function(d){
d.sort(function(a,b){
    console.log(a,b);
    return  b['date']['$date']+a['date']['$date'];
})
for(item in d){
$('#activityFeed').append(
"    <div class='container'>"+
"        <div class='media'>"+
"            <a class='pull-left' href='#'>"+
"                <img class='media-object' src=" + d[item]['picture'] +"></img>"+
"            </a>"+
"            <div class='media-body'>"+
"                <h4 class='media-heading media-heading-bold'>"+d[item]['name'] + "</h4>"+
d[item]['message'] +
"                <h5 class='activityFeedDate'>"+ new Date(d[item]['date']['$date']) + "</h5>"+
"            </div>"+
"        </div>"+
"    </div>"
)
}
}
$(document).ready(function(){
})
