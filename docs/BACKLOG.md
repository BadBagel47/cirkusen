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
- **Steg 3 (2026-11-14, ägaren: "jag vill se det över hela affischen"):** Scenen runt figurerna är omritad i samma stil: tältet har ett varmt ljus i mitten och mörknar mot kanterna, publiken är skuggade huvuden med ögon som tittar mot manegen, manegens kant och golv har skuggning och ljus, skylten med rubriken har fått djup, blanka lampor och kraftigare kontur, och vimplarna, bandet och datumstämpeln följer med. Provat lokalt i dator- och mobilbredd och med minskad rörelse, inga konsolfel.
- **Steg 4 (2026-11-14, ägaren: figurerna utgick fortfarande från streckgubbar och behövde ritas om helt):** Alla nio figurer är nu ritade från grunden i `tools/restyle.py` (funktionerna `fig_*`): päronformade kroppar, tjocka gummislangsarmar och -ben, stora vita handskar, stora runda skor och ännu större huvuden. Rekvisita och skyltar från originalet återanvänds. V:s skylt och MP:s skylt är flyttade så att de syns. Känt: MP:s skylt skymmer talmannens megafon, och talmannens hatt skymmer delvis L. Provat lokalt i dator- och mobilbredd och med minskad rörelse, inga konsolfel.
- **Steg 5 (2026-11-14):** Ägaren: inga figurer känns rätt jämfört med referensbilden. Slutsats: figurer ritade som kod blir geometriska och når inte den målade stilen. Ägaren godkände ett test med bildgenerator (ElevenLabs, modell gpt-image-2.5, cirka 760 krediter för fyra varianter). Testfiguren S (domptör) finns i `drafts/2026-11-14-v3-test/` som utskuren bild (`s.webp`, 865×700 px) inlagd i affischen, med skyltarna STÖDPARTI och INFLYTANDE som kod ovanpå. Figuren går att trycka på och pratbubblan fungerar. Varianterna syns i `drafts/preview/test-genererad-varianter.jpg`. Känt i testet: moroten och skylten INFLYTANDE krockar med C och V:s skylt, och bilden har för låg upplösning för skarp visning på högupplösta skärmar (nästa gång: begär högre upplösning och stående format).
- **Miljö:** `elevenlabsusercontent.com` är tillåten i molnmiljön sedan 2026-11-14, så att genererade bilder kan laddas ned.
- **Steg 6 (2026-11-14, ägaren: "Kör"):** Alla figurer, kanonen och stolen är genererade i samma stil (S som stilreferens) och frilagda. Utkastet ligger i `drafts/2026-11-14-v3/` (bilder i `img/`, cirka 1,2 MB totalt) och byggs av `tools/compose_v3.py`, som lägger skyltar, partibokstäver och markskuggor ovanpå som kod. Kanonen står nu på en träställning i stället för att hänga i luften. Kostnad totalt cirka 6 000 krediter (test 760, tio bilder 4 900, friläggning 300). Provat lokalt: alla elva går att trycka på i dator- och mobilbredd, inga konsolfel.
- **Steg 7 (2026-11-14, ägarens önskemål):** M är spegelvänd och tittar nu in mot manegen. Figurerna är omplacerade så att avstånden är jämnare: V och S har mer luft, stolen står mellan V och SD, L, T och MP krockar inte längre, och den tomma ytan nere till vänster är fylld. Skuggorna följer nu figurerna automatiskt i `tools/compose_v3.py`. Den gamla dekorationen "z z z" vid M är borttagen i utkastet. Flytt, storlek och spegling kostar inga krediter.
- **Känt i utkastet:** smårörelserna inuti figurerna finns inte kvar (hela figurer gungar och studsar fortfarande). Bilderna är cirka 2 gånger visningsstorleken, utom S som är cirka 1,5. Det kodritade utkastet ligger kvar i `drafts/2026-11-14-v2/` och används som bakgrund.
- **Kvar:** Ägaren bedömer utkastet. Sedan bestäms om det ska ersätta affischen från 14 november eller gälla från nästa affisch, och vid publicering flyttas bilderna till `public/<datum>/img/`.

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
