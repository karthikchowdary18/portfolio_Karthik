const html = document.documentElement;
const body = document.body;
const langToggle = document.querySelector("#lang-toggle");
const featuredProjectsContainer = document.querySelector("#featured-projects");
const demoProjectList = document.querySelector("#demo-project-list");
const projectForm = document.querySelector("#project-form");
const projectSubmit = document.querySelector("#project-submit");
const projectReset = document.querySelector("#project-reset");
const projectStatus = document.querySelector("#project-status");
const scrollProgressBar = document.querySelector("#scroll-progress-bar");
const cursorGlow = document.querySelector("#cursor-glow");
const parallaxRoots = document.querySelectorAll("[data-parallax-root]");
const trafficScene = document.querySelector("[data-traffic-scene]");
const trafficButton = document.querySelector("[data-traffic-button]");
const trafficStatus = document.querySelector("[data-traffic-status]");
const trafficCountdown = document.querySelector("[data-traffic-countdown]");
const trafficActionRow = document.querySelector(".hero-drive-scene__action-row");

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const dictionaries = {};
const projectAccentClasses = [
    "project-card--cyan",
    "project-card--violet",
    "project-card--coral",
];

const state = {
    locale: localStorage.getItem("portfolio-locale") === "de" ? "de" : "en",
    projects: [],
    editingProjectId: null,
};

const trafficState = {
    phase: "idle",
    secondsRemaining: 10,
    arrivalTimer: null,
    pedestrianTimer: null,
    signalTimer: null,
    countdownTimer: null,
    resetTimer: null,
};

function lookup(dictionary, path) {
    return path.split(".").reduce((value, key) => value?.[key], dictionary);
}

async function loadDictionary(locale) {
    if (dictionaries[locale]) {
        return dictionaries[locale];
    }

    const response = await fetch(`/static/lang/${locale}.json?v=20260420-1`, {
        cache: "no-store",
    });

    if (!response.ok) {
        throw new Error(`Unable to load locale: ${locale}`);
    }

    const dictionary = await response.json();
    dictionaries[locale] = dictionary;
    return dictionary;
}

function t(key) {
    return lookup(dictionaries[state.locale], key) ?? key;
}

function tFormat(key, replacements = {}) {
    const value = t(key);

    if (typeof value !== "string") {
        return key;
    }

    return Object.entries(replacements).reduce(
        (text, [placeholder, replacement]) =>
            text.replaceAll(`{${placeholder}}`, String(replacement)),
        value
    );
}

function setStatus(message, type = "") {
    if (!projectStatus) {
        return;
    }

    projectStatus.textContent = message;
    projectStatus.classList.remove("is-error", "is-success");

    if (type) {
        projectStatus.classList.add(type);
    }
}

function createElement(tagName, className, textContent) {
    const element = document.createElement(tagName);

    if (className) {
        element.className = className;
    }

    if (typeof textContent === "string") {
        element.textContent = textContent;
    }

    return element;
}

function projectValue(project, keyBase) {
    return project[`${keyBase}_${state.locale}`];
}

function renderStaticTranslations() {
    document.querySelectorAll("[data-i18n]").forEach((node) => {
        const key = node.dataset.i18n;
        const attr = node.dataset.i18nAttr;
        const value = t(key);

        if (!attr && node.dataset.i18nEnFallback === undefined) {
            node.dataset.i18nEnFallback = node.textContent.trim().replace(/\s+/g, " ");
        }

        if (typeof value !== "string") {
            return;
        }

        if (state.locale === "en" && node.dataset.i18nPreserveEn === "true" && !attr) {
            node.textContent = node.dataset.i18nEnFallback ?? node.textContent;
            return;
        }

        if (attr) {
            node.setAttribute(attr, value);
            return;
        }

        node.textContent = value;
    });

    html.lang = state.locale;
    localStorage.setItem("portfolio-locale", state.locale);

    if (langToggle) {
        langToggle.textContent = state.locale === "en" ? "DE" : "EN";
        langToggle.setAttribute("aria-label", t("meta.toggle_language"));
    }

    document.title = t("meta.title");

    if (projectSubmit) {
        projectSubmit.textContent = state.editingProjectId
            ? t("api.form.submit_update")
            : t("api.form.submit_create");
    }

    updateTrafficSceneCopy();
}

