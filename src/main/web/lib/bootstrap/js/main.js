$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
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
  

});
