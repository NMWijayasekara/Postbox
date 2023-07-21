document.addEventListener('DOMContentLoaded', () => {
    const post_body = document.querySelector('#post_body');
    post_body.onkeyup = () => {
        document.querySelector('#char_count').innerHTML = `${post_body.value.length}/1000`
    }
})
