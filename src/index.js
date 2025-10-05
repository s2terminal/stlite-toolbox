// @ts-check

// @ts-ignore
import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js";

const PYTHON_CODE = `
import streamlit as st

st.title("stlite app!")

name = st.text_input('名前を入力してください')
st.write("Hello,", name or "world")
`;

mount(
  PYTHON_CODE.trim(),
  document.getElementById("root"),
);