function renderFeaturedProjects() {
    if (!featuredProjectsContainer) {
        return;
    }

    featuredProjectsContainer.replaceChildren();

    const featuredProjects = state.projects.filter((project) => project.featured);

    if (featuredProjects.length === 0) {
        const placeholder = createElement("article", "placeholder-card glass-card");
        placeholder.append(createElement("p", "", t("dynamic.projects.empty")));
        featuredProjectsContainer.append(placeholder);
        return;
    }

    featuredProjects.forEach((project, index) => {
        const card = createElement(
            "article",
            `project-card glass-card ${projectAccentClasses[index % projectAccentClasses.length]}`
        );
        const header = createElement("div", "project-card__header");
        const indexBadge = createElement(
            "span",
            "project-card__index",
            String(index + 1).padStart(2, "0")
        );

        const meta = createElement("div", "project-meta");
        meta.append(createElement("span", "meta-pill", project.category));
        meta.append(createElement("span", "meta-pill", project.timeframe));
        header.append(indexBadge, meta);

        const title = createElement("h3", "", projectValue(project, "title"));
        const summary = createElement("p", "", projectValue(project, "summary"));
        const impact = createElement("p", "project-impact");
        const impactLabel = createElement("span", "", t("dynamic.projects.impact_label"));
        impact.append(impactLabel);
        impact.append(document.createTextNode(projectValue(project, "impact")));

        const techList = createElement("ul", "tech-list");
        project.tech_stack.forEach((tech) => {
            techList.append(createElement("li", "", tech));
        });

        const links = createElement("div", "project-links");

        if (project.live_url) {
            const liveLink = createElement("a", "project-link", t("dynamic.projects.live_link"));
            liveLink.href = project.live_url;
            liveLink.target = "_blank";
            liveLink.rel = "noreferrer";
            links.append(liveLink);
        }

        if (project.repo_url) {
            const repoLink = createElement("a", "project-link", t("dynamic.projects.repo_link"));
            repoLink.href = project.repo_url;
            repoLink.target = "_blank";
            repoLink.rel = "noreferrer";
            links.append(repoLink);
        }

        card.append(header, title, summary, impact, techList);

        if (links.childNodes.length > 0) {
            card.append(links);
        }

        featuredProjectsContainer.append(card);
    });
}

function populateForm(project) {
    if (!projectForm) {
        return;
    }

    projectForm.title_en.value = project.title_en;
    projectForm.title_de.value = project.title_de;
    projectForm.summary_en.value = project.summary_en;
    projectForm.summary_de.value = project.summary_de;
    projectForm.impact_en.value = project.impact_en;
    projectForm.impact_de.value = project.impact_de;
    projectForm.tech_stack.value = project.tech_stack.join(", ");
    projectForm.timeframe.value = project.timeframe;
    projectForm.category.value = project.category;
    projectForm.live_url.value = project.live_url;
    projectForm.repo_url.value = project.repo_url;
    projectForm.featured.checked = project.featured;
    state.editingProjectId = project.id;
    renderStaticTranslations();
    setStatus(t("dynamic.api.editing"), "is-success");
}

function resetForm() {
    if (!projectForm) {
        return;
    }

    projectForm.reset();
    state.editingProjectId = null;
    renderStaticTranslations();
    setStatus("");
}

function renderProjectManager() {
    if (!demoProjectList) {
        return;
    }

    demoProjectList.replaceChildren();

    if (state.projects.length === 0) {
        const empty = createElement("div", "manager-card");
        empty.append(createElement("p", "", t("dynamic.api.empty")));
        demoProjectList.append(empty);
        return;
    }

    state.projects.forEach((project) => {
        const card = createElement("article", "manager-card");
        const header = createElement("div", "manager-card__header");
        const titleGroup = createElement("div");
        const title = createElement("h4", "manager-card__title", projectValue(project, "title"));
        const meta = createElement(
            "p",
            "project-meta",
            `${project.category} - ${project.timeframe}`
        );
        titleGroup.append(title, meta);

        const actions = createElement("div", "manager-actions");
        const editButton = createElement("button", "manager-button", t("dynamic.api.edit"));
        editButton.type = "button";
        editButton.addEventListener("click", () => populateForm(project));

        const deleteButton = createElement(
            "button",
            "manager-button manager-button--danger",
            t("dynamic.api.delete")
        );
        deleteButton.type = "button";
        deleteButton.addEventListener("click", async () => {
            await deleteProject(project.id);
        });

        actions.append(editButton, deleteButton);
        header.append(titleGroup, actions);

        const summary = createElement("p", "", projectValue(project, "summary"));
        const techList = createElement("ul", "tech-list");
        project.tech_stack.forEach((tech) => {
            techList.append(createElement("li", "", tech));
        });

        card.append(header, summary, techList);
        demoProjectList.append(card);
    });
}

async function fetchProjects() {
    const response = await fetch("/api/projects");

    if (!response.ok) {
        throw new Error("Unable to load projects.");
    }

    state.projects = await response.json();
    renderFeaturedProjects();
    renderProjectManager();
}

