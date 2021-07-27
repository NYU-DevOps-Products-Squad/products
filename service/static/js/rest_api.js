$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_price").val(res.price);
        $("#product_inventory").val(res.inventory);
        $("#product_owner").val(res.owner);
        $("#product_category").val(res.category);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_price").val("");
        $("#product_inventory").val("");
        $("#product_owner").val("");
        $("#product_category").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {
      var name = $("#product_name").val();
      var price = $("#product_price").val();
      var owner = $("#product_owner").val();
      var category = $("#product_category").val();

      var queryString = ""

      if (price) {
        queryString += 'low=' + price + '&high=' + price
      }
      if (name) {
        if (queryString.length > 0) {
          queryString += '&name=' + name
        }else{
          queryString += 'name=' + name
        }
      }
      if (category) {
          if (queryString.length > 0) {
              queryString += '&category=' + category
          } else {
              queryString += 'category=' + category
          }
      }
      if (owner) {
          if (queryString.length > 0) {
              queryString += '&owner=' + owner
          } else {
              queryString += 'owner=' + owner
          }
      }

      var ajax = $.ajax({
          type: "GET",
          url: "/products?" + queryString,
          contentType: "application/json",
          data: ''
      })

      ajax.done(function(res){
          //alert(res.toSource())
          $("#search_results").empty();
          $("#search_results").append('<table class="table-striped" cellpadding="10">');
          var header = '<tr>'
          header += '<th style="width:10%">ID</th>'
          header += '<th style="width:40%">Name</th>'
          header += '<th style="width:40%">Price</th>'
          header += '<th style="width:40%">Category</th>'
          header += '<th style="width:10%">Owner</th></tr>'
          $("#search_results").append(header);
          var firstProduct = "";
          for(var i = 0; i < res.length; i++) {
              var product = res[i];
              var row = "<tr><td>"+product._id+"</td><td>"+product.name+"</td><td>"+product.price+"</td><td>"+product.category+"</td><td>"+product.owner+"</td></tr>";
              $("#search_results").append(row);
              if (i == 0) {
                  firstProduct = product;
              }
          }

          $("#search_results").append('</table>');

          // copy the first result to the form
          if (firstProduct != "") {
              update_form_data(firstProduct)
          }

          flash_message("Success")
      });

      ajax.fail(function(res){
          flash_message(res.responseJSON.message)
      });

  });

})
