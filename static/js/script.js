
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

  $(".basic-search #filter_button").click(function(){
    $("#filter_form").fadeToggle();
  });

  $("#show_nav_toggel").click(function(){
    $("#sidebar").fadeToggle();
  });

  var x = document.getElementById('sidebar');
  var button = document.getElementById('show_nav_toggel');
  console.log(x.style.display);

  if (x.style.display === "none"){
    button.innerHTML = "<i class='fa fa-angle-left'></i>";
  }else {
    button.innerHTML = "<i class='fa fa-angle-right'></i>";
  }


});

//
// var x = document.getElementById('sidebar');
// var button = document.getElementById('show_nav_toggel');
// console.log(x.style.display);
// if (x.style.display === "none"){
//   button.innerHTML = "<i class='fa fa-angle-left'></i>";
// }else {
//   button.innerHTML = "<i class='fa fa-angle-right'></i>";
// }

//
// function toggel_filter() {
//   var x = document.getElementById("filter_button");
//   if (x.style.display === "none") {
//     x.style.display = "block";
//   } else {
//     x.style.display = "none";
//   }
// }

// $('#myTab a[href="#profile"]').tab('show') // Select tab by name
// $('#myTab li:first-child a').tab('show') // Select first tab
// $('#myTab li:last-child a').tab('show') // Select last tab
// $('#myTab li:nth-child(3) a').tab('show') // Select third tab


//
// function searchStudent() {
//     // Get List of Channels
//     const request = new XMLHttpRequest();
//     request.open('POST', '/search');
//
//     // Callback function for when request completes
//     request.onload = () => {
//
//     	// Extract JSON data from request
//     	const data = JSON.parse(request.responseText);
//
//     	// Extract list of channels and populate variable and dropdown menu
//     	// if (data.success) {
//     	//     var channels = data["channel_list"];
//     	//     for (var i = 0, len = channels.length; i < len; i++) {
//     	// 	if (channels[i] == global_current_channel){
//     	// 	    add_channel(channels[i], 1);
//     	// 	}
//     	// 	else {
//     	// 	    add_channel(channels[i],0);
//     	// 	}
//     	//     }
//     	// }
//     	// else {
//     	//     console.log("API call failed");
//     	// }
//         }
//
//     // Send request
//     request.send();
// }

// document.getElementById("search_btn").onclick = () => {
//
//   const request = new XMLHttpRequest();
//   request.open('POST', '/search');
//
//   // Callback function for when request completes
//   request.onload = () => {
//
//     // Extract JSON data from request
//     const data = JSON.parse(request.responseText);
//     console.log(data);
//   }
//
//   // Send request
//   request.send();
// };

function studentTableRecord(data) {
  return `
  <tr>
    <td><input type="checkbox" name="student" value="${ data.id }" style="height: .9em;width: .9em;"></td>
    <th scope="row">{{ loop.index + pagination.skip }}</th>
    <td>${ data.un_id }</td>
    <td><a href="{{ url_for('student', id=${ data.id } }}">${ data.name }</a></td>

        <td>${ data.major }</td>
        <td>${ data.level }</td>

    <td>${ data[3] }</td>
    <td>

      <a href="{{ url_for('generate_word_file', id=${ data.id }) }}" class="btn btn-light text-info btn-sm" title="Generate Word File for student data." type="submit" style="cursor: pointer;" name="delete_all"><i class="fas fa-file-word"></i></a>
      <a href="{{ url_for('generate_word_file', id=${ data.id }) }}" class="btn btn-light text-danger btn-sm" title="Generate PDF File for student data." type="submit" style="cursor: pointer;" name="delete_all"><i class="fas fa-file-pdf"></i></a>
      <a href="#"class="btn btn-light text-success btn-sm"  download><span><i class="fas fa-image"></i></span></a>
    </td>
  </tr>
  `;
}

function liveSearch(value){
				value = value.trim(); // remove any spaces around the text
				if(value != ""){ // don't make requests with an empty string
					$.ajax({
						url: "search",
						data: {searchText: value},
						dataType: "json",
						success: function(data){
							var res = "";
							// // create the html with results
							for(i=1; i<data.data.length;i++){
								res += studentTableRecord(data.data);
							}
							$("#student_table tbody").html(res);

              console.log(data.data);
              // console.log(res);
              console.log(data.data.length);
						}

					});
				}
				else{
					// $("#results").html(""); // set the results empty in case of empty string
				}
			}






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
