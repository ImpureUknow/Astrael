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
const nameModeSelect = document.querySelector("#name-mode-select");
const viewTabs = [...document.querySelectorAll(".reader-tab")];
const readerMeta = document.querySelector("#reader-meta");
const chapterNav = document.querySelector(".chapter-nav");

const VIEW_MODE_KEY = "astrael-reader-view-mode";
const comicChapters = window.ASTRAEL_COMICS ?? {};

const NAME_MODE_KEY = "astrael-reader-name-mode";
const nameModeValues = new Set(["english", "thai", "english-thai", "thai-english"]);
const nameEntries = [
  { english: "Admiral Adrian Valcrest", thai: "พลเรือเอก เอเดรียน วาลเครสต์" },
  { english: "Patrick Draven Alcine", thai: "แพททริค เดรเวน แอลซีน" },
  { english: "Magnus Reinhardt", thai: "แม็กนัส ไรน์ฮาร์ด" },
  { english: "Adrian Valcrest", thai: "เอเดรียน วาลเครสต์" },
  { english: "Alistair Valtieri", thai: "อลิสแตร์ วัลเทียรี" },
  { english: "Aurelius Valtieri", thai: "ออเรเลียส วัลเทียรี" },
  { english: "Seraphina Valtieri", thai: "เซราฟินา วัลเทียรี" },
  { english: "Patrick Alcine", thai: "แพททริค แอลซีน" },
  { english: "Draven Alcine", thai: "เดรเวน แอลซีน" },
  { english: "Cedric Alcine", thai: "เซดริก แอลซีน" },
  { english: "Elias Velmora", thai: "อีเลียส เวลมอรา" },
  { english: "Vael Drakhar", thai: "เวล ดราคฮาร์" },
  { english: "Kael Alcine", thai: "เคล แอลซีน" },
  { english: "Dawn Reed", thai: "ดอว์นรีด" },
  { english: "Grey Wren", thai: "เกรย์เรน" },
  { english: "Stone Cove", thai: "อ่าวศิลา" },
  { english: "Aetherion", thai: "เอเธอเรียน" },
  { english: "Astrael", thai: "อัสทราเอล" },
  { english: "Solhaven", thai: "ซอลเฮเวน" },
  { english: "Solvane", thai: "โซลเวน" },
  { english: "Rosvaria", thai: "รอสวาเรีย" },
  { english: "Caldara", thai: "คัลดารา" },
  { english: "Caldria", thai: "คัลเดรีย" },
  { english: "Darian", thai: "ดาเรียน" },
  { english: "Ressa", thai: "เรสซา" },
  { english: "Tovin", thai: "โทวิน" },
  { english: "Maren", thai: "มาเรน" },
  { english: "Taren", thai: "ทาเรน" },
  { english: "Mereth", thai: "เมเรธ" },
  { english: "Nalla", thai: "นัลลา" },
  { english: "Orren", thai: "ออร์เรน" },
  { english: "Hale", thai: "เฮล" },
  { english: "Liora", thai: "ลิโอรา" },
  { english: "Neris", thai: "เนริส" },
  { english: "Ilyan", thai: "อิลยัน" },
  { english: "Bren", thai: "เบรน" },
  { english: "Sella", thai: "เซลลา" },
  { english: "Senn", thai: "เซนน์" },
  { english: "Hessa", thai: "เฮสซา" },
  { english: "Oren", thai: "โอเรน" },
  { english: "Noll", thai: "นอล" },
  { english: "Varric", thai: "วาร์ริก" },
  { english: "Hearth", thai: "ฮาร์ธ" },
  { english: "Black Guard", thai: "แบล็กการ์ด" },
  { english: "Frostfang", thai: "ฟรอสต์แฟง" },
  { english: "Reinhardt", thai: "ไรน์ฮาร์ด" },
  { english: "Seraphina", thai: "เซราฟินา" },
  { english: "Valcrest", thai: "วาลเครสต์" },
  { english: "Valtieri", thai: "วัลเทียรี" },
  { english: "Duremont", thai: "ดูเรมอนต์" },
  { english: "Velmora", thai: "เวลมอรา" },
  { english: "Varelia", thai: "วาเรเลีย" },
  { english: "Drakhar", thai: "ดราคฮาร์" },
  { english: "Eryndor", thai: "เอรินดอร์" },
  { english: "Aurelis", thai: "ออเรลิส" },
  { english: "Aurelius", thai: "ออเรเลียส" },
  { english: "Alistair", thai: "อลิสแตร์" },
  { english: "Patrick", thai: "แพททริค" },
  { english: "Cedric", thai: "เซดริก" },
  { english: "Magnus", thai: "แม็กนัส" },
  { english: "Adrian", thai: "เอเดรียน" },
  { english: "Eldric", thai: "เอลดริก" },
  { english: "Aldren", thai: "อัลเดรน" },
  { english: "Arcelia", thai: "อาร์เซเลีย" },
  { english: "Rensveil", thai: "เรนส์เวล" },
  { english: "Veymar", thai: "เวย์มาร์" },
  { english: "Aresia", thai: "อาเรเซีย" },
  { english: "Lacoss", thai: "ลาคอส" },
  { english: "Alcine", thai: "แอลซีน" },
  { english: "Draven", thai: "เดรเวน" },
  { english: "Alvis", thai: "อัลวิส" },
  { english: "Rowan", thai: "โรวัน" },
  { english: "Elias", thai: "อีเลียส" },
  { english: "Kael", thai: "เคล" },
  { english: "Vael", thai: "เวล" },
  { english: "Eli", thai: "อีไล" },
];

