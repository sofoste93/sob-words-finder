const translations = {
  en: {
    systems: "ALL SYSTEMS NOMINAL", finder: "Finder", settings: "Settings", help: "Help",
    headline: "Find the signal<br><em>inside the noise.</em>", lede: "Scan a local document for any word or phrase. Your files stay aboard this machine.",
    console: "SCAN CONSOLE", target: "Define your target", local: "LOCAL ONLY", source: "Source",
    sample: "Mission log", sampleHint: "Try the onboard sample", document: "Your document", documentHint: "TXT · PDF · DOCX + more",
    drop: "Drop a document or browse", limit: "Up to 16 MB · processed in memory", query: "WORD OR PHRASE", launch: "Launch scan",
    telemetry: "Telemetry", velocity: "VELOCITY", altitude: "ALTITUDE", orbit: "ORBIT", stable: "STABLE", thor: "Transmission complete.",
    occurrences: "OCCURRENCES", locations: "LOCATIONS", scanned: "SCANNED", settingsTitle: "Tune the scanner.",
    settingsIntro: "Your preferences are saved locally in this browser.", language: "Interface language", case: "Case-sensitive",
    caseHint: "Distinguish Signal from signal", whole: "Whole words", wholeHint: "Exclude partial matches", motion: "Reduce motion",
    motionHint: "Pause ambient animation", resultLimit: "Result limit", resultHint: "Locations displayed per scan",
    helpTitle: "Ready for launch.", helpIntro: "Everything you need for a clean first scan.", helpOneTitle: "Choose a source",
    helpOne: "Use the mission log for a quick test or select a document from your device.", helpTwoTitle: "Set the target",
    helpTwo: "Enter a word or a phrase. Fine-tune matching rules in Settings.", helpThreeTitle: "Read the report",
    helpThree: "Each result shows its line, page, or paragraph and a contextual excerpt.", privacyTitle: "Private by design",
    privacy: "Documents are processed in memory and never uploaded to a remote service. Closing the app clears them.",
    scanning: "Scanning…", acquired: "Signal acquired", noSignal: "No signal detected", noMatch: "No match in this document.",
    selectFile: "Choose a document before starting the scan.", result: "result", results: "results", hidden: "More locations exist beyond your display limit."
  },
  fr: {
    systems: "TOUS SYSTÈMES NOMINAUX", finder: "Recherche", settings: "Réglages", help: "Aide",
    headline: "Trouvez le signal<br><em>dans le bruit.</em>", lede: "Analysez un document local pour trouver un mot ou une phrase. Vos fichiers restent à bord de cette machine.",
    console: "CONSOLE DE SCAN", target: "Définissez votre cible", local: "100 % LOCAL", source: "Source",
    sample: "Journal de mission", sampleHint: "Essayez l’exemple embarqué", document: "Votre document", documentHint: "TXT · PDF · DOCX + autres",
    drop: "Déposez un document ou parcourez", limit: "16 Mo max · traité en mémoire", query: "MOT OU PHRASE", launch: "Lancer le scan",
    telemetry: "Télémétrie", velocity: "VITESSE", altitude: "ALTITUDE", orbit: "ORBITE", stable: "STABLE", thor: "Transmission terminée.",
    occurrences: "OCCURRENCES", locations: "POSITIONS", scanned: "ANALYSÉS", settingsTitle: "Réglez le scanner.",
    settingsIntro: "Vos préférences sont enregistrées localement dans ce navigateur.", language: "Langue de l’interface", case: "Respecter la casse",
    caseHint: "Distinguer Signal de signal", whole: "Mots entiers", wholeHint: "Exclure les correspondances partielles", motion: "Réduire les animations",
    motionHint: "Suspendre les animations d’ambiance", resultLimit: "Limite de résultats", resultHint: "Positions affichées par scan",
    helpTitle: "Prêt au lancement.", helpIntro: "Tout ce qu’il faut pour réussir votre premier scan.", helpOneTitle: "Choisissez une source",
    helpOne: "Utilisez le journal de mission pour un essai rapide ou choisissez un document sur votre appareil.", helpTwoTitle: "Fixez la cible",
    helpTwo: "Saisissez un mot ou une phrase. Affinez la recherche dans Réglages.", helpThreeTitle: "Lisez le rapport",
    helpThree: "Chaque résultat indique sa ligne, page ou paragraphe avec un extrait du contexte.", privacyTitle: "Privé par conception",
    privacy: "Les documents sont traités en mémoire et ne sont jamais envoyés à un service distant. Fermer l’app les efface.",
    scanning: "Scan en cours…", acquired: "Signal acquis", noSignal: "Aucun signal détecté", noMatch: "Aucune correspondance dans ce document.",
    selectFile: "Choisissez un document avant de lancer le scan.", result: "résultat", results: "résultats", hidden: "D’autres positions existent au-delà de votre limite d’affichage."
  }
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const saved = JSON.parse(localStorage.getItem("sob-settings") || "{}");
const settings = { language: saved.language || "en", caseSensitive: !!saved.caseSensitive, wholeWord: !!saved.wholeWord,
  reduceMotion: !!saved.reduceMotion, resultLimit: saved.resultLimit || "50" };

function persist() {
  localStorage.setItem("sob-settings", JSON.stringify(settings));
}

function setLanguage(language) {
  settings.language = language;
  document.documentElement.lang = language;
  $$('[data-i18n]').forEach((node) => {
    const value = translations[language][node.dataset.i18n];
    if (value) node.innerHTML = value;
  });
  persist();
}

function showView(name) {
  $$('[data-view-panel]').forEach((panel) => {
    const active = panel.dataset.viewPanel === name;
    panel.hidden = !active;
    panel.classList.toggle("active", active);
  });
  $$('[data-view]').forEach((button) => button.classList.toggle("active", button.dataset.view === name));
  window.scrollTo({ top: 0, behavior: settings.reduceMotion ? "auto" : "smooth" });
}

$$('[data-view]').forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));

