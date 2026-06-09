/* SimSage HIT prototype — minimal demo interactions only.
   This is a static mockup: nothing here talks to a backend or calculates
   real results. It just makes the click-through feel alive for the client. */
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

    // "Recommended Sieve Size" helper — picks the nearest standard sieve
    // below the rock lower size, from a representative sieve series.
    // Demo only: illustrative, not the production calculation.
    var SIEVES = [1, 1.18, 1.7, 2.36, 3.35, 4.75, 6.7, 9.5, 13.2, 16, 19, 22.4, 26.5];
    var sieveBtn = document.querySelector("[data-sieve-btn]");
    if (sieveBtn) {
      sieveBtn.addEventListener("click", function () {
        var lower = parseFloat(
          (document.querySelector('[name="rock_lower_size"]') || {}).value
        );
        var out = document.querySelector("[data-sieve-out]");
        if (!out) return;
        var pick = SIEVES[0];
        for (var i = 0; i < SIEVES.length; i++) {
          if (SIEVES[i] <= (isNaN(lower) ? 1 : lower)) pick = SIEVES[i];
        }
        out.value = pick.toFixed(2);
      });
    }

    // Static-mockup safety net: any form just navigates via the submit
    // button's data-goto, never actually POSTing anywhere.
    document.querySelectorAll("form[data-goto]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        window.location.href = form.getAttribute("data-goto");
      });
    });
  });
})();
