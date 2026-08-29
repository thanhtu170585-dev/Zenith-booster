/* ==========================================================
   SNEERYBOOSTER V1 — script.js
   White Frosted Gaming Control Center
   - No fake authentication
   - No secrets in frontend
   - API-ready placeholders for future backend
   ========================================================== */

// -------------------- API CONFIG (future backend) --------------------
/**
 * Central API configuration.
 * Keep this isolated so switching environments is trivial.
 * DO NOT put secrets / API keys here.
 */
const API_CONFIG = Object.freeze({
  BASE_URL: "https://api.sneerybooster.example.com", // placeholder — replace when backend is ready
  ENDPOINTS: Object.freeze({
    LOGIN: "/api/auth/login",
    REGISTER: "/api/auth/register",
    LOGOUT: "/api/auth/logout",
    ME: "/api/auth/me",
    LICENSE: "/api/license",
    LICENSE_ACTIVATE: "/api/license/activate",
    DEVICES: "/api/devices",
    DEVICE_BY_ID: (id) => `/api/devices/${encodeURIComponent(id)}`,
    GAME_PROFILES: "/api/game-profiles",
    GAME_PROFILE_BY_ID: (id) => `/api/game-profiles/${encodeURIComponent(id)}`,
    APP_LATEST: "/api/app/latest",
    APP_DOWNLOAD: "/api/app/download",
    NOTIFICATIONS: "/api/notifications",
    ACTIVITY: "/api/activity",
  }),
  // Optional changelog page — update when page exists
  CHANGELOG_URL: "#changelog",
  // External links — intentionally placeholder, do not invent
  DISCORD_URL: "pages/support.html",
  DOCS_URL: "pages/support.html",
});

/**
 * Build full API URL.
 * @param {string} endpoint
 * @returns {string}
 */
function apiUrl(endpoint) {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
}

// -------------------- SUPPORTED GAMES (reusable data) --------------------
/**
 * Supported games — used to render Supported Games section.
 * Paths are relative to index.html (public homepage).
 * For pages inside pages/ use ../assets/images/games/...
 * Logos are copied verbatim from the desktop app's "Game Logo" folder (no generation, no hotlink, no initials).
 * Real filenames: Roblox.webp, VALORANT.jpg, CS2.jpg, Fornite.png, Genshin Impact.PNG, Minecraft.jpg
 */
const supportedGames = Object.freeze([
  {
    name: "Roblox",
    logo: "assets/images/games/Roblox.webp",
    alt: "Roblox logo",
    status: "Profile Supported",
  },
  {
    name: "VALORANT",
    logo: "assets/images/games/VALORANT.jpg",
    alt: "VALORANT logo",
    status: "Profile Supported",
  },
  {
    name: "Counter-Strike 2",
    logo: "assets/images/games/CS2.jpg",
    alt: "Counter-Strike 2 logo",
    status: "Profile Supported",
  },
  {
    name: "Fortnite",
    logo: "assets/images/games/Fornite.png",
    alt: "Fortnite logo",
    status: "Profile Supported",
  },
  {
    name: "Genshin Impact",
    logo: "assets/images/games/Genshin Impact.PNG",
    alt: "Genshin Impact logo",
    status: "Profile Supported",
  },
  {
    name: "Minecraft",
    logo: "assets/images/games/Minecraft.jpg",
    alt: "Minecraft logo",
    status: "Profile Supported",
  },
]);

/**
 * Optional helper to render games dynamically (if #gamesGrid is used).
 * Keeps existing static HTML intact — non-destructive enhancement.
 */
function renderSupportedGames(targetId = "gamesGrid") {
  const grid = document.getElementById(targetId);
  if (!grid || grid.dataset.rendered === "true") return;
  // If grid already has correct images, do not overwrite
  const hasLogos = grid.querySelectorAll(".game-logo img").length === supportedGames.length;
  if (hasLogos) return;
  grid.innerHTML = supportedGames
    .map(
      (g) => `
    <div class="game-card reveal visible">
      <div class="game-logo">
        <img src="${g.logo}" alt="${g.alt}" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='grid';" />
        <div class="game-logo-fallback" aria-hidden="true" style="display:none">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 11h10"/><path d="M8 6h8"/><path d="M8 18h8"/><rect x="4" y="4" width="16" height="16" rx="2"/></svg>
        </div>
      </div>
      <h3>${g.name}</h3>
      <p><span class="dot-green"></span> ${g.status}</p>
    </div>`
    )
    .join("");
  grid.dataset.rendered = "true";
}