function collectPayload() {
    return {
        title_en: projectForm.title_en.value.trim(),
        title_de: projectForm.title_de.value.trim(),
        summary_en: projectForm.summary_en.value.trim(),
        summary_de: projectForm.summary_de.value.trim(),
        impact_en: projectForm.impact_en.value.trim(),
        impact_de: projectForm.impact_de.value.trim(),
        tech_stack: projectForm.tech_stack.value
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
        timeframe: projectForm.timeframe.value.trim(),
        category: projectForm.category.value.trim(),
        featured: projectForm.featured.checked,
        live_url: projectForm.live_url.value.trim(),
        repo_url: projectForm.repo_url.value.trim(),
    };
}

async function submitProject(event) {
    event.preventDefault();

    const payload = collectPayload();
    const isEditing = state.editingProjectId !== null;
    const endpoint = isEditing ? `/api/projects/${state.editingProjectId}` : "/api/projects";
    const method = isEditing ? "PUT" : "POST";

    try {
        setStatus(t("dynamic.api.saving"));

        const response = await fetch(endpoint, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error("Unable to save project.");
        }

        resetForm();
        await fetchProjects();
        setStatus(
            isEditing ? t("dynamic.api.updated") : t("dynamic.api.created"),
            "is-success"
        );
    } catch (error) {
        console.error(error);
        setStatus(t("dynamic.api.error"), "is-error");
    }
}

async function deleteProject(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("Unable to delete project.");
        }

        if (state.editingProjectId === projectId) {
            resetForm();
        }

        await fetchProjects();
        setStatus(t("dynamic.api.deleted"), "is-success");
    } catch (error) {
        console.error(error);
        setStatus(t("dynamic.api.error"), "is-error");
    }
}

function setupRevealAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                }
            });
        },
        {
            threshold: 0.16,
        }
    );

    document.querySelectorAll(".reveal").forEach((node) => observer.observe(node));
}

function updateScrollState() {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollableHeight > 0 ? window.scrollY / scrollableHeight : 0;

    if (scrollProgressBar) {
        scrollProgressBar.style.transform = `scaleX(${progress})`;
    }

    body.classList.toggle("is-scrolled", window.scrollY > 18);
}

function setupCursorGlow() {
    if (!cursorGlow || prefersReducedMotion) {
        return;
    }

    const updateCursorGlow = (event) => {
        body.classList.add("has-pointer");
        cursorGlow.style.transform = `translate3d(${event.clientX - 150}px, ${event.clientY - 150}px, 0)`;
    };

    window.addEventListener("pointermove", updateCursorGlow, { passive: true });
}

function setupHeroParallax() {
    if (prefersReducedMotion) {
        return;
    }

    parallaxRoots.forEach((root) => {
        root.style.setProperty("--pointer-x", "0.5");
        root.style.setProperty("--pointer-y", "0.5");

        root.addEventListener("pointermove", (event) => {
            const rect = root.getBoundingClientRect();
            const pointerX = (event.clientX - rect.left) / rect.width;
            const pointerY = (event.clientY - rect.top) / rect.height;

            root.style.setProperty("--pointer-x", pointerX.toFixed(3));
            root.style.setProperty("--pointer-y", pointerY.toFixed(3));
        });

        root.addEventListener("pointerleave", () => {
            root.style.setProperty("--pointer-x", "0.5");
            root.style.setProperty("--pointer-y", "0.5");
        });
    });
}

function clearTrafficTimers() {
    window.clearTimeout(trafficState.arrivalTimer);
    window.clearTimeout(trafficState.pedestrianTimer);
    window.clearTimeout(trafficState.signalTimer);
    window.clearTimeout(trafficState.resetTimer);
    window.clearInterval(trafficState.countdownTimer);
    trafficState.arrivalTimer = null;
    trafficState.pedestrianTimer = null;
    trafficState.signalTimer = null;
    trafficState.resetTimer = null;
    trafficState.countdownTimer = null;
}

function updateTrafficSceneCopy() {
    if (!trafficButton || !trafficStatus || !trafficCountdown) {
        return;
    }

    trafficButton.textContent = t("hero.signal_button");

    const statusKeyByPhase = {
        idle: "hero.pedestrian_status_approaching",
        pedestrian_approaching: "hero.pedestrian_status_approaching",
        pedestrian_waiting: "hero.pedestrian_status_waiting",
        signal_approaching: "hero.signal_status_approaching",
        waiting: "hero.signal_status_waiting",
        green: "hero.signal_status_green",
        auto: "hero.signal_status_auto",
    };

    const isWaiting = trafficState.phase === "waiting";

    trafficStatus.textContent = t(statusKeyByPhase[trafficState.phase] ?? "hero.signal_status_approaching");
    trafficCountdown.textContent = isWaiting
        ? tFormat("hero.signal_countdown", { seconds: trafficState.secondsRemaining })
        : "";

    if (trafficActionRow) {
        trafficActionRow.hidden = !isWaiting;
    }
}

