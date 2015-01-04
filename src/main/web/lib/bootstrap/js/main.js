$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    if($('#fileupload').length>0) {

    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: '/fileupload'
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

  $('#fileupload').fileupload('option', {
    
                              url: '/fileupload',
                              // Enable image resizing, except for Android and Opera,
                              // which actually support image resizing, but fail to
                              // send Blob objects via XHR requests:
                              disableImageResize: /Android(?!.*Chrome)|Opera/
                              .test(window.navigator.userAgent),
                              maxFileSize: 5000000,
                              acceptFileTypes: /(\.|\/)(txt|dat?a|xml|csv)$/i
                              });
          // Load existing files:
        $('#fileupload').addClass('fileupload-processing');
        $.ajax({
            // Uncomment the following to send cross-domain cookies:
            //xhrFields: {withCredentials: true},
            url: $('#fileupload').fileupload('option', 'url'),
            dataType: 'json',
            context: $('#fileupload')[0]
        }).always(function () {
            $(this).removeClass('fileupload-processing');
        }).done(function (result) {
            $(this).fileupload('option', 'done')
                .call(this, $.Event('done'), {result: result});
        });
  

  } //end if
});

function parseJson(j) {
  return jQuery.parseJSON(j);
}

function getMessagesFromJson(j) {
  if (j.length) {
    var resultMsgs=""
    for(i=0; i<j.length; i++){
      resultMsgs+=j[i].message+'<br/>'
    }
    return resultMsgs
  } else {
    return j.message
  }
}

function getValuesFromJson (j, fieldName) {
  if (j.length) {
    var resultMsgs=""
    for(i=0; i<j.length; i++){
      resultMsgs+=j[i][fieldName]+'<br/>'
    }
    return resultMsgs
  } else {
    return j[fieldName]
  }
}

function displayResultMessage(whichUI, msg) {
  $(whichUI).html(msg)
}

function getPointerEventsValueOn () {
  return "auto";
}
function getPointerEventsValueOff () {
  return "none";
}
function getOpacityOn() {
  return "1.0"
}
function getOpacityOff() {
  return "0.2"
}

//Cookie related
function readCookie(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        }

