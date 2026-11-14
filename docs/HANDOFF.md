# Handoff

## Agentregler och inventering
- **Agentregler:** v1.7 (2026-11-14). Repot är skapat enligt reglerna från början.
- **Inventory: 2026-11-14** – Nytt, tomt repo. Bara `main`, inga PR, inga Issues, ingen tidigare dokumentation.
- **Projektspråk:** svenska (affischens text).
- **Publicering:** Cloudflare Workers, Worker `cirkusen`, static assets från `public/` enligt `wrangler.jsonc`. Adress: https://cirkusen.trythis.one/
- **Miljöns begränsningar (2026-11-14, molnsession):** push till `main` fungerar. Agenten kan inte se Cloudflare. Anrop till `*.trythis.one` från molnmiljön stoppas av Cloudflares säkerhetsskydd för zonen (403 "Attention Required"). Publiceringen behöver därför kontrolleras av ägaren.
- **Lagar och regler:** inga cookies, ingen lagring och inga tredjepartsanrop. Typsnitten är under OFL med licensfiler. Innehållet är politisk satir om partier och offentliga roller, och källorna står i sidfoten.

## Läget nu
- Sidan är publicerad på https://cirkusen.trythis.one/. Ägaren verifierade den 2026-11-14. Agenten har testat lokalt i dator- och mobilbredd utan konsolfel.
- Affischen visar läget **14 november 2026**. Den är "färskvara" och blir inaktuell när regeringsfrågan avgörs.

## Nästa steg
- Vänta på ägarens klartecken för körningen nedan (F-002, F-003, F-004). Ingen kod är ändrad än.
- Ägaren behöver bekräfta tolkningen i F-002: nya affischer görs av agenten på ägarens begäran, inte av besökare.
- Affischen behöver uppdateras när regeringsläget ändras.

## Engångsåtgärder
- **Klar (2026-11-14):** repot är kopplat till Cloudflare Workers med den egna domänen `cirkusen.trythis.one`. `workers.dev`-adresserna är avstängda.
- **Möjlig (ej föreslagen än):** en säkerhetsregel i Cloudflare som släpper igenom agentens kontroller, så att agenten kan verifiera publiceringen själv.

## Beslut
- **2026-11-14:** Cloudflare Workers i stället för GitHub Pages, så att repot kan vara privat och bara `public/` publiceras (ägarens val).
- **2026-11-14:** Typsnitten ligger lokalt i stället för att hämtas från Google Fonts, så att inga besökaruppgifter skickas till tredje part.
- **2026-11-14:** Bara vyn "Karikatyraffischen" publiceras. Artefaktens andra vyer ("Regeringscirkusen 2026" och "Manegen – interaktiv") är inte med.

## Föreslagna körningar
**A** – standardmodell, hög nivå – Flera affischer med bläddring och snabbval
- F-002 – Gör om sidan till ett arkiv där varje affisch har en egen adress och startsidan visar den senaste. Ger att nya affischer kan läggas till utan att de gamla försvinner.
- F-003 – Lägg till knappar (och piltangenter) för föregående och nästa affisch. Ger att man kan bläddra genom affischerna i tidsordning.
- F-004 – Lägg till en meny med alla affischer. Ger att man kan hoppa direkt till en viss affisch.

## Senaste ändringar
| Datum | Agent | Vad |
|---|---|---|
| 2026-11-14 | Claude | Nya önskemål inlagda i backloggen: affischarkiv, bläddring och snabbval (F-002, F-003, F-004). Agentreglerna uppdaterade till v1.7, inget i repot behövde ändras. |
| 2026-11-14 | Claude | Ägaren verifierade att sidan fungerar på cirkusen.trythis.one. |
| 2026-11-14 | Claude | Den egna domänen är tillagd. Agenten blockeras av Cloudflares skydd och kan inte verifiera innehållet. |
| 2026-11-14 | Claude | Ägaren kopplade Workern. Agentens kontroll av adressen misslyckades (svarade inte). |
| 2026-11-14 | Claude | Repot skapat: affischen som fristående sida, Cloudflare-konfiguration och dokumentation. |
