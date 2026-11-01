(function () {
  var C = window.LAMDA || {};
  var html = document.documentElement;
  // ---- language (Arabic RTL default, full English toggle) ----
  function setLang(l, save) {
    html.lang = l; html.dir = l === "ar" ? "rtl" : "ltr";
    var tt = html.getAttribute("data-title-" + l); if (tt) document.title = tt;
    document.querySelectorAll(".lang").forEach(function (b) { b.textContent = l === "ar" ? "English" : "عربي"; b.setAttribute("aria-label", l === "ar" ? "Switch to English" : "التحويل للعربي"); });
    if (save) try { localStorage.setItem("lamda_lang", l); } catch (e) {}
  }
  var q = new URLSearchParams(location.search).get("lang"), saved = null;
  try { saved = localStorage.getItem("lamda_lang"); } catch (e) {}
  setLang(q === "en" || q === "ar" ? q : (saved || "ar"), false);
  document.querySelectorAll(".lang").forEach(function (b) { b.addEventListener("click", function () { setLang(html.lang === "ar" ? "en" : "ar", true); }); });

  // ---- config-driven links ----
  document.querySelectorAll("[data-apk]").forEach(function (a) { if (C.apkUrl) a.href = C.apkUrl; });
  document.querySelectorAll("[data-version]").forEach(function (e) { e.textContent = C.version || ""; });
  document.querySelectorAll("[data-size]").forEach(function (e) { e.textContent = C.apkSizeMb || ""; });
  document.querySelectorAll("[data-sha]").forEach(function (e) { e.textContent = C.apkSha256 || ""; });
  document.querySelectorAll("[data-mail]").forEach(function (a) { a.href = "mailto:" + C.contactEmail; if (!a.children.length) a.textContent = C.contactEmail; });
  document.querySelectorAll("[data-social]").forEach(function (a) { var u = (C.social || {})[a.getAttribute("data-social")]; if (u) a.href = u; });
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  // ---- scroll reveal ----
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (e) { io.observe(e); });
  } else els.forEach(function (e) { e.classList.add("in"); });

  // ---- hero: orb flies and writes "Lamda" (same stroke as the app splash) ----
  var stage = document.querySelector(".stage");
  if (stage) {
    var path = stage.querySelector("#ink"), glow = stage.querySelector("#inkglow"), orb = stage.querySelector(".orb"), svg = stage.querySelector("svg.script");
    var L = path.getTotalLength(), DUR = 3200, t0 = null;
    [path, glow].forEach(function (p) { p.style.strokeDasharray = L; p.style.strokeDashoffset = reduce ? 0 : L; });
    function place(len, extraY) {
      var p = path.getPointAtLength(len), r = svg.getBoundingClientRect(), s = r.width / 1000;
      orb.style.left = (p.x * s) + "px"; orb.style.top = (p.y * s - r.width * 0.085 + (extraY || 0)) + "px";
    }
    function ease(x) { return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
    function frame(ts) {
      if (t0 === null) t0 = ts;
      var k = Math.min(1, (ts - t0) / DUR), e = ease(k), len = L * e;
      path.style.strokeDashoffset = L - len; glow.style.strokeDashoffset = L - len;
      place(Math.max(1, len), Math.sin(ts / 180) * 4);
      if (k < 1) requestAnimationFrame(frame); else hover(ts);
    }
    function hover() { // after writing: gentle float at the end of the word
      function f(ts) { place(L, Math.sin(ts / 600) * 8); requestAnimationFrame(f); }
      requestAnimationFrame(f);
    }
    if (reduce) place(L, 0); else requestAnimationFrame(frame);
    addEventListener("resize", function () { if (reduce) place(L, 0); });
  }

  // ---- carousel ----
  document.querySelectorAll(".carousel").forEach(function (c) {
    var tr = c.querySelector(".track");
    c.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var d = +b.getAttribute("data-dir") * (html.dir === "rtl" ? -1 : 1);
        tr.scrollBy({ left: d * 276, behavior: reduce ? "auto" : "smooth" });
      });
    });
  });

  // ---- pricing toggle ----
  var tg = document.querySelector(".toggle");
  if (tg) tg.addEventListener("click", function (ev) {
    var b = ev.target.closest("button"); if (!b) return;
    var per = b.getAttribute("data-period");
    tg.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    document.querySelectorAll("[data-m]").forEach(function (e) { e.textContent = e.getAttribute(per === "y" ? "data-y" : "data-m"); });
    document.querySelectorAll("[data-per]").forEach(function (e) { e.hidden = e.getAttribute("data-per") !== per; });
  });

  // ---- tabs (install guide) ----
  document.querySelectorAll("[role=tablist]").forEach(function (tl) {
    var tabs = tl.querySelectorAll("[role=tab]");
    function sel(t) {
      tabs.forEach(function (x) { var on = x === t; x.setAttribute("aria-selected", on); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute("aria-controls")).hidden = !on; });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { sel(t); });
      t.addEventListener("keydown", function (e) {
        var n = { ArrowRight: 1, ArrowLeft: -1 }[e.key]; if (!n) return;
        if (html.dir === "rtl") n = -n; var j = (i + n + tabs.length) % tabs.length; tabs[j].focus(); sel(tabs[j]);
      });
    });
    var h = location.hash.replace("#", ""); var pre = h && tl.querySelector("[aria-controls=" + h + "]"); if (pre) sel(pre);
  });
})();