const sourceInputs = $$('input[name="source"]');
const dropZone = $('#drop-zone');
const fileInput = $('#file');
sourceInputs.forEach((input) => input.addEventListener("change", () => { dropZone.hidden = input.value !== "upload" || !input.checked; }));

function setFile(file) {
  if (!file) return;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  fileInput.files = transfer.files;
  $('#file-label').textContent = file.name;
}
fileInput.addEventListener("change", () => setFile(fileInput.files[0]));
["dragenter", "dragover"].forEach((event) => dropZone.addEventListener(event, (e) => { e.preventDefault(); dropZone.classList.add("dragging"); }));
["dragleave", "drop"].forEach((event) => dropZone.addEventListener(event, (e) => { e.preventDefault(); dropZone.classList.remove("dragging"); }));
dropZone.addEventListener("drop", (event) => setFile(event.dataTransfer.files[0]));

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = value;
  return element.innerHTML;
}

function highlight(value, query) {
  const safe = escapeHtml(value);
  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return safe.replace(new RegExp(`(${escapedQuery})`, settings.caseSensitive ? "g" : "gi"), "<mark>$1</mark>");
}

function unitLabel(unit, number) {
  const labels = { en: { line: "Line", page: "Page", paragraph: "Paragraph" }, fr: { line: "Ligne", page: "Page", paragraph: "Paragraphe" } };
  return `${labels[settings.language][unit] || unit} ${String(number).padStart(2, "0")}`;
}

function renderResults(data) {
  const t = translations[settings.language];
  $('#results-panel').hidden = false;
  $('#results-title').textContent = data.occurrences ? t.acquired : t.noSignal;
  $('#results-file').textContent = `${data.filename} · “${data.query}”`;
  $('#occurrences').textContent = data.occurrences;
  $('#matched').textContent = data.matchedUnits;
  $('#scanned').textContent = data.scannedUnits;
  const list = $('#result-list');
  if (!data.results.length) {
    list.innerHTML = `<p class="empty-state">${t.noMatch}</p>`;
  } else {
    list.innerHTML = data.results.map((item) => `<article class="result-item"><span class="location">${unitLabel(data.unit, item.number)}</span><p>${highlight(item.preview, data.query)}</p><span class="count">${item.occurrences} ${item.occurrences === 1 ? t.result : t.results}</span></article>`).join("") + (data.truncated ? `<p class="empty-state">${t.hidden}</p>` : "");
  }
  $('#results-panel').scrollIntoView({ behavior: settings.reduceMotion ? "auto" : "smooth", block: "start" });
}

$('#search-form').addEventListener("submit", async (event) => {
  event.preventDefault();
  const t = translations[settings.language];
  const form = event.currentTarget;
  const button = form.querySelector('button[type="submit"]');
  const source = form.querySelector('input[name="source"]:checked').value;
  if (source === "upload" && !fileInput.files.length) { $('#form-message').textContent = t.selectFile; return; }
  const payload = new FormData(form);
  payload.set("caseSensitive", String(settings.caseSensitive));
  payload.set("wholeWord", String(settings.wholeWord));
  payload.set("limit", settings.resultLimit);
  $('#form-message').textContent = "";
  button.disabled = true;
  button.querySelector('span').textContent = t.scanning;
  try {
    const response = await fetch("/api/search", { method: "POST", body: payload });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Scan failed");
    renderResults(data);
  } catch (error) {
    $('#form-message').textContent = error.message;
  } finally {
    button.disabled = false;
    button.querySelector('span').textContent = t.launch;
  }
});

$('#language').value = settings.language;
$('#case-sensitive').checked = settings.caseSensitive;
$('#whole-word').checked = settings.wholeWord;
$('#reduce-motion').checked = settings.reduceMotion;
$('#result-limit').value = settings.resultLimit;
$('#language').addEventListener("change", (e) => setLanguage(e.target.value));
$('#case-sensitive').addEventListener("change", (e) => { settings.caseSensitive = e.target.checked; persist(); });
$('#whole-word').addEventListener("change", (e) => { settings.wholeWord = e.target.checked; persist(); });
$('#reduce-motion').addEventListener("change", (e) => { settings.reduceMotion = e.target.checked; document.body.classList.toggle("reduce-motion", settings.reduceMotion); persist(); });
$('#result-limit').addEventListener("change", (e) => { settings.resultLimit = e.target.value; persist(); });
document.body.classList.toggle("reduce-motion", settings.reduceMotion);
setLanguage(settings.language);

if (!settings.reduceMotion) {
  setInterval(() => {
    $('#velocity').textContent = (27580 + Math.round(Math.random() * 16 - 8)).toLocaleString(settings.language);
    $('#altitude').textContent = (408.2 + Math.random() * .6 - .3).toFixed(1);
  }, 1800);
}
