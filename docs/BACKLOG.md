# Backlog

**Prioritet:** Hög · Medel · Låg
**ID:** gemensam nummerserie, `B-` bugg, `F-` funktion, `D-` planering/design.

## Öppna

### F-002 Affischarkiv: flera affischer på sidan
- **Prio:** Hög
- **Önskemål (ägaren 2026-11-14):** "Jag vill att man ska kunna skapa nya affischer och bläddra mellan dem."
- **Förslag:** Varje affisch får en egen adress med datum (t.ex. `/2026-11-14/`) och startsidan visar alltid den senaste. Det som är gemensamt (stil, typsnitt, pratbubblornas funktion) bryts ut, så att en ny affisch blir en ny fil plus en rad i en affischlista. En kort instruktion för hur en ny affisch görs läggs i `docs/`.
- **Bekräftat (ägaren 2026-11-14):** "Det är du och jag som bygger affischerna." Nya affischer görs alltså av ägaren och agenten tillsammans, inte av besökare i webbläsaren.
- **Lagar och regler:** ingen lagring i webbläsaren behövs (sidan minns inte vilken affisch besökaren såg senast), så läget är oförändrat.

### F-003 Bläddra mellan affischerna
- **Prio:** Hög
- **Önskemål (ägaren 2026-11-14):** se F-002.
- **Förslag:** Knappar för föregående och nästa affisch, som också går att nå med piltangenterna. Knapparna ska fungera i dator- och mobilbredd och inte skymma affischen eller textrutan på mobil. Bygger på F-002.

### F-004 Snabbval för att hoppa mellan affischerna
- **Prio:** Hög
- **Önskemål (ägaren 2026-11-14):** "Även ett snabbval för att hoppa mellan affischen behövs."
- **Förslag:** En meny som listar alla affischer med datum och rubrik, så att man kan hoppa direkt till en viss affisch utan att bläddra. Bygger på F-002.

## Parkerat
_(inget)_

## Klart

### F-001 Publicera karikatyraffischen som fristående sida ✅ 2026-11-14
- **Prio:** Hög
- **Gjort:** Artefaktvyn "Karikatyraffischen" är omgjord till vanlig HTML och JS, med lokala typsnitt, ikoner och delningsbild. På mobil visas texten i en ruta längst ner. Cloudflare-konfigurationen ligger i `wrangler.jsonc`. Publicerad och verifierad av ägaren 2026-11-14.
