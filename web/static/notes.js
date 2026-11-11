// omat lisäykset, puhuu notes-api:n kanssa gatewayn kautta

// ettei html mene sivulle sellaisenaan
function escapeHtml(text) {
  var div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// etusivun luku
var statNotes = document.getElementById("stat-notes");
if (statNotes) {
  fetch("/api/stats")
    .then(function (res) { return res.json(); })
    .then(function (data) { statNotes.textContent = data.notes; })
    .catch(function () { statNotes.textContent = "?"; });
}

var notesDiv = document.getElementById("notes");
var topic = notesDiv.dataset.topic;

if (topic) {
  notesDiv.hidden = false;
  var form = document.getElementById("note-form");
  var list = document.getElementById("note-list");
  var statusEl = document.getElementById("note-status");

  try { form.elements.author.value = localStorage.getItem("nimi") || ""; } catch (e) {}

  function showStatus(msg, isError) {
    statusEl.textContent = msg;
    statusEl.className = isError ? "error" : "ok";
    statusEl.hidden = false;
    setTimeout(function () { statusEl.hidden = true; }, 3000);
  }

  // sivun nimi ja linkki aiheesta (Kaikki lisäykset -sivulla)
  function topicLabel(t) {
    if (PAGES[t]) return '<a href="' + PAGES[t].url + '">' + escapeHtml(PAGES[t].title) + "</a>";
    return escapeHtml(t);
  }

  function loadNotes() {
    var params = new URLSearchParams();
    if (topic != "*") params.set("topic", topic);
    var name = form.elements.author.value.trim();
    if (form.elements.mine.checked && name) params.set("author", name);

    fetch("/api/notes?" + params)
      .then(function (res) {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(function (notes) {
        if (notes.length == 0) {
          list.innerHTML = '<li class="empty">Ei vielä lisäyksiä tälle sivulle.</li>';
          return;
        }
        list.innerHTML = notes.map(function (n) {
          var date = new Date(n.updated_at).toLocaleDateString("fi-FI");
          return (
            "<li>" +
            '<button class="delete" data-id="' + n.id + '" title="Poista">Poista</button>' +
            '<div class="info"><b>' + escapeHtml(n.author) + "</b>" +
            (topic == "*" ? " · " + topicLabel(n.topic) : "") +
            " · " + date + "</div>" +
            "<code>" + escapeHtml(n.title) + "</code>" +
            (n.body ? "<p>" + escapeHtml(n.body) + "</p>" : "") +
            "</li>"
          );
        }).join("");
      })
      .catch(function () {
        list.innerHTML = '<li class="empty">Lisäyksiä ei saatu haettua. Onko notes-api käynnissä?</li>';
      });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = form.querySelector("button");
    btn.disabled = true;
    try { localStorage.setItem("nimi", form.elements.author.value.trim()); } catch (e) {}

    fetch("/api/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        author: form.elements.author.value.trim(),
        topic: topic == "*" ? "yleinen" : topic,
        title: form.elements.title.value.trim(),
        body: form.elements.body.value.trim(),
      }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error();
        form.elements.title.value = "";
        form.elements.body.value = "";
        showStatus("Lisätty!", false);
        loadNotes();
      })
      .catch(function () {
        showStatus("Tallennus epäonnistui, yritä uudelleen.", true);
      })
      .finally(function () {
        btn.disabled = false;
      });
  });

  // poisto: ensimmäinen klikkaus kysyy varmistuksen
  list.addEventListener("click", function (e) {
    var btn = e.target.closest(".delete");
    if (!btn) return;
    if (!btn.classList.contains("confirm")) {
      btn.classList.add("confirm");
      btn.textContent = "Varmasti?";
      setTimeout(function () {
        btn.classList.remove("confirm");
        btn.textContent = "Poista";
      }, 3000);
      return;
    }
    fetch("/api/notes/" + btn.dataset.id, { method: "DELETE" }).then(loadNotes);
  });

  form.elements.mine.addEventListener("change", loadNotes);
  loadNotes();
}
