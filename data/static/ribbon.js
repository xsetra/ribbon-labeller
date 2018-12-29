function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function before_ajax(csrftoken) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;

    //var csrftoken = getCookie('csrftoken');
}

function flash(id) {
    $(id).show();
    $(id).delay(800).hide(200);
}

function not_clickable(sentence_id){
    $("#plus"+sentence_id).css({'pointer-events': 'none'});
    $("#incorrect"+sentence_id).css({'pointer-events': 'none'});
    $("#asp"+sentence_id).css({'pointer-events': 'none'});
    $("#pol"+sentence_id).css({'pointer-events': 'none'});
}

function clickable(sentence_id){
    $("#plus"+sentence_id).css({'pointer-events': 'auto'});
    $("#incorrect"+sentence_id).css({'pointer-events': 'auto'});
    $("#asp"+sentence_id).css({'pointer-events': 'auto'});
    $("#pol"+sentence_id).css({'pointer-events': 'auto'});
}

function add_label(plusBtnID) {
    var sentence_id = parseInt($("#"+plusBtnID).attr('sentence-id'));
    var aspect = $("[name=asp"+ sentence_id +"]").val();
    var polarity = $("[name=pol"+ sentence_id +"]").val();
    polarity = (polarity == 'True')
    labelPayload.push({"id": sentence_id, "aspect": aspect, "polarity": polarity, "correctness": true});
    flash("#plus_flash");
    $("#row"+sentence_id).css({'background-color': '#d0d02d'});
    not_clickable(sentence_id);
}

function delete_item(item, index, arr) {
    if(item['id'] == sentence_id) {
        arr.splice(index, 1);
        isDeleted = true;
    }
}

function remove_label(trashBtnID) {
    // Global `sentence_id` because, delete_item compares which one will be deleted.
    sentence_id = parseInt($("#"+trashBtnID).attr('sentence-id'));
    labelPayload.forEach(delete_item);
    if (isDeleted == true) {
        flash("#trash_flash");
        $("#row"+sentence_id).css({'background-color': 'inherit'});
        clickable(sentence_id);
        isDeleted = false;
    }
    else {
        $("#nothing_todo").show();
        flash("#nothing_todo");
    }
}

function incorrect_label(incorrectBtnID) {
    var sentence_id = parseInt($("#"+incorrectBtnID).attr('sentence-id'));
    labelPayload.push({"id": sentence_id, "correctness": false});
    flash("#incorrect_flash");
    $("#row"+sentence_id).css({'background-color': '#b9b9b9'});
    not_clickable(sentence_id);
}

function saveLabels(uri) {
    if(labelPayload.length == 0){
        alert("En az bir etiket eklemiş olmalısınız.");
    }
    else {
        var csrftoken = getCookie('csrftoken');
        before_ajax(csrftoken);
        $.post({
            type: 'POST',
            url: uri,
            data: {"labels": JSON.stringify(labelPayload)},
            success: function (resp) {
                alert(resp);
            },
            error: function (resp) {
                alert(resp);
            }
        });
        location.reload();
    }
}