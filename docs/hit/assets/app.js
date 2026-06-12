/* SimSage HIT prototype — minimal demo interactions only.
   Static mockup: nothing talks to a backend or calculates real results.
   It just makes the click-through feel alive for review. */
(function () {
  "use strict";

  function onReady(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  onReady(function () {
    // Default any empty date field to today.
    var today = new Date().toISOString().slice(0, 10);
    document.querySelectorAll('input[type="date"]').forEach(function (el) {
      if (!el.value) el.value = today;
    });

    // "Recommended Sieve Size" helper — nearest standard sieve at/below the
    // rock lower size. Demo only, not the production calculation.
    var SIEVES = [1, 1.18, 1.7, 2.36, 3.35, 4.75, 6.7, 9.5, 13.2, 16, 19, 22.4, 26.5];
    var sieveBtn = document.querySelector("[data-sieve-btn]");
    if (sieveBtn) {
      sieveBtn.addEventListener("click", function () {
        var lower = parseFloat((document.querySelector('[name="rock_lower_size"]') || {}).value);
        var out = document.querySelector("[data-sieve-out]");
        if (!out) return;
        var pick = SIEVES[0];
        for (var i = 0; i < SIEVES.length; i++) {
          if (SIEVES[i] <= (isNaN(lower) ? 1 : lower)) pick = SIEVES[i];
        }
        out.value = pick.toFixed(2);
      });
    }

    // Show a chosen file name in the upload dropzone.
    document.querySelectorAll('input[type="file"][data-file-out]').forEach(function (input) {
      input.addEventListener("change", function () {
        var target = document.querySelector(input.getAttribute("data-file-out"));
        if (target && input.files && input.files.length) {
          target.textContent = input.files[0].name;
        }
      });
    });

    // Buttons/links flagged as inert demo actions: acknowledge without navigating.
    document.querySelectorAll("[data-demo]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var note = el.getAttribute("data-demo") || "Demo only — no file is generated in this prototype.";
        var box = document.querySelector("[data-demo-note]");
        if (box) { box.textContent = note; box.hidden = false; }
      });
    });

    // Static-mockup navigation: forms with data-goto just navigate, never POST.
    document.querySelectorAll("form[data-goto]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        window.location.href = form.getAttribute("data-goto");
      });
    });

    // Back-to-top button (long doc pages). Shows after scrolling down.
    var toTop = document.querySelector("[data-to-top]");
    if (toTop) {
      var toggleToTop = function () {
        toTop.classList.toggle("is-visible", window.scrollY > 400);
      };
      window.addEventListener("scroll", toggleToTop, { passive: true });
      toggleToTop();
      toTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
  });
})();