// -------------------- AUTH STATE (placeholder, no fake logic) --------------------
/**
 * Return the current authenticated user or null.
 * Future implementation should call: GET /api/auth/me with credentials: 'include'
 * or Authorization header. For now it returns null (unauthenticated).
 *
 * IMPORTANT: Do not store passwords or tokens in localStorage.
 * Use httpOnly secure cookies or secure token handling via backend.
 *
 * @returns {Promise<null|object>}
 */
async function getCurrentUser() {
  // Placeholder for future:
  // try {
  //   const res = await fetch(apiUrl(API_CONFIG.ENDPOINTS.ME), { credentials: 'include' });
  //   if (!res.ok) return null;
  //   return await res.json();
  // } catch { return null; }
  return null;
}

/**
 * Update navbar auth actions based on auth state.
 * Shows Dashboard when authenticated, otherwise Login / Get Started.
 */
async function syncAuthUI() {
  const user = await getCurrentUser();
  const authSlot = document.getElementById("authSlot");
  const mobileAuthSlot = document.getElementById("mobileAuthSlot");
  if (!authSlot) return;

  if (user) {
    authSlot.innerHTML = `<a href="pages/dashboard.html" class="btn-primary">Dashboard</a>`;
    if (mobileAuthSlot) {
      mobileAuthSlot.innerHTML = `<a href="pages/dashboard.html" class="btn-primary" style="flex:1">Dashboard</a>`;
    }
  } else {
    authSlot.innerHTML = `
      <a href="pages/login.html" class="btn-ghost">Login</a>
      <a href="pages/register.html" class="btn-primary">Get Started</a>
    `;
    if (mobileAuthSlot) {
      mobileAuthSlot.innerHTML = `
        <a href="pages/login.html" class="btn-secondary" style="flex:1">Login</a>
        <a href="pages/register.html" class="btn-primary" style="flex:1">Get Started</a>
      `;
    }
  }
}

// -------------------- NAVIGATION --------------------
function initNavbar() {
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobileMenu");
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener("click", () => {
    const expanded = hamburger.getAttribute("aria-expanded") === "true";
    hamburger.setAttribute("aria-expanded", String(!expanded));
    mobileMenu.classList.toggle("open", !expanded);
    mobileMenu.setAttribute("aria-hidden", String(expanded));
  });

  // Close on link click
  mobileMenu.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => {
      hamburger.setAttribute("aria-expanded", "false");
      mobileMenu.classList.remove("open");
      mobileMenu.setAttribute("aria-hidden", "true");
    });
  });

  // Close on outside click / escape
  document.addEventListener("click", (e) => {
    if (!mobileMenu.classList.contains("open")) return;
    if (mobileMenu.contains(e.target) || hamburger.contains(e.target)) return;
    hamburger.setAttribute("aria-expanded", "false");
    mobileMenu.classList.remove("open");
    mobileMenu.setAttribute("aria-hidden", "true");
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      hamburger.setAttribute("aria-expanded", "false");
      mobileMenu.classList.remove("open");
      mobileMenu.setAttribute("aria-hidden", "true");
    }
  });
}

// Smooth scroll for Learn More / anchors
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

// Reveal on scroll (respects prefers-reduced-motion via CSS)
function initReveal() {
  const els = document.querySelectorAll(".reveal");
  if (!els.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    els.forEach((el) => el.classList.add("visible"));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  els.forEach((el) => io.observe(el));
}

// Year in footer
function initYear() {
  const y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
}

// Logo fallback is handled via <img onerror>; no extra JS needed

// -------------------- INIT --------------------
document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initSmoothScroll();
  initReveal();
  initYear();
  syncAuthUI();
  renderSupportedGames();
});
