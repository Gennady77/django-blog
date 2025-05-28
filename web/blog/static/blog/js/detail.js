let authorized = false;

const ERenderPosition = {
  AFTER: 'after',
}

class CommentsDataStore {
  data;
  init (data) {
    this.data = [...data];
  }
  getData () {
    return this.data;
  }
  updateCommentReplies (commentId, data) {
    this.data = this.data.map((comment) => commentId === comment.id ? { ...comment, children: [...data] } : comment);
  }
  getCommentReplies (commentId, offset, limit) {
    const comment = this.data.find((item) => item.id === commentId);

    const newOffset = offset + limit;

    return {
      offset: newOffset,
      hasMore: newOffset < comment.children.length,
      list: comment.children.slice(offset, offset + limit),
    };
  }
}

class Component {
  constructor (props) {
    this.props = props;

    this.beforeInitRoot(props);

    this.$root = this.initRoot();

    this.handleRoot();
  }

  static render (props) {
    const self = this;
    return function (container, position) {
      return (new self(props)).render(container, position);
    }
  }

  render (container, position) {
    this.$container = $(container);

    switch(position) {
      case ERenderPosition.AFTER:
        this.$container.after(this.$root);
        break;

      default:
        this.$container.append(this.$root);
    }

    return this;
  }

  destroy () {
    this.$root.remove();

    this.$root = null;
  }

  handleRoot () {}

  beforeInitRoot () {}

  initRoot () {
    return $('<p>Common component</p>');
  }
}

class CommentsRootListComponent extends Component {
  initRoot () {
    const data = dataStore.getData();

    const $root = $('<ul class="comments-list"></ul>');

    data.map((comment) => CommentComponent.render({
      data: comment,
    })($root));

    return $root;
  }

  handleRoot () {}
}

class ReplyFormComponent extends Component {
  initRoot () {
    return $(`
      <form action="/api/v1/article/comment/" class="replyForm" data-point="replyForm">
        <textarea class="form-control content" rows="1" name="content"></textarea>
        <button type="submit" class="btn btn-primary"><i class="fa fa-reply"></i> Submit</button>
        <button class="btn btn-secondary" data-point="cancelBtn">Cancel</button>
      </form>
    `);
  }

  handleRoot () {
    this.$cancelBtn = this.$root.find('[data-point=cancelBtn]');

    this.$root.submit(this.sendReply.bind(this));
    this.$cancelBtn.click(this.handleCancelClick.bind(this));
  }

  handleCancelClick () {
    const { onClose } = this.props;

    onClose();
  }

  sendReply (e) {
    e.preventDefault();

    const { onSubmit } = this.props;

    const fromData = new FormData(this.$root[0]);

    if (!fromData.get('content')) {
      return;
    }

    const { commentId } = this.props;
    const blogId = getBlogId();

    $.post({
      url: this.$root.attr('action'),
      dataType: 'json',
      data: {
        article: blogId,
        parent: commentId,
        content: fromData.get('content'),
      },
      success: () => {
        $.get({
          url: `/api/v1/article/comment/${blogId}/${commentId}/`,
          dataType: 'json',
          success: (data) => {
            dataStore.updateCommentReplies(commentId, data);

            onSubmit();
          },
          error: () => {
            alert('Ошибка при загрузке ответов');
          },
        });
      },
      error: () => {
        alert('Ошибка при отправке ответа');
      },
    });
  }
}

class ReplyCommentComponent extends Component {
  initRoot () {
    const { data } = this.props;

    return $(`
      <li>
        <div class="comment-avatar"><img
          src="http://i9.photobucket.com/albums/a88/creaticode/avatar_2_zps7de12f8b.jpg" alt=""></div>

        <div class="comment-box">
          <div class="comment-head">
            <div class="comment-head-info">
              <h6 class="comment-name"><a href="#">${ data.user.full_name }</a></h6>
              <span>${ dayjs(data.created).format('DD-MM-YYYY HH:mm') }</span>
            </div>
            <i class="fa fa-heart commentLike"
               data-id="{ child.id }" data-vote=1
               data-type="comment" data-href="">
            </i>
          </div>
          <div class="comment-content">
            ${data.content}
          </div>
        </div>
      </li>
    `);
  }
}

class CommentComponent extends Component {
  beforeInitRoot (props) {
    this.data = props.data;
    this.offset = 0;
    this.limit = 3;
    this.hasMore = false;
    this.$more = null;
  }

  handleRoot () {
    this.$mainLevel = this.$root.find('[data-point=mainLevel]');
    this.$addReply = this.$root.find('[data-point=addReply]');
    this.$replyList = this.$root.find('[data-point=replyList]');

    if (this.$addReply.length > 0) {
      this.$addReply.on('click', this.handleReplyClick.bind(this));
    }
  }

