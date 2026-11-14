# Backlog

**Prioritet:** Hög · Medel · Låg
**ID:** gemensam nummerserie, `B-` bugg, `F-` funktion, `D-` planering/design.

## Öppna

### D-006 Mer utvecklad stil på figurerna (utkast)
- **Prio:** Medel · **Status:** Utkast, väntar på ägarens synpunkter
- **Önskemål (ägaren, 2026-11-14):** En ny version med mer utvecklad stil, i riktning mot klassisk tecknad film: mjuk skuggning, svarta konturer, vita handskar och blanka skor. Inga skyddade figurer får användas. Ingenting ska publiceras än.
- **Gjort:** `tools/restyle.py` ritar om en befintlig affisch. Alla figurer får volymskuggning, kraftigare konturer, glans på armar och ben, vita handskar, högre ögon med glans i pupillerna och blanka skor. Utkastet ligger i `drafts/2026-11-14-v2/index.html`. Provat lokalt i dator- och mobilbredd och med minskad rörelse, inga konsolfel.
- **Förhandsvisa:** kopiera `public/` till en tillfällig mapp, lägg utkastet som `2026-11-14/index.html` där och servera mappen.
- **Steg 2 (2026-11-14, ägaren valde "gå vidare med teckningen"):** Alla nio ansikten är omritade för hand i `tools/restyle.py`: större huvuden, stora ovala ögon med glans, runda näsor och tydliga miner (S skrattar, C förskräckt bakom glasögonen, V sur med mustasch, M livrädd med gnisslande tänder, L kämpar, KD blåser med uppblåst kind, SD slug, talmannen ropar, MP glad clown). Hattar och hår följer med de större huvudena, handskarna är större och enklare, och skorna större. V:s skylt "MINISTER" är flyttad upp ovanför huvudet. Provat lokalt i dator- och mobilbredd och med minskad rörelse, inga konsolfel.
- **Kvar:** Ägaren tycker till. Sedan bestäms om stilen ska ersätta affischen från 14 november, gälla först från nästa affisch, eller utvecklas vidare (t.ex. omritade ansikten och bakgrund i samma stil).

### F-005 Delningsbild som görs automatiskt för varje affisch
- **Prio:** Medel
- **Förslag:** Ett skript i `tools/` som ritar en delningsbild (1200×630) från affischen, så att varje ny affisch får rätt bild utan handarbete. Idag byts bilden för hand (se `docs/AFFISCHER.md`, punkt 4).

## Parkerat
_(inget)_

## Klart

### F-002 Affischarkiv: flera affischer på sidan ✅ 2026-11-14
- **Prio:** Hög
- **Önskemål (ägaren):** "Jag vill att man ska kunna skapa nya affischer och bläddra mellan dem." Ägaren bekräftade att affischerna byggs av ägaren och agenten tillsammans, inte av besökare.
- **Gjort:** Varje affisch har en egen adress med datum (första: `/2026-11-14/`) och startsidan visar den senaste. Gemensam stil och kod ligger i `assets/`. `tools/posters.py` skapar en ny affisch som kopia av den senaste och kontrollerar arkivet. Instruktion i `docs/AFFISCHER.md`. Provat lokalt i dator- och mobilbredd med en tillfällig kopia med tre affischer. Inte publicerat och verifierat av ägaren än.

### F-003 Bläddra mellan affischerna ✅ 2026-11-14
- **Prio:** Hög
- **Gjort:** Knapparna Äldre och Nyare samt piltangenterna ← och →. Knapparna är minst 44 px stora på mobil och fältet ligger fast överst när man scrollar, utan att skymma affischen eller textrutan. Avstängda i ändlägena. Provat lokalt.

### F-004 Snabbval för att hoppa mellan affischerna ✅ 2026-11-14
- **Prio:** Hög
- **Gjort:** Knappen i mitten öppnar en lista med alla affischer (datum och rubrik, nyast först, "Senaste" markerad). Går att styra med tangentbordet och stängs med Esc eller klick utanför. Provat lokalt.

### F-001 Publicera karikatyraffischen som fristående sida ✅ 2026-11-14
- **Prio:** Hög
- **Gjort:** Artefaktvyn "Karikatyraffischen" är omgjord till vanlig HTML och JS, med lokala typsnitt, ikoner och delningsbild. På mobil visas texten i en ruta längst ner. Cloudflare-konfigurationen ligger i `wrangler.jsonc`. Publicerad och verifierad av ägaren 2026-11-14.
