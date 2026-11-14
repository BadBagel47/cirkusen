(() => {
  const stage = document.getElementById("stage");
  const sheet = document.getElementById("sheet");
  let scale = 1;
  const fit = () => {
    scale = Math.min(1, document.documentElement.clientWidth / 1080);
    stage.style.transform = scale < 1 ? `scale(${scale})` : "";
    stage.style.marginBottom = `${1620 * (scale - 1)}px`;
    stage.style.marginRight = `${1080 * (scale - 1)}px`;
  };
  fit();
  addEventListener("resize", fit, { passive: true });

  const buttons = [...document.querySelectorAll("[data-act]")];
  const pops = [...document.querySelectorAll("[data-pop]")];
  // On small screens the scaled speech bubbles are too small to read, so the text is shown in a bottom sheet.
  const show = (id) => {
    const small = scale < 0.7;
    pops.forEach((p) => (p.hidden = small || p.dataset.pop !== id));
    const pop = pops.find((p) => p.dataset.pop === id);
    sheet.hidden = !(small && pop);
    if (small && pop) sheet.innerHTML = pop.innerHTML;
    buttons.forEach((b) => b.setAttribute("aria-expanded", String(b.dataset.act === id)));
  };
  buttons.forEach((b) => {
    b.addEventListener("click", () => show(b.dataset.act));
    b.addEventListener("mouseenter", () => show(b.dataset.act));
  });
  pops.forEach((p) => p.addEventListener("click", () => show(null)));
  sheet.addEventListener("click", () => show(null));
  addEventListener("keydown", (e) => { if (e.key === "Escape") show(null); });

  // ---- Poster navigation: previous, next and quick select ----
  // The list of posters lives in /assets/posters.json (oldest first). The newest poster is also served at "/".
  const nav = document.getElementById("nav");
  const current = document.body.dataset.poster;
  const fmt = new Intl.DateTimeFormat("sv-SE", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
  const make = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  };

  const build = (list) => {
    list.sort((a, b) => (a.slug < b.slug ? -1 : 1));
    const idx = list.findIndex((p) => p.slug === current);
    if (idx < 0) { nav.hidden = true; return; }
    const last = list.length - 1;
    const href = (i) => (i === last ? "/" : `/${list[i].slug}/`);
    const label = (p) => fmt.format(new Date(p.date));

    const step = (cls, text, arrow, aria, target, arrowFirst) => {
      const a = make("a", `nav-btn ${cls}`);
      a.setAttribute("aria-label", aria);
      const ar = make("span", "nav-arrow", arrow);
      ar.setAttribute("aria-hidden", "true");
      const tx = make("span", "nav-txt", text);
      a.append(...(arrowFirst ? [ar, tx] : [tx, ar]));
      if (target >= 0 && target <= last) a.href = href(target);
      else a.setAttribute("aria-disabled", "true");
      return a;
    };
    const prev = step("nav-prev", "Äldre", "‹", "Äldre affisch", idx - 1, true);
    const next = step("nav-next", "Nyare", "›", "Nyare affisch", idx + 1 > last ? -1 : idx + 1, false);

    const pick = make("button", "nav-btn nav-pick");
    pick.type = "button";
    pick.setAttribute("aria-expanded", "false");
    pick.setAttribute("aria-controls", "nav-menu");
    pick.setAttribute("aria-label", "Välj affisch");
    const here = list[idx];
    pick.append(
      make("span", "nav-cur", `${label(here)} · ${here.title}`),
      make("span", "nav-count", `${idx + 1}/${list.length} ▾`)
    );

    const menu = make("ul", "nav-menu");
    menu.id = "nav-menu";
    menu.hidden = true;
    for (let i = last; i >= 0; i--) {
      const li = make("li");
      const a = make("a");
      a.href = href(i);
      a.append(make("span", "nav-date", label(list[i])), make("span", "nav-title", list[i].title));
      if (i === last) a.append(make("span", "nav-tag", "Senaste"));
      if (i === idx) a.setAttribute("aria-current", "page");
      li.append(a);
      menu.append(li);
    }

    const inner = make("div", "nav-in");
    inner.append(prev, pick, next, menu);
    nav.replaceChildren(inner);

    const items = () => [...menu.querySelectorAll("a")];
    const close = (refocus) => {
      menu.hidden = true;
      pick.setAttribute("aria-expanded", "false");
      if (refocus) pick.focus();
    };
    const open = () => {
      menu.hidden = false;
      pick.setAttribute("aria-expanded", "true");
      (menu.querySelector("[aria-current]") || items()[0]).focus();
    };
    pick.addEventListener("click", () => (menu.hidden ? open() : close(false)));
    document.addEventListener("click", (e) => { if (!menu.hidden && !inner.contains(e.target)) close(false); });
    menu.addEventListener("keydown", (e) => {
      const all = items();
      const i = all.indexOf(document.activeElement);
      if (e.key === "ArrowDown") all[Math.min(i + 1, all.length - 1)].focus();
      else if (e.key === "ArrowUp") all[Math.max(i - 1, 0)].focus();
      else if (e.key === "Home") all[0].focus();
      else if (e.key === "End") all[all.length - 1].focus();
      else if (e.key === "Escape") { close(true); e.stopPropagation(); }
      else return;
      e.preventDefault();
    });
    pick.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !menu.hidden) { close(true); e.stopPropagation(); }
    });

    // Left and right arrow keys step between posters.
    addEventListener("keydown", (e) => {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey || !menu.hidden) return;
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      const target = e.key === "ArrowLeft" ? prev : e.key === "ArrowRight" ? next : null;
      if (target && target.href) location.href = target.href;
    });
  };

  fetch("/assets/posters.json")
    .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
    .then(build)
    .catch(() => { nav.hidden = true; });
})();
