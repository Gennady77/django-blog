function init(confirmKey, url) {
	$('#btnConfirm').click(() => {
		$.post({
			url,
			dataType: 'json',
			data: { key: confirmKey },
			success: () => {
				console.log('confirm success');
			},
			error: function (data) {
				console.error(data);
			}
		});
	});
}
