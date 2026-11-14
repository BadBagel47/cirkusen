# cirkusen – projektregler

> **Övergripande agentregler:** https://raw.githubusercontent.com/BadBagel47/agent-rules/main/AGENTS.md. Läs dem vid varje sessionsstart, de gäller före projektreglerna nedan.
> **Handoff:** `docs/HANDOFF.md` · **Backlog:** `docs/BACKLOG.md` · **Affischarkivet:** `docs/AFFISCHER.md`

## Vad projektet är
En satirisk, interaktiv karikatyraffisch om regeringsbildningen 2026: "Regeringscirkusen". Den publiceras på https://cirkusen.trythis.one/. Originalet är en Claude Design-artefakt med titeln "Regeringscirkusen 2026 – satirisk affisch", vyn "Karikatyraffischen". Den är omgjord till en fristående sida.

## Struktur
```
public/                 Det enda som publiceras (se wrangler.jsonc)
public/<datum>/index.html    En affisch per mapp, t.ex. 2026-11-14
public/index.html       Genererad kopia av den senaste affischen (redigeras inte för hand)
public/assets/poster.css, poster.js   Gemensam stil och kod: skalning, pratbubblor, bläddring, snabbval
public/assets/posters.json   Lista över alla affischer, äldst först
public/assets/fonts/    Bungee, Rye och Inter, lokalt med OFL-licenser
public/assets/og-image.jpg   Delningsbild 1200×630 (första affischen)
public/favicon.*, apple-touch-icon.png   Ikoner
tools/posters.py        Skapar nya affischer och kontrollerar arkivet, publiceras inte
tools/restyle.py        Utkastverktyg: ritar om en affisch i tecknad stil med skuggning (D-006), publiceras inte
drafts/                 Utkast som inte är publicerade. Ligger utanför public/ och syns inte på sajten
wrangler.jsonc          Cloudflare Workers-konfiguration (static assets)
AGENTS.md, docs/        Regler och dokumentation, publiceras inte
```

## Projektregler
- **Bara `public/` publiceras.** Lägg aldrig något annat där.
- **Inga externa resurser.** Typsnitt och bilder ligger lokalt, så att besökarnas IP-adresser inte skickas till tredje part.
- **Satiren ska träffa alla partier.** Inget parti skonas, och sakuppgifterna ska gå att belägga (källor står i affischens sidfot).
- Affischen är ritad i 1080×1620 px och skalas ner till skärmens bredd. På smala skärmar visas pratbubblornas text i en ruta längst ner, eftersom bubblorna annars blir oläsliga.
- Klart betyder: fungerar i dator- och mobilbredd, inga konsolfel, respekterar `prefers-reduced-motion`, och artisternas `aria-label` stämmer.
