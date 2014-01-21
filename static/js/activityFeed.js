addPeople = function(d){
d.sort(function(a,b){
    return b['date']['$date']-a['date']['$date']
})
for(item in d){
htmlStr = 
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
"        </div>"

if ('type' in d[item]){
    if (d[item]['type'] == 'friendrequest'){
        htmlStr +=
            "   <button id='reject' class='btn btn-warning pull-right'>Reject</button>"+
            "   <button id='accept' class='btn btn-primary pull-right'>Accept</button>"+
            "    </div>"
        
        $('#activityFeed').append(htmlStr)
    }
    else{
        $('#activityFeed').append(htmlStr+'</div>')
    }
}
else{
}
}
}
$(document).on('click','button#accept',function(){
    //TODO add username to message to help make this way easier.
    url = '/acceptfriendreq/' + username 
    $.get(url)
    $(this).parent().remove(); 
    //refresh the feed
    addPeople(d.newsfeed)
})
