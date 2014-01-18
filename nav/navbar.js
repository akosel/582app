$(document).ready(function(){
$('#navbar').html( 
"    <nav class='navbar navbar-inverse navbar-fixed-top' role='navigation'>"+
"        <div class='navbar-header'>"+
"            <button type='button' class='navbar-toggle navbar-left' data-toggle='collapse' data-target='#bs-example-navbar-collapse-1'>"+
"             <span class='sr-only'>Toggle navigation</span>"+
"              <span class='icon-bar'></span>"+
"              <span class='icon-bar'></span>"+
"              <span class='icon-bar'></span>"+
"            </button>"+
"        <a class='navbar-brand' href='#'>Mesh</a>"+
"        </div>"+
"        <div class='collapse navbar-collapse' id='bs-example-navbar-collapse-1'>"+
"            <ul class='nav navbar-nav'>"+
"                <li><a href='/newgoal'>New Goal</a></li>"+
"                <li><a href='/brainstorm'>Brainstorm</a></li>"+
"                <li><a href='/goalrequests'>Goal Requests</a></li>"+
"                <li><a href='/missedgoals'>Missed Goals</a></li>"+
"                <li><a href='/todo'>To Do</a></li>"+
"                <li><a href='/completedgoals'>Completed Goals</a></li>"+
"            </ul>"+
"            <ul class='nav navbar-nav navbar-right' id='back'>"+
"                <li><a href='/'>Back</a></li>"+
"            </ul>"+
"        </div><!-- /.navbar-collapse -->"+
"    </nav>"
)
});
