function ShowVal(x){
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    document.getElementById('sel_price').innerText = x;
}

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