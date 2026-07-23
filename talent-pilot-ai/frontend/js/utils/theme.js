import { THEME_STORAGE_KEY } from "../config.js";

const THEMES = ["light", "dark"];

function systemPrefersDark() {
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

export function getStoredTheme() {
  const stored = localStorage.getItem(THEME_STORAGE_KEY);
  if (stored && THEMES.includes(stored)) return stored;
  return systemPrefersDark() ? "dark" : "light";
}

export function applyTheme(theme) {
  const next = THEMES.includes(theme) ? theme : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem(THEME_STORAGE_KEY, next);
  const label = document.getElementById("theme-label");
  if (label) label.textContent = next === "dark" ? "Dark" : "Light";
  return next;
}

export function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || getStoredTheme();
  return applyTheme(current === "dark" ? "light" : "dark");
}

export function initTheme() {
  applyTheme(getStoredTheme());
  const toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      toggleTheme();
    });
  }
}
