$(function () {
  init();
});

function init() {
	const urlSearchParams = new URLSearchParams(window.location.search);

	$.post({
		url: '/api/v1/auth/sign-up/verify/',
		dataType: 'json',
		data: { key: urlSearchParams.get('confirm_key') },
		success: () => {
			console.log('confirm success');
		},
		error: function (data) {
			console.error(data);
		}
	});
}
