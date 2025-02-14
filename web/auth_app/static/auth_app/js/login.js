$(function () {
  $('#loginForm').submit(login);
});

$(function () {
  $('#forgotPasswordForm').submit(forgotPassword);
});

function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
}

function forgotPassword(e) {
  e.preventDefault();

  const form = $(this);

  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    dataType: 'json',
    data: form.serialize(),
    success: function() {
      $('#pwdModal').modal('hide');

      alert('Success! An email confirming the password change was sent to the specified email address. Follow the instructions.');
    },
    error: function(data) {
      let text = 'Server error.';

      switch (data.status) {
        case 404:
          text = 'There is no user with such an email.';
        break;
      }

      alert(`Error! ${text}`);
    }
  });
}
