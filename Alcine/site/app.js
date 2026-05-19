const chapters = window.ASTRAEL_CHAPTERS ?? [];
const chapterList = document.querySelector("#chapter-list");
const chapterContent = document.querySelector("#chapter-content");
const chapterKicker = document.querySelector("#chapter-kicker");
const chapterTitle = document.querySelector("#chapter-title");
const searchInput = document.querySelector("#search-input");
const prevButton = document.querySelector("#prev-chapter");
const nextButton = document.querySelector("#next-chapter");
const navToggle = document.querySelector("#nav-toggle");
const sidebar = document.querySelector("#sidebar");
const themeToggle = document.querySelector("#theme-toggle");
const fontDown = document.querySelector("#font-down");
const fontUp = document.querySelector("#font-up");

let activeIndex = Math.max(0, chapters.findIndex((chapter) => chapter.number === "1"));
let fontScale = Number(localStorage.getItem("astrael-reader-font-scale") ?? 1);

init();

function init() {
  applySavedTheme();
  applyFontScale();
  bindEvents();
  renderChapterList(chapters);
  renderChapter(activeIndex);
}

function bindEvents() {
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLocaleLowerCase("th");
    const filtered = chapters.filter((chapter) =>
      `${chapter.number} ${chapter.title}`.toLocaleLowerCase("th").includes(query),
    );
    renderChapterList(filtered);
  });

  prevButton.addEventListener("click", () => renderChapter(activeIndex - 1));
  nextButton.addEventListener("click", () => renderChapter(activeIndex + 1));

  navToggle.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    document.body.classList.toggle("nav-open");
  });

  document.addEventListener("click", (event) => {
    if (!document.body.classList.contains("nav-open")) {
      return;
    }
    if (!sidebar.contains(event.target) && !navToggle.contains(event.target)) {
      sidebar.classList.remove("open");
      document.body.classList.remove("nav-open");
    }
  });

  themeToggle.addEventListener("click", () => {
    const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    if (nextTheme === "dark") {
      document.documentElement.dataset.theme = "dark";
    } else {
      delete document.documentElement.dataset.theme;
    }
    localStorage.setItem("astrael-reader-theme", nextTheme);
  });

  fontDown.addEventListener("click", () => setFontScale(fontScale - 0.08));
  fontUp.addEventListener("click", () => setFontScale(fontScale + 0.08));

  chapterList.addEventListener("click", (event) => {
    const button = event.target.closest(".chapter-item");
    if (!button) {
      return;
    }
    const index = chapters.findIndex((chapter) => chapter.number === button.dataset.number);
    renderChapter(index);
    sidebar.classList.remove("open");
    document.body.classList.remove("nav-open");
  });
}

function renderChapterList(items) {
  chapterList.innerHTML = items
    .map(
      (chapter) => `
        <button
          class="chapter-item ${chapter.number === chapters[activeIndex]?.number ? "active" : ""}"
          data-number="${chapter.number}"
          type="button"
        >
          <span>${chapter.number === "0" ? "ตอน 00" : `ตอน ${chapter.number}`}</span>
          <strong>${escapeHtml(chapter.title)}</strong>
        </button>
      `,
    )
    .join("");

}

function renderChapter(index) {
  if (index < 0 || index >= chapters.length) {
    return;
  }

  activeIndex = index;
  const chapter = chapters[activeIndex];
  chapterKicker.textContent = chapter.number === "0" ? "ตอน 00" : `ตอน ${chapter.number}`;
  chapterTitle.textContent = chapter.title;
  chapterContent.innerHTML = renderMarkdown(chapter.content);
  prevButton.disabled = activeIndex === 0;
  nextButton.disabled = activeIndex === chapters.length - 1;
  document.title = `${chapter.number === "0" ? "ตอน 00" : `ตอน ${chapter.number}`} - ${chapter.title} | Astrael`;
  renderChapterList(filterChapters(searchInput.value.trim()));
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function filterChapters(query) {
  const normalized = query.toLocaleLowerCase("th");
  if (!normalized) {
    return chapters;
  }
  return chapters.filter((chapter) =>
    `${chapter.number} ${chapter.title}`.toLocaleLowerCase("th").includes(normalized),
  );
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/^\s*\uFEFF?/, "").replace(/\r/g, "").split("\n");
  const blocks = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    if (trimmed === "—") {
      blocks.push("<hr />");
      index += 1;
      continue;
    }

    const image = trimmed.match(/^!\[(.*?)\]\((.*?)\)$/);
    if (image) {
      const source = image[2].startsWith("aresia-")
        ? window.ASTRAEL_INLINE_MAP ?? `./assets/${image[2]}`
        : image[2];
      blocks.push(`
        <figure class="chapter-image">
          <img src="${escapeAttribute(source)}" alt="${escapeAttribute(image[1])}" />
        </figure>
      `);
      index += 1;
      continue;
    }

    const heading = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = Math.min(heading[1].length, 4);
      blocks.push(`<h${level}>${inline(heading[2])}</h${level}>`);
      index += 1;
      continue;
    }

    if (trimmed.startsWith(">")) {
      const quoteLines = [];
      while (index < lines.length && lines[index].trim().startsWith(">")) {
        quoteLines.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      blocks.push(`<blockquote>${quoteLines.map((item) => `<p>${inline(item)}</p>`).join("")}</blockquote>`);
      continue;
    }

    if (/^\*\s+/.test(trimmed)) {
      const items = [];
      while (index < lines.length && /^\*\s+/.test(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^\*\s+/, ""));
        index += 1;
      }
      blocks.push(`<ul>${items.map((item) => `<li>${inline(item)}</li>`).join("")}</ul>`);
      continue;
    }

    const paragraphLines = [];
    while (
      index < lines.length &&
      lines[index].trim() &&
      lines[index].trim() !== "—" &&
      !/^!\[(.*?)\]\((.*?)\)$/.test(lines[index].trim()) &&
      !/^(#{1,6})\s+/.test(lines[index].trim()) &&
      !lines[index].trim().startsWith(">") &&
      !/^\*\s+/.test(lines[index].trim())
    ) {
      paragraphLines.push(lines[index].trim());
      index += 1;
    }
    blocks.push(`<p>${inline(paragraphLines.join("<br />"))}</p>`);
  }

  return blocks.join("");
}

function inline(text) {
  return escapeHtml(text)
    .replace(/&lt;br \/&gt;/g, "<br />")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function applySavedTheme() {
  if (localStorage.getItem("astrael-reader-theme") === "dark") {
    document.documentElement.dataset.theme = "dark";
  }
}

function setFontScale(nextScale) {
  fontScale = Math.min(1.32, Math.max(0.84, Number(nextScale.toFixed(2))));
  localStorage.setItem("astrael-reader-font-scale", fontScale);
  applyFontScale();
}

function applyFontScale() {
  document.documentElement.style.setProperty("--reader-scale", fontScale);
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}
