// haku: näyttää vain ne taulukon rivit joissa hakusana on
// ja piilottaa osiot joista ei löydy mitään

var search = document.getElementById("search");
var content = document.querySelector(".content");
var noResults = document.getElementById("no-results");

// jaetaan sivu osioihin h2-otsikoiden mukaan
var sections = [];
var current = null;
Array.prototype.forEach.call(content.children, function (el) {
  if (el.tagName == "H1" || el.id == "no-results") return;
  if (el.tagName == "H2" || current == null) {
    current = { heading: el.tagName == "H2" ? el : null, items: [] };
    sections.push(current);
    if (el.tagName == "H2") return;
  }
  current.items.push(el);
});

function runSearch() {
  var q = search.value.toLowerCase().trim();
  var found = 0;

  sections.forEach(function (s) {
    var sectionHits = 0;
    s.items.forEach(function (el) {
      var rows = el.querySelectorAll ? el.querySelectorAll("tbody tr") : [];
      if (rows.length) {
        var hits = 0;
        rows.forEach(function (row) {
          var match = !q || row.textContent.toLowerCase().includes(q);
          row.hidden = !match;
          if (match) hits++;
        });
        el.hidden = hits == 0;
        sectionHits += hits;
      } else {
        // muut kuin taulukot piiloon haun ajaksi
        el.hidden = !!q;
      }
    });
    if (s.heading) s.heading.hidden = q && sectionHits == 0;
    found += sectionHits;
  });

  noResults.hidden = !(q && found == 0);
}

// sivuilla joilla ei ole taulukoita ei tarvita hakua
if (!content.querySelector("tbody tr")) {
  document.querySelector(".topbar").hidden = true;
} else {
  search.addEventListener("input", runSearch);
}

// "/" vie hakuun, esc tyhjentää
document.addEventListener("keydown", function (e) {
  var tag = document.activeElement.tagName;
  if (e.key == "/" && tag != "INPUT" && tag != "TEXTAREA") {
    e.preventDefault();
    search.focus();
  }
  if (e.key == "Escape" && document.activeElement == search) {
    search.value = "";
    runSearch();
    search.blur();
  }
});