const nameLookup = new Map(nameEntries.map((entry) => [entry.english, entry]));
const namePattern = new RegExp(
  `(^|[^A-Za-z])(${nameEntries
    .map((entry) => entry.english)
    .sort((a, b) => b.length - a.length)
    .map(escapeRegExp)
    .join("|")})(?![A-Za-z])`,
  "g",
);

let viewMode = getInitialViewMode();
let activeIndex = getInitialChapterIndex();
let fontScale = Number(localStorage.getItem("astrael-reader-font-scale") ?? 1);
let nameMode = getSavedNameMode();

init();

function init() {
  applySavedTheme();
  applyFontScale();
  applyNameModeControl();
  bindEvents();
  renderChapter(activeIndex);
}

function bindEvents() {
  searchInput.addEventListener("input", () => {
    renderChapterList(filterChapters(searchInput.value.trim()));
  });

  prevButton.addEventListener("click", () => navigateChapter(-1));
  nextButton.addEventListener("click", () => navigateChapter(1));

  viewTabs.forEach((tab) => {
    tab.addEventListener("click", () => setViewMode(tab.dataset.view));
    tab.addEventListener("keydown", (event) => {
      const keys = ["ArrowLeft", "ArrowRight", "Home", "End"];
      if (!keys.includes(event.key)) {
        return;
      }
      event.preventDefault();
      const nextTab = event.key === "Home"
        ? viewTabs[0]
        : event.key === "End"
          ? viewTabs[viewTabs.length - 1]
          : viewTabs[(viewTabs.indexOf(tab) + 1) % viewTabs.length];
      setViewMode(nextTab.dataset.view);
      nextTab.focus();
    });
  });

  chapterContent.addEventListener("click", (event) => {
    const novelButton = event.target.closest("[data-open-novel]");
    if (novelButton) {
      setViewMode("novel", novelButton.dataset.openNovel);
      document.querySelector("#novel-tab").focus();
    }
    if (event.target.closest("[data-reader-top]")) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      document.querySelector("#comic-tab").focus({ preventScroll: true });
    }
  });

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
  nameModeSelect?.addEventListener("change", () => {
    nameMode = nameModeValues.has(nameModeSelect.value) ? nameModeSelect.value : "english";
    localStorage.setItem(NAME_MODE_KEY, nameMode);
    renderChapter(activeIndex);
  });

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
          <span>${chapterLabel(chapter)}</span>
          <strong>${inline(viewMode === "comic" ? comicChapters[chapter.number].title : chapter.title)}</strong>
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
  const comic = comicChapters[chapter.number];
  const isComic = viewMode === "comic";
  const title = isComic ? comic.title : chapter.title;
  const available = getAvailableChapters();
  const currentPosition = available.indexOf(chapter);

  document.body.dataset.view = viewMode;
  viewTabs.forEach((tab) => {
    const selected = tab.dataset.view === viewMode;
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });
  document.querySelectorAll(".novel-control").forEach((control) => {
    control.hidden = isComic;
  });
  chapterContent.setAttribute("aria-labelledby", `${viewMode}-tab`);
  chapterContent.classList.toggle("comic-content", isComic);
  chapterKicker.textContent = chapterLabel(chapter);
  chapterTitle.innerHTML = inline(title);
  readerMeta.hidden = !isComic;
  readerMeta.textContent = isComic
    ? `จากนิยายตอนที่ ${formatChapterNumbers(comic.novelChapters)} · ${comic.pages.length} หน้า · เลื่อนลงเพื่ออ่านต่อ`
    : "";
  chapterContent.innerHTML = isComic ? renderComic(chapter, comic) : renderMarkdown(chapter.content);
  prevButton.disabled = currentPosition <= 0;
  nextButton.disabled = currentPosition === available.length - 1;
  chapterNav.hidden = isComic && available.length < 2;
  document.title = `${chapterLabel(chapter)} - ${title} | Astrael`;
  renderChapterList(filterChapters(searchInput.value.trim()));
  updateReaderUrl(chapter);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function getAvailableChapters() {
  return viewMode === "comic"
    ? chapters.filter((chapter) => comicChapters[chapter.number]?.pages?.length)
    : chapters;
}

function formatChapterNumbers(numbers) {
  return numbers.length < 2
    ? numbers.join("")
    : `${numbers.slice(0, -1).join(", ")} และ ${numbers[numbers.length - 1]}`;
}

function chapterLabel(chapter) {
  return viewMode === "comic"
    ? `การ์ตูนตอนที่ ${chapter.number}`
    : chapter.number === "0" ? "ตอน 00" : `ตอน ${chapter.number}`;
}

