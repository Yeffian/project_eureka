(function () {
  // Read Django's CSRF token from the cookie
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  const init = () => {
    const csrftoken = getCookie('csrftoken');
    const checkboxes = document.querySelectorAll('input[id^="assignment-"]');

    checkboxes.forEach((box) => {
      box.addEventListener('change', async () => {
        const id = box.id.replace('assignment-', '');
        const isDone = box.checked;

        // optimistic: dim the label immediately
        const label = box.nextElementSibling;
        if (label) label.style.opacity = isDone ? '0.5' : '1';

        try {
          const res = await fetch(`/classes/assignments/${id}/toggle/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ is_done: isDone }),
          });

          if (!res.ok) throw new Error('Request failed');
        } catch (err) {
          // revert on failure
          box.checked = !isDone;
          if (label) label.style.opacity = box.checked ? '0.5' : '1';
          console.error('Could not update assignment:', err);
        }
      });
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();