status_of_shop_cart();
function ShowVal(x){
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    document.getElementById('sel_price').innerText = x;
}

function status_of_shop_cart(){
    $.ajax({
        type: "GET",
        url: "/orders/status_of_shop_cart/",
        success: function (res){
            $("#indicator__value").text(res);
            $("#indicator__value_mobile").text(res);
        }
    });
}

status_of_shop_cart();

function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        if (params_arr.length) rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function select_sort(){
    var select_sort_value = $("#select_sort").val();
    var url = removeParam("sort_type", window.location.href);
    if (url.includes("?"))
    {
        window.location =url+"&sort_type="+select_sort_value;
    }
    else{
        window.location =url+"?sort_type="+select_sort_value;
    }

}

function select_number_show(){
    var select_sort_value = $("#select_number_show").val();
    var url = removeParam("number_show", window.location.href);
    if (url.includes("?"))
    {
        window.location =url+"&number_show="+select_sort_value;

    }
    else{
        window.location =url+"?number_show="+select_sort_value;
    }

}

status_of_shop_cart();

function add_to_shop_cart(product_id, qty){
    if(qty === 0){
        qty = $("#product-quantity").val();
    }
    $.ajax({
        type: "GET",
        url: "/orders/add_to_shop_cart/",
        data: {
            product_id:product_id,
            qty:qty
        },
        success: function (res){
            status_of_shop_cart();
        }
    });
}

function delete_from_shop_cart(product_id){
    $.ajax({
        type: "GET",
        url: "/orders/delete_from_shop_cart/",
        data: {
            product_id:product_id,
        },
        success: function (res){
            alert('?????????? ???????? ?????? ?????? ???? ?????? ???????? ?????? ????')
            $('#shop_cart_list').html(res);
            status_of_shop_cart();
        }
    });
}
function add_to_input_number(){
    var val = document.getElementById("product-quantity").value;
    val = parseInt(val);
    val +=1;
    document.getElementById("product-quantity").value = val;
}

function sub_to_input_number(){
    var val = document.getElementById("product-quantity").value;
    val = parseInt(val);
    if(val>1){
        val -=1;
    }
    document.getElementById("product-quantity").value = val;
}

function add_to_input_number_in_cart_shop(id, qty){
    $.ajax({
        type:"GET",
        url:"/orders/add_to_input_number/",
        data: {
            id:id,
            qty:qty,
        },
        success: function (res){
            $('#shop_cart_list').html(res);
            status_of_shop_cart();
        }
    });
}

function sub_to_input_number_in_cart_shop(id){
    $.ajax({
        type:"GET",
        url:"/orders/sub_to_input_number/",
        data: {
            id:id,
        },
        success: function (res){
            $('#shop_cart_list').html(res);
            status_of_shop_cart();
        }
    });
}

function AgreeClick(){
    if (document.querySelector('#subi').disabled )
    {
     $('#subi').removeAttr('disabled');
    }
    else {
        document.querySelector('#subi').disabled=true;
    }
}
