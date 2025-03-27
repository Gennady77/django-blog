$(function () {
  $.ajax({
    url: '/api/v1/article/list/',
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      const listContainer = $('#blogList');

      listContainer.append(data.results.map((article) => renderArticle(article)).join(''));

      updatePaginator(data);
    },
    error: () => {
      window.alert('Ошибка при загрузке статей');
    },
  });
});

function navigatePage(pageNumber) {
  const query = pageNumber ? `?page=${pageNumber}` : '';

  $.ajax({
    url: `/api/v1/article/list/${query}`,
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      const listContainer = $('#blogList').empty();

      listContainer.append(data.results.map((article) => renderArticle(article)).join(''));

      updatePaginator(data, pageNumber);
    },
    error: () => {
      window.alert('Ошибка при загрузке статей');
    },
  });
}

function updatePaginator(data, currentPage = 1) {
  const paginatorContainer = $('#paginator');
  paginatorContainer.empty();

  const count = Math.ceil(data.count / 5);
  const prevDisabled = currentPage === 1;
  const nextDisabled = currentPage === count;

  const prev = $(`
    <li>
      <a href="javascript: void(0)" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
  `)
    .click(() => !prevDisabled && navigatePage(currentPage - 1))
    .addClass(prevDisabled ? 'disabled' : '');

  const next = $(`
    <li>
      <a href="javascript: void(0)" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  `)
    .click(() => !nextDisabled && navigatePage(currentPage + 1))
    .addClass(nextDisabled ? 'disabled' : '');

  paginatorContainer.append(prev);

  for(let i = 1; i <= count; i++) {
    const active = i === currentPage;

    const li = $(`<li><a href="javascript: void(0)">${i}</a></li>`)
      .click(() => !active && navigatePage(i))
      .addClass(active ? 'active' : '')
    paginatorContainer.append(li);
  }

  paginatorContainer.append(next);
}

function renderArticle(article) {
  return `
    <div class="row">
      <div class="col-md-12 post">
        <div class="row">
          <div class="col-md-12">
            <h4>
              <strong>
                <a href="/blog/${article.id}" class="post-title">${ article.title }</a>
              </strong>
            </h4>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 post-header-line">
            <span class="glyphicon glyphicon-user"></span>by <a href="#">${ article.author.full_name }</a> |
            <span class="glyphicon glyphicon-calendar"></span> ${ dayjs(article.updated).format('DD-MM-YYYY HH:mm') } |
            <span class="glyphicon glyphicon-comment"></span><a href="#">{{ article.comments_count }} Comments</a> |
            <i class="icon-share"></i><a href="#">39 Shares</a> |
            <span class="glyphicon glyphicon-tags"></span> Tags: <a href="#">
            <span class="label label-info">Snipp</span></a> <a href="#">
            <span class="label label-info">Bootstrap</span></a> <a href="#">
            <span class="label label-info">UI</span></a> <a href="#">
            <span class="label label-info">growth</span></a>
          </div>
        </div>
        <div class="row post-content">
          <div class="col-md-3">
            <a href="#">
              <img
                src="${article.image}"
                alt="" class="img-responsive">
            </a>
          </div>
          <div class="col-md-9">
            <p>
              ${article.short_content}
            </p>
            <p>
              <a class="btn btn-read-more" href="/blog/${article.id}">Read more</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  `;
}