function navigateChapter(direction) {
  const available = getAvailableChapters();
  const position = available.indexOf(chapters[activeIndex]);
  const nextChapter = available[position + direction];
  if (nextChapter) {
    renderChapter(chapters.indexOf(nextChapter));
  }
}

function setViewMode(mode, requestedNovelNumber) {
  if (mode !== "novel" && mode !== "comic") {
    return;
  }
  const previousMode = viewMode;
  const previousNumber = chapters[activeIndex]?.number;
  viewMode = mode;
  localStorage.setItem(VIEW_MODE_KEY, mode);
  const available = getAvailableChapters();
  if (mode === "novel") {
    const novelNumber = requestedNovelNumber
      ?? (previousMode === "comic" ? comicChapters[previousNumber]?.novelChapters[0] : null);
    const index = chapters.findIndex((chapter) => chapter.number === novelNumber);
    if (index >= 0) {
      activeIndex = index;
    }
  } else if (previousMode === "novel") {
    const matchingComic = Object.entries(comicChapters).find(([, comic]) =>
      comic.novelChapters.includes(previousNumber),
    );
    const index = chapters.findIndex((chapter) => chapter.number === matchingComic?.[0]);
    if (index >= 0) {
      activeIndex = index;
    }
  }
  if (!available.includes(chapters[activeIndex])) {
    const matchingComic = Object.entries(comicChapters).find(([, comic]) =>
      comic.novelChapters.includes(chapters[activeIndex]?.number),
    );
    const target = available.find((chapter) => chapter.number === matchingComic?.[0])
      ?? available.find((chapter) => chapter.number === "1")
      ?? available[0];
    activeIndex = chapters.indexOf(target);
  }
  renderChapter(activeIndex);
}

function getInitialViewMode() {
  const requested = new URLSearchParams(window.location.search).get("view");
  const saved = localStorage.getItem(VIEW_MODE_KEY);
  return (requested ?? saved) === "comic" ? "comic" : "novel";
}

function getInitialChapterIndex() {
  const requested = new URLSearchParams(window.location.search).get("chapter");
  const available = getAvailableChapters();
  const chapter = available.find((item) => item.number === requested)
    ?? available.find((item) => item.number === "1")
    ?? available[0];
  return chapters.indexOf(chapter);
}

function updateReaderUrl(chapter) {
  const url = new URL(window.location.href);
  url.searchParams.set("chapter", chapter.number);
  url.searchParams.set("view", viewMode);
  window.history.replaceState(null, "", url);
}

function renderComic(chapter, comic) {
  const pages = comic.pages;
  return `
    <div class="comic-pages" aria-label="การ์ตูนตอนที่ ${escapeAttribute(chapter.number)}">
      ${pages.map((page, index) => `
        <img class="comic-page"
          src="${escapeAttribute(page.src)}"
          alt="ตอนที่ ${escapeAttribute(chapter.number)} หน้า ${index + 1} จาก ${pages.length}: ${escapeAttribute(page.description)}"
          width="${page.width}" height="${page.height}"
          loading="${index === 0 ? "eager" : "lazy"}" decoding="async"
          ${index === 0 ? 'fetchpriority="high"' : ""}
        />
      `).join("")}
    </div>
    <div class="comic-end">
      <p>จบตอนที่ ${escapeHtml(chapter.number)}</p>
      <div class="comic-actions">
        ${comic.novelChapters.map((number) => `
          <button class="reader-action" type="button" data-open-novel="${escapeAttribute(number)}">อ่านนิยายตอนที่ ${escapeHtml(number)}</button>
        `).join("")}
        <button class="reader-action" type="button" data-reader-top>กลับขึ้นด้านบน ↑</button>
      </div>
    </div>
  `;
}

function filterChapters(query) {
  const normalized = query.toLocaleLowerCase("th");
  const available = getAvailableChapters();
  if (!normalized) {
    return available;
  }
  return available.filter((chapter) =>
    `${chapter.number} ${viewMode === "comic" ? comicChapters[chapter.number].title : chapter.title}`
      .toLocaleLowerCase("th").includes(normalized),
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
  return escapeHtml(formatNameText(text))
    .replace(/&lt;br \/&gt;/g, "<br />")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function formatNameText(text) {
  if (!text || nameMode === "english") {
    return text;
  }

  return text.replace(namePattern, (match, prefix, englishName) => {
    const entry = nameLookup.get(englishName);
    if (!entry) {
      return match;
    }

    return `${prefix}${formatNameEntry(entry)}`;
  });
}

function formatNameEntry(entry) {
  if (nameMode === "thai") {
    return entry.thai;
  }

  if (nameMode === "thai-english") {
    return `${entry.thai} (${entry.english})`;
  }

  return `${entry.english} (${entry.thai})`;
}

function getSavedNameMode() {
  const savedMode = localStorage.getItem(NAME_MODE_KEY);
  return nameModeValues.has(savedMode) ? savedMode : "english-thai";
}

function applyNameModeControl() {
  if (nameModeSelect == null) {
    return;
  }

  nameModeSelect.value = nameMode;
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

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
