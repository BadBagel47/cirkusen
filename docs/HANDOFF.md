# Handoff

## Agentregler och inventering
- **Agentregler:** v1.5 (2026-11-14). Repot är skapat enligt reglerna från början.
- **Inventory: 2026-11-14** – Nytt, tomt repo. Bara `main`, inga PR, inga Issues, ingen tidigare dokumentation.
- **Projektspråk:** svenska (affischens text).
- **Publicering:** Cloudflare Workers, Worker `cirkusen`, static assets från `public/` enligt `wrangler.jsonc`. Adress: https://cirkusen.trythis.one/
- **Miljöns begränsningar (2026-11-14, molnsession):** push till `main` fungerar. Agenten kan inte se Cloudflare och inte heller nå `cirkusen.trythis.one` om adressen inte är tillåten i miljöns nätverk. Publiceringen behöver därför kontrolleras av ägaren.
- **Lagar och regler:** inga cookies, ingen lagring och inga tredjepartsanrop. Typsnitten är under OFL med licensfiler. Innehållet är politisk satir om partier och offentliga roller, och källorna står i sidfoten.

## Läget nu
- Sidan ligger i `public/` och är testad lokalt i dator- och mobilbredd, inga konsolfel.
- Affischen visar läget **14 november 2026**. Den är "färskvara" och blir inaktuell när regeringsfrågan avgörs.

## Nästa steg
1. Ägaren kopplar repot till Cloudflare (Workers & Pages → Import a repository) och lägger till den egna domänen `cirkusen.trythis.one`.
2. Ägaren kontrollerar att sidan syns på adressen.

## Engångsåtgärder
- **Väntar (2026-11-14):** koppla repot till Cloudflare Workers och lägg till den egna domänen.

## Beslut
- **2026-11-14:** Cloudflare Workers i stället för GitHub Pages, så att repot kan vara privat och bara `public/` publiceras (ägarens val).
- **2026-11-14:** Typsnitten ligger lokalt i stället för att hämtas från Google Fonts, så att inga besökaruppgifter skickas till tredje part.
- **2026-11-14:** Bara vyn "Karikatyraffischen" publiceras. Artefaktens andra vyer ("Regeringscirkusen 2026" och "Manegen – interaktiv") är inte med.

## Föreslagna körningar
_Inga just nu._

## Senaste ändringar
| Datum | Agent | Vad |
|---|---|---|
| 2026-11-14 | Claude | Repot skapat: affischen som fristående sida, Cloudflare-konfiguration och dokumentation. |
