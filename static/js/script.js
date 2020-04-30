
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
//
$(document).ready(function(){
  $('#myTab a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
  });
});

// $('#myTab a[href="#profile"]').tab('show') // Select tab by name
// $('#myTab li:first-child a').tab('show') // Select first tab
// $('#myTab li:last-child a').tab('show') // Select last tab
// $('#myTab li:nth-child(3) a').tab('show') // Select third tab
