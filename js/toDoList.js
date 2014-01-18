addItems = function(){
for(i = 0; i < 5; i++){
$('#toDoList').append(
"    <div class='container'>"+
"        <div class='media'>"+
"            <a class='pull-left' href='#'>"+
"                <i class='fa-media-object fa fa-square-o fa-4x'></i>"+
"            </a>"+
"            <div class='media-body'>"+
"                 <h5>February 1, 2014</h5>"+
"                <h4 class='media-heading'>Run "+ Math.ceil(Math.random()*10)  +"</h4>"+
"                Part of my training program"+
"            </div>"+
"        </div>"+
"    </div>"
)
}
}
$(document).ready(function(){
    addItems();
});
