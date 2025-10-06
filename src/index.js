// @ts-check

// @ts-ignore
import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js";

async function startStlite() {
  const FILES = [
    "streamlit_app.py",
    "pages/char_count.py",
  ];

  const files = FILES.reduce((acc, file) => {
    acc[file] = { url: `./src_py/${file}` };
    return acc;
  }, /** @type {Record<string, {url: string}>} */ ({}));

  mount(
    { entrypoint: FILES[0], files },
    document.getElementById("root"),
  );
}

startStlite();
