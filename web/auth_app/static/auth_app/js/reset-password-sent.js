$(function () {
  $('#recoveryForm').submit(submit);
});

function submit(e) {
  e.preventDefault();

  const form = $(this);
  const fromData = new FormData(this);
  const urlSearchParams = new URLSearchParams(window.location.search);

  if (fromData.get('password_1') !== fromData.get('password_2')) {
    alert('Error! Password and password confirmation are not equal.');

    return;
  }

  $.ajax({
    url: form.attr('action'),
    type: 'POST',
    dataType: 'json',
    data: {
      uid: urlSearchParams.get('uid'),
      token: urlSearchParams.get('token'),
      password_1: this.elements.password_1.value,
      password_2: this.elements.password_2.value,
    },
    success: function (data) {
      alert('Success! Password was updated. You can login with new credentials.');
    },
    error: function (error) {
      let text = 'Server error.';

      switch (error.status) {
        case 400:
          text = 'Some form\'s fields are invalid.';
      }

      alert(`Error! ${text}`);
    }
  })
}
