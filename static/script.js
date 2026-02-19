document.addEventListener("DOMContentLoaded", () => {
  const submitButton = document.getElementById("submitBtn");
  const userInputElement = document.getElementById("userInput");
  const resultsDiv = document.getElementById("results");
  const loadingSpinner = document.getElementById("loadingSpinner");
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.getElementById("primary-menu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!isExpanded));
      navMenu.classList.toggle("toggled-on");
    });
  }

  if (!submitButton || !userInputElement || !resultsDiv || !loadingSpinner) {
    return;
  }

  const renderMarkdown = (content) => {
    if (window.marked && typeof window.marked.parse === "function") {
      return window.marked.parse(content);
    }
    return content.replace(/\n/g, "<br>");
  };

  const showResult = (html, isError = false) => {
    resultsDiv.classList.remove("visible");
    resultsDiv.innerHTML = isError
      ? `<p style="color: var(--error-color); margin: 0;">${html}</p>`
      : html;
    requestAnimationFrame(() => {
      resultsDiv.style.display = "block";
      requestAnimationFrame(() => {
        resultsDiv.classList.add("visible");
      });
    });
  };

  const toggleLoading = (isLoading) => {
    loadingSpinner.style.display = isLoading ? "block" : "none";
    submitButton.disabled = isLoading;
  };

  const submitPrompt = async () => {
    const userInput = userInputElement.value.trim();
    if (!userInput) {
      showResult("Please enter some health context before submitting.", true);
      userInputElement.focus();
      return;
    }

    resultsDiv.style.display = "none";
    resultsDiv.innerHTML = "";
    resultsDiv.classList.remove("visible");
    toggleLoading(true);

    try {
      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userInput }),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || `HTTP ${response.status}`);
      }

      showResult(renderMarkdown(data.result || "No advice returned."));
    } catch (error) {
      showResult(`Request failed: ${error.message}`, true);
    } finally {
      toggleLoading(false);
    }
  };

  submitButton.addEventListener("click", submitPrompt);
  userInputElement.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      submitPrompt();
    }
  });
});
