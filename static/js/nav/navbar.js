$(document).ready(function(){
$('#navbar').html( 
"    <nav class='navbar navbar-inverse navbar-static-top' role='navigation'>"+
"        <div class='navbar-header'>"+
"            <button type='button' class='navbar-toggle navbar-left' data-toggle='collapse' data-target='#bs-example-navbar-collapse-1'>"+
"             <span class='sr-only'>Toggle navigation</span>"+
"              <span class='icon-bar'></span>"+
"              <span class='icon-bar'></span>"+
"              <span class='icon-bar'></span>"+
"            </button>"+
"        <a class='navbar-brand' href='/'>Mesh</a>"+
"        </div>"+
"        <div class='collapse navbar-collapse' id='bs-example-navbar-collapse-1'>"+
"            <ul class='nav navbar-nav'>"+
"                <li><a href='/dashboard/'>Dashboard</a></li>"+
"                <li><a href='/goals/'>Goals</a></li>"+
"                <li><a href='/friends/'>Friends</a></li>"+
"            </ul>"+
"         <ul class='nav navbar-nav navbar-right' id='back'>"+
"          <li><a href='/home.html'>Signout</a></li>"+
"         </ul> "+ 
"        </div><!-- /.navbar-collapse -->"+
"    </nav>"
)
})