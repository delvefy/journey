// Persistent state + alignment-keyed routing for the Coulesia story.
// Two axes: law (positive = Lawful, negative = Chaotic) and good (positive = Good, negative = Evil).
// Each choice button declares its alignment nudge via data-law and data-good attributes.
// After deltas are applied, the player is routed to the next level's node whose
// alignment-code matches the new bucket. Node IDs are "<level>-<alignment-code>"
// for levels 2 and above; level 0 is a single intro node and level 1 is gender-distinct.

const STORAGE_KEY = "coulesia.story.v1";
const BUCKET_THRESHOLD = 2;

const DEFAULT_STATE = Object.freeze({
  name: "",
  gender: "",
  law: 0,
  good: 0,
  history: [],
});

let CURRENT_NODE_ID = null;

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

function lawCode(law) {
  if (law >= BUCKET_THRESHOLD) return "l";
  if (law <= -BUCKET_THRESHOLD) return "c";
  return "n";
}

function goodCode(good) {
  if (good >= BUCKET_THRESHOLD) return "g";
  if (good <= -BUCKET_THRESHOLD) return "e";
  return "n";
}

function alignmentCode(state) {
  const l = lawCode(state.law);
  const g = goodCode(state.good);
  if (l === "n" && g === "n") return "tn";
  return `${l}${g}`;
}

function alignmentLabel(state) {
  const law = state.law >= BUCKET_THRESHOLD ? "Lawful" : state.law <= -BUCKET_THRESHOLD ? "Chaotic" : "Neutral";
  const good = state.good >= BUCKET_THRESHOLD ? "Good" : state.good <= -BUCKET_THRESHOLD ? "Evil" : "Neutral";
  if (law === "Neutral" && good === "Neutral") return "True Neutral";
  return `${law} ${good}`;
}

function recordVisit(nodeId) {
  const state = loadState();
  if (state.history[state.history.length - 1] !== nodeId) {
    state.history.push(nodeId);
    saveState(state);
  }
}

function currentLevel() {
  if (!CURRENT_NODE_ID) return 0;
  const [level] = CURRENT_NODE_ID.split("-");
  return Number(level);
}

function applyChoice({ law = 0, good = 0 }) {
  const state = loadState();
  state.law += law;
  state.good += good;
  const next = `${currentLevel() + 1}-${alignmentCode(state)}`;
  state.history.push(next);
  saveState(state);
  window.location.href = `${next}.html`;
}

function wireChoices(root = document) {
  root.querySelectorAll("button.choice[data-law], button.choice[data-good]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      applyChoice({
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
  CURRENT_NODE_ID = nodeId;
  recordVisit(nodeId);
  wireChoices();
  renderReadout();
  document.addEventListener("keydown", (e) => {
    if (e.shiftKey && (e.key === "A" || e.key === "a")) {
      document.body.classList.toggle("show-alignment");
    }
  });
}

window.Story = { loadState, saveState, resetState, alignmentLabel, alignmentCode, applyChoice, bootNode };
