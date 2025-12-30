const numEl = document.getElementById("topn-number");
const rangeEl = document.getElementById("topn");
// Synchronize the slider with the counter
rangeEl.addEventListener("input", () => {
  numEl.value = rangeEl.value;
});

// Source titles from the select options already populated by Jinja:
const MOVIES = Array.from(document.querySelectorAll('#movie option')).map(o => o.value);


const selectEl = document.getElementById("movie");

// Movie suggestions on typing
const input = document.getElementById("movie-input");
const list = document.getElementById("movie-suggestions");

let activeIndex = -1; // which suggestion is focused
let currentItems = []; // currently rendered suggestions
let debounceTimer = null;

// Basic fuzzy filter: contains match, case-insensitive
function filterMovies(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return MOVIES.filter((t) => t.toLowerCase().includes(q)).slice(0, 8); // cap results
}

function renderSuggestions(items) {
  currentItems = items;
  list.innerHTML = "";
  activeIndex = -1;

  if (!items.length) {
    hideSuggestions();
    return;
  }

  items.forEach((title, i) => {
    const li = document.createElement("li");
    li.role = "option";
    li.id = `movie-opt-${i}`;
    li.className = `bg-black/50 z-10
            cursor-pointer px-4 py-2 text-sm
            text-gray-200 hover:bg-gray-800/70
            border-b border-gray-800 last:border-b-0
          `;
    li.textContent = title;
    li.addEventListener("mousedown", (e) => {
      // mousedown ensures we catch the click before input loses focus
      e.preventDefault();
      choose(i);
    });
    list.appendChild(li);
  });

  showSuggestions();
}

function showSuggestions() {
  list.classList.remove("hidden");
  input.setAttribute("aria-expanded", "true");
}

function hideSuggestions() {
  list.classList.add("hidden");
  input.setAttribute("aria-expanded", "false");
}

function choose(i) {
  if (i >= 0 && i < currentItems.length) {
    input.value = currentItems[i];
    hideSuggestions();
    // Set the <select id="movie"> to the same value:
    const selectEl = document.getElementById("movie");
    if (selectEl) {
      const match = Array.from(selectEl.options).find(
        (o) => o.value === currentItems[i]
      );
      if (match) selectEl.value = match.value;
    }
  }
}

function setActive(i) {
  // clear previous
  Array.from(list.children).forEach((li, idx) => {
    li.classList.toggle("bg-gray-800", idx === i);
    li.classList.toggle("text-white", idx === i);
  });
  activeIndex = i;
}

// Debounced input
input.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    const q = input.value;
    const items = filterMovies(q);
    renderSuggestions(items);
  }, 120);
});

// Keyboard support
input.addEventListener("keydown", (e) => {
  const visible = !list.classList.contains("hidden");

  switch (e.key) {
    case "ArrowDown":
      e.preventDefault();
      if (!visible) {
        const items = filterMovies(input.value);
        renderSuggestions(items);
        return;
      }
      setActive((activeIndex + 1) % currentItems.length);
      break;

    case "ArrowUp":
      e.preventDefault();
      if (!visible) return;
      setActive((activeIndex - 1 + currentItems.length) % currentItems.length);
      break;

    case "Enter":
      if (visible && activeIndex >= 0) {
        e.preventDefault();
        choose(activeIndex);
      }
      // if no movie is chosen and enter is clicked choose the first movie in the apparent list
      else if (visible && activeIndex < 0) {
        e.preventDefault();
        activeIndex = 0;
        choose(activeIndex);
      }
      // if no movie is chosen the list is empty (there are no suggestions) do nothing
      else {
        e.preventDefault();
      }
      break;

    case "Escape":
      hideSuggestions();
      break;
  }
});

// Hide on blur (with slight delay to allow click selection)
input.addEventListener("blur", () => {
  setTimeout(hideSuggestions, 120);
});

// Clicking outside closes suggestions
document.addEventListener("click", (e) => {
  if (!list.contains(e.target) && e.target !== input) {
    hideSuggestions();
  }
});

// Clicking inside opens suggestions
document.addEventListener("click", (e) => {
  if (!list.contains(e.target) && e.target === input) {
    showSuggestions();
  }
});

// Always match the selected movie in "Movie name" to "select a movie" if we used the select movie dropdown
document.addEventListener("click", (e) => {
  if (!list.contains(e.target) && e.target === selectEl) {
    input.value = selectEl.value;
  }
});
