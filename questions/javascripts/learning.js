(() => {
  const QUESTIONS = [
    "01-agent-vs-workflow",
    "02-react-and-agent-loop",
    "03-agent-stop-and-loop-control",
    "04-reliable-tool-calling",
    "05-context-engineering",
    "06-single-vs-multi-agent",
    "07-agent-evaluation",
    "08-production-rag",
    "09-agent-vs-model-and-components",
    "10-agent-patterns-task-decomposition-replanning",
    "11-reflection-reflexion-evaluator-optimizer",
    "12-coding-agent-verifiable-repair-loop",
    "13-framework-vs-custom-runtime",
    "14-agent-layered-security-defense",
    "15-badcase-attribution-and-data-flywheel",
    "16-agent-system-prompt-design",
    "17-few-shot-and-chain-of-thought-in-agents",
    "18-agent-prompt-robustness",
    "19-skill-tool-mcp-workflow-boundaries",
    "20-rag-chunking-and-contextual-retrieval",
    "21-embedding-model-selection-and-finetuning",
    "22-rag-query-routing-and-rewriting",
    "23-vector-index-selection",
    "24-hybrid-retrieval-and-rank-fusion",
    "25-reranker-bi-encoder-vs-cross-encoder",
    "26-rag-evaluation-system",
    "27-rag-complex-documents-and-multimodal",
    "28-long-context-vs-rag",
    "29-agent-rag-hallucination-detection-and-mitigation",
    "30-knowledge-conflict-versioning-and-updates",
    "31-function-calling-vs-tool-calling",
    "32-tool-result-compression-and-evidence-preservation",
    "33-async-long-running-tool-execution",
    "34-tool-discovery-routing-and-candidate-control",
    "35-parallel-tool-calling-consistency",
    "36-agent-memory-layering",
    "37-memory-write-read-update-forgetting",
    "38-long-conversation-short-term-memory",
    "39-multi-tenant-memory-isolation-and-consistency",
    "40-memory-cold-start",
    "41-multi-agent-topology-communication-state-routing",
    "42-multi-agent-error-amplification",
    "43-mcp-architecture-primitives-and-transports",
    "44-mcp-vs-function-calling-and-direct-api",
    "45-sse-vs-websocket-for-agent-frontend",
    "46-a2a-protocol-agent-card-task-message",
    "47-llm-gateway-design",
    "48-production-customer-service-agent-design",
    "49-model-capability-boundaries-and-routing",
    "50-coding-agent-product-comparison",
    "51-agent-framework-selection",
    "52-harness-engineering",
    "53-design-minimal-agent-runtime",
    "54-function-calling-end-to-end",
    "55-agent-state-and-message-protocol",
    "56-context-builder-and-token-budget",
    "57-stop-conditions-and-loop-detection",
    "58-checkpoint-pause-resume-idempotency",
    "59-async-long-running-tools",
    "60-parallel-tool-dependency-scheduler",
    "61-planner-executor-replanner",
    "62-human-in-the-loop-approval-state-machine",
    "63-agent-trace-replay-failure-attribution"
  ];

  const MASTERED_KEY = "agent-interview-mastered-v1";
  const LAST_KEY = "agent-interview-last-question-v1";

  const readSet = () => {
    try {
      const value = JSON.parse(localStorage.getItem(MASTERED_KEY) || "[]");
      return new Set(Array.isArray(value) ? value : []);
    } catch (_) {
      return new Set();
    }
  };

  const saveSet = (set) => {
    localStorage.setItem(MASTERED_KEY, JSON.stringify([...set]));
  };

  const rootUrl = () => {
    const logo = document.querySelector("a.md-header__button.md-logo");
    if (logo && logo.href) return new URL(logo.href);

    const marker = "/agent-interview/";
    const index = window.location.pathname.indexOf(marker);
    const path = index >= 0 ? window.location.pathname.slice(0, index + marker.length) : "/";
    return new URL(path, window.location.origin);
  };

  const questionUrl = (slug) => new URL(`${slug}/`, rootUrl()).href;

  const currentQuestion = () => {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return QUESTIONS.find((slug) => parts.includes(slug)) || null;
  };

  const questionNumber = (slug) => `Q${slug.slice(0, 2).padStart(3, "0")}`;

  const renderHomeProgress = () => {
    const container = document.querySelector("[data-learning-progress]");
    if (!container) return;

    const mastered = readSet();
    const count = QUESTIONS.filter((slug) => mastered.has(slug)).length;
    const percent = Math.round((count / QUESTIONS.length) * 100);

    container.innerHTML = `
      <div class="learning-progress__meta">
        <strong>学习进度 ${count} / ${QUESTIONS.length}</strong>
        <span>${percent}%</span>
      </div>
      <div class="learning-progress__bar" aria-label="学习进度 ${percent}%">
        <span style="width:${percent}%"></span>
      </div>
    `;

    const continueButton = document.querySelector("[data-continue-learning]");
    const lastQuestion = localStorage.getItem(LAST_KEY);
    if (continueButton) {
      continueButton.href = lastQuestion && QUESTIONS.includes(lastQuestion)
        ? questionUrl(lastQuestion)
        : questionUrl("09-agent-vs-model-and-components");
      continueButton.textContent = lastQuestion ? `继续学习 ${questionNumber(lastQuestion)}` : "从 Q009 开始";
    }

    const randomButton = document.querySelector("[data-random-question]");
    if (randomButton) {
      randomButton.onclick = () => {
        const unfinished = QUESTIONS.filter((slug) => !mastered.has(slug));
        const pool = unfinished.length ? unfinished : QUESTIONS;
        const slug = pool[Math.floor(Math.random() * pool.length)];
        window.location.href = questionUrl(slug);
      };
    }

    const resetButton = document.querySelector("[data-reset-progress]");
    if (resetButton) {
      resetButton.onclick = () => {
        if (!window.confirm("确定清空当前浏览器中的学习进度吗？")) return;
        localStorage.removeItem(MASTERED_KEY);
        renderHomeProgress();
      };
    }
  };

  const renderQuestionActions = () => {
    const slug = currentQuestion();
    if (!slug) return;

    localStorage.setItem(LAST_KEY, slug);

    const title = document.querySelector(".md-content h1");
    if (!title || document.querySelector(".question-actions")) return;

    const mastered = readSet();
    const actions = document.createElement("div");
    actions.className = "question-actions";

    const badge = document.createElement("span");
    badge.className = "question-badge";
    badge.textContent = questionNumber(slug);

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "question-action";

    const refreshToggle = () => {
      const done = mastered.has(slug);
      toggle.textContent = done ? "✓ 已掌握" : "标记为已掌握";
      toggle.classList.toggle("question-action--mastered", done);
    };

    toggle.onclick = () => {
      if (mastered.has(slug)) mastered.delete(slug);
      else mastered.add(slug);
      saveSet(mastered);
      refreshToggle();
    };

    refreshToggle();
    actions.append(badge, toggle);
    title.insertAdjacentElement("afterend", actions);
  };

  const initialize = () => {
    renderHomeProgress();
    renderQuestionActions();
  };

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initialize);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
