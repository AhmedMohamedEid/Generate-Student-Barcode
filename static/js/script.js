
var x_list = document.getElementById("list");
var x_card = document.getElementById("card");

function viewList() {
  x_list.style.display = "block";
  x_card.style.display = "none";
}

function viewCard() {
  x_list.style.display = "none";
  x_card.style.display = "block";
}

function toggle(source) {
  checkboxes = document.getElementsByName('student');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function toggle_1(source) {
  checkboxes = document.getElementsByName('major');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function showButtons (checkbox, box) {

    var chboxs = document.getElementsByName(checkbox);
    var vis = "none";
    for(var i=0;i<chboxs.length;i++) {
        if(chboxs[i].checked){
         vis = "inline-block";
            break;
        }
    }
    document.getElementById(box).style.display = vis;


}

function toggle_2(source) {
  checkboxes = document.getElementsByName('level');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}
//
$(document).ready(function(){
  $('#myTab a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
  });

  $(".basic-search #filter_button").click(function(){
    $("#filter_form").fadeToggle();
  });

  $("#show_nav_toggel").click(function(){
    $("#sidebar").fadeToggle();
  });
  //
  // var x = document.getElementById('sidebar');
  // var button = document.getElementById('show_nav_toggel');
  // console.log(x.style.display);
  //
  // if (x.style.display === "none"){
  //   button.innerHTML = "<i class='fa fa-angle-left'></i>";
  // }else {
  //   button.innerHTML = "<i class='fa fa-angle-right'></i>";
  // }


});


(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

})(jQuery);



// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function checkDelete(){
    return confirm('Are you sure to Delete?');
}
