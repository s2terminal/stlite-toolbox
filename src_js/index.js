// @ts-check

// @ts-ignore
import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js";

const mainScript = await fetch('../src_py/streamlit_app.py').then(res => res.text());

mount(
  {
    entrypoint: "streamlit_app.py",
    files: {
      "streamlit_app.py": mainScript,
    },
  },
  document.getElementById("root"),
);
