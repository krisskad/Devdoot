    $("#state").change(function () {
      var url = $("#locationform").attr("data-location-url");  // get the url of the `cities` view
      var state_id = $(this).val();  // get the selected state ID from the HTML input
      $.ajax({                       // initialize an AJAX request
        type: "GET",
        url: url,                    // set the url of the request (= localhost:8000/load-courses/)
        data: {
          'state_id': state_id       // add the programming id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_courses` view function
          $("#city").html(data);  // replace the contents of the course input with the data that came from the server
        }
      });
    });