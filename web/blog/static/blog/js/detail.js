$(function () {
  const container = $('#article');
  const searchParams = new URLSearchParams(window.location.search);
  const matches = window.location.pathname.match(/^\/blog\/(\d+)$/i);
  const blogId = matches[1];

  $.ajax({
    url: `/api/v1/article/detail/${blogId}/`,
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      container.replaceWith(renderArticle(data));
    },
    error: () => {
      window.alert('Ошибка при загрузке статей');
    },
  });
});

function renderArticle(article) {
  return $(`
    <div>
      <h1><a href="javascript: void(0)">${article.title}</a></h1>
      <p class="lead"><i class="fa fa-user"></i> by <a href="javascript: void(0)">${article.author.full_name}</a>
      </p>
      <hr>
      <p><i class="fa fa-calendar"></i> Posted on ${dayjs(article.created).format('MMMM DD, YYYY [at]  HH:mm')}</p>
      <p><i class="fa fa-tags"></i> Tags: <a href=""><span class="badge badge-info">Bootstrap</span></a> <a
        href=""><span class="badge badge-info">Web</span></a> <a href=""><span class="badge badge-info">CSS</span></a>
        <a href=""><span class="badge badge-info">HTML</span></a></p>

      <hr>
      <img src="${article.image}" class="img-responsive">
      <hr>
      ${article.content}
    </div>
  `);
}