  initRoot () {
    const { data } = this.props;

    const $root = $(`
      <li class="comment">
        <div class="comment-main-level" data-point="mainLevel">
          <div class="comment-avatar"><img
            src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
          <div class="comment-box">
            <div class="comment-head">
              <div class="comment-head-info">
                <h6 class="comment-name by-author"><a href="#">${data.user.full_name}</a></h6>
                <span>${ dayjs(data.created).format('DD-MM-YYYY HH:mm') }</span>
              </div>
              <div>
                <i class="fa fa-heart commentLike"
                   data-id="{ comment.id }"
                   data-vote=1
                   data-href=""
                   data-type="comment"
                ></i>
              </div>
            </div>
            <div class="comment-content">
               ${data.content}
            </div>
          </div>
        </div>
        <!-- Comments reply -->
        <ul class="comments-list reply-list" data-point="replyList"></ul>
      </li>
    `);

    if (authorized) {
      $root.find('.commentLike').after(`
        <a data-point="addReply">
          <i class="fa fa-reply"></i>
        </a>
      `);
    }

    const { list, offset, hasMore } = dataStore.getCommentReplies(data.id, this.offset, this.limit);
    const $replyList = $root.find('[data-point=replyList]');

    list.forEach((comment) => ReplyCommentComponent.render({ data: comment })($replyList));

    if (hasMore) {
      this.$more = $('<div class="moreReplies">Показать еще...</div>');
      $root.append(this.$more);
      this.$more.click(this.handleMoreClick.bind(this));
    }

    return $root;
  }

  handleMoreClick () {
    this.offset += this.limit;
    this.updateChildren();
  }

  updateChildren () {
    const { data: {
      id: commentId,
    } } = this.props;

    const { list, offset, hasMore } = dataStore.getCommentReplies(commentId, this.offset, this.limit);

    list.forEach((comment) => ReplyCommentComponent.render({ data: comment })(this.$replyList));

    if (!hasMore) {
      this.$more.remove();
      this.$more = null;
    }
  }

  handleSubmit () {
    this.updateChildren();
  }

  handleClose () {
    this.replyFormComponent.destroy();
    this.replyFormComponent = null;
    this.replyFormShow = false;
  }

  handleReplyClick (event) {
    event.preventDefault();

    if (!authorized) {
      return;
    }

    if (this.replyFormShow) {
      return;
    }

    this.replyFormShow = true;

    const {
      data: {
        id: commentId,
      }
    } = this.props;

    this.replyFormComponent = ReplyFormComponent.render({
      commentId,
      onClose: this.handleClose.bind(this),
      onSubmit: this.handleSubmit.bind(this),
    })(this.$mainLevel, ERenderPosition.AFTER);
  }
}

const dataStore = new CommentsDataStore();

function getBlogId() {
  const matches = window.location.pathname.match(/^\/blog\/(\d+)$/i);

  return matches[1];
}

$(function () {
  $.ajax({
    url: `/api/v1/profile/`,
    type: 'GET',
    dataType: 'json',
    success: () => {
      authorized = true;
    },
    complete: () => {
      loadData();
    }
  });
});

function loadData() {
  const containerArticle = $('#article');
  const containerCommentsCount = $('#commentCount');
  const containerComments = $('#paginationComment');
  const searchParams = new URLSearchParams(window.location.search);
  const blogId = getBlogId();

  $.ajax({
    url: `/api/v1/article/detail/${blogId}/`,
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      containerCommentsCount.text(`Comments (${data.comments_count})`);
      containerArticle.replaceWith(renderArticle(data));
    },
    error: () => {
      window.alert('Ошибка при загрузке статей');
    },
  });

  $.ajax({
    url: `/api/v1/article/comment/${blogId}/`,
    type: 'GET',
    dataType: 'json',
    success: (data) => {
      dataStore.init(data);

      CommentsRootListComponent.render({
        data
      })($('#commentCount'), ERenderPosition.AFTER);
    },
    error: () => {
      window.alert('Ошибка при загрузке комментариев');
    },
  });
}

$(function () {
  $('#commentForm').submit(sendComment);
});

function closeReplyForm() {
  const replyForm = $(this.closest('.replyForm'));

  replyForm.remove();
}

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

function sendComment(e) {
  e.preventDefault();

  const formData = new FormData(this);

  const pathname = window.location.pathname;

  const [,articleId] = pathname.match(/^\/blog\/(\d+)$/i);

  $.ajax({
    url: '/api/v1/article/comment/',
    data: {
      article: articleId,
      content: formData.get('content')
    },
    type: 'POST',
    dataType: 'json',
    success: (data) => {
      console.log(data);
    },
    error: () => {
      window.alert('Ошибка при отправке комментария');
    },
  });
}

function renderCommentList() {}
