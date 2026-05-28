// Persistent state + alignment helpers for the Coulesia story.
// Two axes: law (positive = Lawful, negative = Chaotic) and good (positive = Good, negative = Evil).
// Each choice page declares deltas on its choice buttons via data attributes.

const STORAGE_KEY = "coulesia.story.v1";

const DEFAULT_STATE = Object.freeze({
  name: "",
  gender: "",
  law: 0,
  good: 0,
  history: [],
});

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULT_STATE };
    const parsed = JSON.parse(raw);
    return { ...DEFAULT_STATE, ...parsed };
  } catch {
    return { ...DEFAULT_STATE };
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function resetState() {
  localStorage.removeItem(STORAGE_KEY);
}

function alignmentLabel(state) {
  // Bucket each axis into [-X, low, mid, high, +X] thresholds; threshold of 2 separates buckets.
  const T = 2;
  const lawBucket = state.law >= T ? "Lawful" : state.law <= -T ? "Chaotic" : "Neutral";
  const goodBucket = state.good >= T ? "Good" : state.good <= -T ? "Evil" : "Neutral";
  if (lawBucket === "Neutral" && goodBucket === "Neutral") return "True Neutral";
  return `${lawBucket} ${goodBucket}`;
}

function recordVisit(nodeId) {
  const state = loadState();
  if (state.history[state.history.length - 1] !== nodeId) {
    state.history.push(nodeId);
    saveState(state);
  }
}

function applyChoice({ next, law = 0, good = 0 }) {
  const state = loadState();
  state.law += law;
  state.good += good;
  state.history.push(next);
  saveState(state);
  window.location.href = `${next}.html`;
}

function wireChoices(root = document) {
  root.querySelectorAll("[data-next]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      applyChoice({
        next: btn.dataset.next,
        law: Number(btn.dataset.law || 0),
        good: Number(btn.dataset.good || 0),
      });
    });
  });
}

function renderReadout() {
  const el = document.getElementById("alignment-readout");
  if (!el) return;
  const s = loadState();
  el.textContent = `${alignmentLabel(s)} · L${s.law >= 0 ? "+" : ""}${s.law} G${s.good >= 0 ? "+" : ""}${s.good}`;
}

function bootNode(nodeId) {
  recordVisit(nodeId);
  wireChoices();
  renderReadout();
  // Hold shift+A on any page to toggle the alignment readout for debugging.
  document.addEventListener("keydown", (e) => {
    if (e.shiftKey && (e.key === "A" || e.key === "a")) {
      document.body.classList.toggle("show-alignment");
    }
  });
}

window.Story = { loadState, saveState, resetState, alignmentLabel, applyChoice, bootNode };
