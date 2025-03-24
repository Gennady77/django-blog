let captchaToken;

$(function () {
  $('#loginForm').submit(login);
});

$(function () {
  $('#forgotPasswordForm').submit(forgotPassword);
});

function recaptchaSuccess(token) {
  captchaToken = token;
}

function recaptchaErrorHandle(data) {
  if (data.responseJSON.g_recaptcha_response) {
    alert('Ошибка подтверждения капчи');

    return true;
  }
}

function login(e) {
  e.preventDefault()

  if (!captchaToken) {
    alert('Поставьте галочку, что вы не робот!');

    return;
  }

  let form = $(this);

  const fromData = new FormData(this);

  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: {
      email: fromData.get('email'),
      password: fromData.get('password'),
      g_recaptcha_response: captchaToken,
    },
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      if (recaptchaErrorHandle(data)) {
        return;
      }

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

  if (!captchaToken) {
    alert('Поставьте галочку, что вы не робот!');

    return;
  }

  const form = $(this);

  const fromData = new FormData(this);

  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    dataType: 'json',
    data: {
      email: fromData.get('email'),
      g_recaptcha_response: captchaToken,
    },
    success: function() {
      $('#pwdModal').modal('hide');

      alert('Success! An email confirming the password change was sent to the specified email address. Follow the instructions.');
    },
    error: function(data) {
      if (recaptchaErrorHandle(data)) {
        return;
      }

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
