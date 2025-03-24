let captchaToken;

function recaptchaSuccess(token) {
  captchaToken = token;
}

$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();

  if (!captchaToken) {
    alert('Поставьте галочку, что вы не робот!');

    return;
  }

  const formData = new FormData(this);

	$.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: {
      first_name: formData.get('first_name'),
      last_name: formData.get('last_name'),
      email: formData.get('email'),
      password_1: formData.get('password_1'),
      password_2: formData.get('password_2'),
      g_recaptcha_response: captchaToken,
    },
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      console.error(data);
    }
  });
}
