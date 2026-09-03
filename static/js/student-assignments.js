(function () {
  // --- CSRF helper (reads Django's csrftoken cookie) ---
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  const init = () => {
    const csrftoken = getCookie('csrftoken');

    // ============================================================
    // 1. Checkbox toggling — flips this student's completion record
    // ============================================================
    const checkboxes = document.querySelectorAll('input[id^="completion-"]');

    checkboxes.forEach((box) => {
      box.addEventListener('change', async () => {
        const id = box.id.replace('completion-', '');
        const isDone = box.checked;

        const row = box.closest('.assignment-row');
        const title = row ? row.querySelector('.assignment-title') : null;

        // Optimistic UI: strike through + tint immediately
        if (title) {
          title.classList.toggle('line-through', isDone);
          title.classList.toggle('text-inksoft/60', isDone);
        }
        if (row) {
          row.classList.toggle('bg-mint/10', isDone);
          row.classList.toggle('bg-cream', !isDone);
        }

        try {
          const res = await fetch(`/classes/completions/${id}/toggle/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ is_done: isDone }),
          });
          if (!res.ok) throw new Error('Request failed');
        } catch (err) {
          // Revert on failure
          box.checked = !isDone;
          if (title) {
            title.classList.toggle('line-through', !isDone);
            title.classList.toggle('text-inksoft/60', !isDone);
          }
          if (row) {
            row.classList.toggle('bg-mint/10', !isDone);
            row.classList.toggle('bg-cream', isDone);
          }
          console.error('Could not update assignment:', err);
        }
      });
    });

    // ============================================================
    // 2. Group-by-course toggle (purely client-side rearrange)
    // ============================================================
    const list = document.getElementById('assignment-list');
    const btnNone = document.getElementById('group-none');
    const btnCourse = document.getElementById('group-course');
    if (!list || !btnNone || !btnCourse) return;

    // Snapshot the original alphabetical order so "None" can restore it
    const originalRows = Array.from(list.querySelectorAll('.assignment-row'));

    const setActive = (activeBtn, inactiveBtn) => {
      activeBtn.classList.add('bg-butter');
      activeBtn.classList.remove('bg-cream');
      activeBtn.setAttribute('aria-pressed', 'true');
      inactiveBtn.classList.remove('bg-butter');
      inactiveBtn.classList.add('bg-cream');
      inactiveBtn.setAttribute('aria-pressed', 'false');
    };

    const clearHeadings = () => {
      list.querySelectorAll('.course-heading').forEach((h) => h.remove());
    };

    const showFlat = () => {
      clearHeadings();
      originalRows.forEach((row) => list.appendChild(row));  // re-append in original order
    };

    const showGrouped = () => {
      clearHeadings();

      // Bucket rows by their data-course value
      const groups = {};
      originalRows.forEach((row) => {
        const course = row.dataset.course || 'Other';
        (groups[course] = groups[course] || []).push(row);
      });

      // Re-append, course by course (course names sorted alphabetically),
      // each preceded by a heading
      Object.keys(groups).sort().forEach((course) => {
        const heading = document.createElement('li');
        heading.className = 'course-heading font-display font-bold text-lg pt-3 pb-1';
        heading.textContent = course;
        list.appendChild(heading);
        groups[course].forEach((row) => list.appendChild(row));
      });
    };

    btnNone.addEventListener('click', () => {
      setActive(btnNone, btnCourse);
      showFlat();
    });
    btnCourse.addEventListener('click', () => {
      setActive(btnCourse, btnNone);
      showGrouped();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();