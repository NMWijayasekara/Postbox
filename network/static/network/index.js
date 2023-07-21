document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.open_comment_form').forEach((element) => {
    const post_id = element.dataset.id
    element.addEventListener('click', () => {
      document.querySelectorAll(`.create_comment`).forEach((element) => {
        if (element.dataset.id === post_id) {
          document.querySelectorAll('.show_comments').forEach((comment) => {
            if (comment.dataset.id === post_id) {
              comment.style.display = 'none';
            }
          });
          element.style.display = 'block';
          element.style.animationPlayState = 'running';
        } else {
          return false;
        }
      });
    });
  });

  document.querySelectorAll('.comment_body').forEach((textarea) => {
    document.querySelectorAll('.comment_submit').forEach((button) => {
      if (textarea.dataset.id === button.dataset.id) {
        textarea.onkeyup = () => {
          if (textarea.value == '') {
            button.disabled = true;
          } else if (!textarea.value.replace(/\s/g, '').length) {
            button.disabled = true;
          } else {
            button.disabled = false;
          }
        }
      }
    });
  });

  document.querySelectorAll('.comment_cancel').forEach((button) => {
    button.addEventListener('click', () => {
      button.parentElement.style.display = 'none';
    });
  });

  document.querySelectorAll('.comment_view').forEach((button) => {
    const post_id = button.dataset.post_id
    button.onclick = () => {
      if (button.innerHTML == '0') {
        document.querySelectorAll(`.create_comment`).forEach((element) => {
          if (element.dataset.id == button.dataset.id) {
            element.style.display = 'block';
            element.style.animationPlayState = 'running';
          }
        });
      } else {
        document.querySelectorAll('.show_comments').forEach((comment) => {
          if (comment.dataset.id === post_id) {
            if (comment.style.display == 'block') {
              comment.style.display = 'none';
            } else {
              document.querySelectorAll('.create_comment').forEach((div) => {
                if (div.dataset.id === post_id) {
                  div.style.display = 'none';
                }
              });
              comment.style.display = 'block';
              comment.style.animationPlayState = 'running';
            }
          }
        });
      }
    }
  });

  document.querySelectorAll('.like_button').forEach((button) => {
    button.addEventListener('click', () => {
      if (button.firstElementChild.classList == 'far fa-heart') {
        fetch('/like', {
          method: 'POST',
          body: JSON.stringify({
            post: button.dataset.id
          })
        })
        button.firstChild.classList = "fas fa-heart"
        document.querySelectorAll('.like_count').forEach((counter) => {
          if (counter.dataset.id === button.dataset.id) {
            const current = parseInt(counter.innerHTML);
            counter.innerHTML = current + 1;
          }
        })
      } else {
        fetch('/unlike', {
          method: 'POST',
          body: JSON.stringify({
            post: button.dataset.id
          })
        })
        button.firstChild.classList = "far fa-heart"
        document.querySelectorAll('.like_count').forEach((counter) => {
          if (counter.dataset.id === button.dataset.id) {
            const current = parseInt(counter.innerHTML);
            counter.innerHTML = current - 1;
          }
        })
      }
    })
  })
});