function setTrafficPhase(phase) {
    trafficState.phase = phase;

    if (trafficButton) {
        trafficButton.disabled = phase !== "waiting";
    }

    updateTrafficSceneCopy();
}

function makeTrafficGreen(source = "user") {
    if (!trafficScene || trafficState.phase !== "waiting") {
        return;
    }

    window.clearInterval(trafficState.countdownTimer);
    trafficState.countdownTimer = null;
    window.clearTimeout(trafficState.arrivalTimer);
    trafficState.arrivalTimer = null;
    window.clearTimeout(trafficState.signalTimer);
    trafficState.signalTimer = null;

    trafficScene.classList.remove("is-awaiting-input");
    trafficScene.classList.add("is-green");
    setTrafficPhase(source === "auto" ? "auto" : "green");

    trafficState.resetTimer = window.setTimeout(() => {
        startTrafficSceneCycle();
    }, prefersReducedMotion ? 3600 : 7600);
}

function startTrafficCountdown() {
    trafficState.secondsRemaining = 10;
    updateTrafficSceneCopy();

    trafficState.countdownTimer = window.setInterval(() => {
        trafficState.secondsRemaining -= 1;

        if (trafficState.secondsRemaining <= 0) {
            trafficState.secondsRemaining = 0;
            updateTrafficSceneCopy();
            makeTrafficGreen("auto");
            return;
        }

        updateTrafficSceneCopy();
    }, 1000);
}

function startTrafficSceneCycle() {
    if (!trafficScene) {
        return;
    }

    clearTrafficTimers();
    trafficState.secondsRemaining = 10;
    trafficScene.classList.add("is-resetting");
    trafficScene.classList.remove(
        "is-green",
        "is-awaiting-input",
        "is-entering",
        "is-heading-pedestrian",
        "is-pedestrian-active",
        "is-heading-signal"
    );

    // Restart the entrance transition cleanly each cycle.
    void trafficScene.offsetWidth;

    setTrafficPhase("pedestrian_approaching");

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            trafficScene.classList.remove("is-resetting");
            trafficScene.classList.add("is-heading-pedestrian");
        });
    });

    trafficState.arrivalTimer = window.setTimeout(() => {
        trafficScene.classList.add("is-pedestrian-active");
        setTrafficPhase("pedestrian_waiting");

        trafficState.pedestrianTimer = window.setTimeout(() => {
            trafficScene.classList.remove("is-pedestrian-active", "is-heading-pedestrian");
            trafficScene.classList.add("is-heading-signal");
            setTrafficPhase("signal_approaching");

            trafficState.signalTimer = window.setTimeout(() => {
                trafficScene.classList.add("is-awaiting-input");
                setTrafficPhase("waiting");
                startTrafficCountdown();
            }, prefersReducedMotion ? 1400 : 2900);
        }, prefersReducedMotion ? 1700 : 3300);
    }, prefersReducedMotion ? 1000 : 2600);
}

function setupTrafficScene() {
    if (!trafficScene || !trafficButton) {
        return;
    }

    trafficButton.addEventListener("click", () => {
        makeTrafficGreen("user");
    });

    startTrafficSceneCycle();
}

function setupMotionSystem() {
    updateScrollState();
    window.addEventListener("scroll", updateScrollState, { passive: true });
    window.addEventListener("resize", updateScrollState, { passive: true });
    setupCursorGlow();
    setupHeroParallax();
    setupTrafficScene();
}

async function applyLocale(locale) {
    state.locale = locale;
    await loadDictionary(locale);
    renderStaticTranslations();
    renderFeaturedProjects();
    renderProjectManager();
}

langToggle?.addEventListener("click", async () => {
    const nextLocale = state.locale === "en" ? "de" : "en";
    await applyLocale(nextLocale);
});

projectForm?.addEventListener("submit", submitProject);
projectReset?.addEventListener("click", resetForm);

Promise.all([loadDictionary("en"), loadDictionary("de")])
    .then(async () => {
        renderStaticTranslations();
        setupRevealAnimations();
        setupMotionSystem();
        await fetchProjects();
    })
    .then(async () => {
        if (state.locale !== "en") {
            await applyLocale(state.locale);
        }

        requestAnimationFrame(() => {
            body.classList.add("is-ready");
        });
    })
    .catch((error) => {
        console.error(error);
        setStatus(t("dynamic.api.error"), "is-error");
    });
