$(function() {

  $('#send_code').click(function() {

    var email = $('input[name="email"]').val();
    
    var regex = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$/;

    console.log(!regex.test(email))

    if(!email) {
      alert('邮件不能为空');
      return;
    } else if(!regex.test(email)){
      alert('邮件格式错误');
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