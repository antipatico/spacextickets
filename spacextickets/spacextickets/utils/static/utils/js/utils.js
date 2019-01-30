function winloadAppend(method) {
    if(method)  {
        let old = window.onload;
        window.onload = function() {
            if (old)
                old();
            method();
        }
    }
}

function createHiddenForm(action, method="POST") {
    return $('<form></form>').attr("action", action).attr("method", method).attr("class", "invisible");
}