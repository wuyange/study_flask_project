$(function() {

  $('#send_code').click(function() {

    var email = $('input[name="email"]').val();

    if(!email) {
      alert('邮件不能为空');
      return;
    }

    var url = '/user/send_verification_code';
    var data = {"email": email}
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(response) {
        console.log(response);
      }
    });

  });

});