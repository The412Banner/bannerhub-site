/* BannerHub site — interactivity (progressive enhancement; site works without JS) */
(function () {
  "use strict";

  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", links.classList.contains("open"));
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") links.classList.remove("open");
    });
  }

  // Mark active nav link by pathname
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(function (a) {
    var href = a.getAttribute("href");
    if (href === here || (here === "" && href === "index.html")) a.classList.add("active");
  });

  // FAQ accordion: close siblings on open (one-open-at-a-time)
  var faqGroups = document.querySelectorAll(".faq");
  faqGroups.forEach(function (group) {
    var items = group.querySelectorAll("details");
    items.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (d.open) items.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });

  // Fade-up on scroll
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    document.querySelectorAll(".fade-up").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".fade-up").forEach(function (el) { el.classList.add("in"); });
  }

  // Year stamp
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
