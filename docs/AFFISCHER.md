# Affischarkivet

Varje affisch har en egen sida med datum i adressen, t.ex. `/2026-11-14/`. Startsidan `/` visar alltid den senaste. Bläddring och snabbval läser listan i `public/assets/posters.json`.

## Så gör vi en ny affisch
1. Skapa den som en kopia av den senaste:
   ```
   tools/posters.py new 2026-12-01 "Dag 79 efter valet"
   ```
   Första argumentet är datumet (`ÅÅÅÅ-MM-DD`, eller `ÅÅÅÅ-MM-DD-b` för en andra affisch samma dag). Andra är rubriken som visas i snabbvalet.
2. Redigera `public/<datum>/index.html` tillsammans: figurer, pratbubblor, stämpeln med datum och dag, sidfoten.
3. Byt metatexter i sidans `<head>` (`title`, `description`, `og:title`, `og:description`, `og:image:alt`) så att de stämmer med den nya affischen.
4. Gör en ny delningsbild (1200×630) och peka `og:image` på den. Ligger den kvar från förra affischen visar delningar av länken fel bild.
5. Kontrollera arkivet och publicera:
   ```
   tools/posters.py check
   ```
   `check` felar om startsidan inte är en kopia av den senaste affischen. Rätta med `tools/posters.py sync`.

## Viktigt att veta
- **`public/index.html` är genererad.** Redigera aldrig den för hand, utan affischen i sin datummapp och kör sedan `tools/posters.py sync`.
- Gamla affischer ändras inte. De är historik och ska visa läget den dagen.
- Gemensam stil och kod ligger i `public/assets/poster.css` och `poster.js`. Ändringar där gäller alla affischer.
- Sidan sparar ingenting i besökarens webbläsare, så den minns inte vilken affisch som sågs senast.

## Bläddring och snabbval
- Knapparna **Äldre** och **Nyare** och piltangenterna ← och → går en affisch bakåt eller framåt.
- Knappen i mitten öppnar en lista över alla affischer, nyast först. Listan går att styra med tangentbordet (pil upp/ned, Home, End, Esc).
