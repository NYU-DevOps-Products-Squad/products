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
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var description = $("#product_description").val();
        var price = $("#product_price").val();
        var inventory = $("#product_inventory").val();
        var owner = $("#product_owner").val();
        var category = $("#product_category").val();

        var data = {
            "name": name,
            "description": description,
            "price": price,
            "inventory": inventory,
            "owner": owner,
            "category": category
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/products/" + product_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Read a Product
    // ****************************************

    $("#read-btn").click(function (){
        var name = $("#product_name").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            var product = res[0];
            $("#product_id").val(product.id);
            $("#product_name").val(product.name);
            $("#product_description").val(product.description);
            $("#product_price").val(product.price);
            $("#product_inventory").val(product.inventory);
            $("#product_owner").val(product.owner);
            $("#product_category").val(product.category);
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });



})
