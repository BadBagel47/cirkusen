# Handoff

## Agentregler och inventering
- **Agentregler:** v1.9 (2026-11-15). Repot är skapat enligt reglerna från början.
- **Inventory: 2026-11-14** – Nytt, tomt repo. Bara `main`, inga PR, inga Issues, ingen tidigare dokumentation.
- **Projektspråk:** svenska (affischens text).
- **Publicering:** Cloudflare Workers, Worker `cirkusen`, static assets från `public/` enligt `wrangler.jsonc`. Adress: https://cirkusen.trythis.one/
- **Miljöns begränsningar (2026-11-14, molnsession):** push till `main` fungerar. Agenten kan inte se Cloudflare. Anrop till `*.trythis.one` från molnmiljön stoppas av Cloudflares säkerhetsskydd för zonen (403 "Attention Required"). Publiceringen behöver därför kontrolleras av ägaren.
- **Lagar och regler:** inga cookies, ingen lagring och inga tredjepartsanrop. Typsnitten är under OFL med licensfiler. Innehållet är politisk satir om partier och offentliga roller, och källorna står i sidfoten.

## Läget nu
- Sidan är publicerad på https://cirkusen.trythis.one/. Ägaren verifierade den 2026-11-14. Agenten har testat lokalt i dator- och mobilbredd utan konsolfel.
- Senaste affischen visar läget **16 november 2026** (dag 64 efter valet, F-006) och finns på `/` och `/2026-11-16/`. Den från 14 november ligger kvar på `/2026-11-14/`. Affischerna är "färskvara" och blir inaktuella när regeringsfrågan avgörs.
- **Dagens affisch bygger på webbsökning, inte på läsning av artiklarna:** agenten kunde inte öppna nyhetssajterna (se Engångsåtgärder). Ägaren bör kolla detaljerna.
- Sidan är nu ett **affischarkiv** (F-002, F-003, F-004): varje affisch har en egen adress med datum, `/` visar den senaste, och det finns Äldre/Nyare-knappar, piltangenter och en snabbvalslista. Så görs en ny affisch: se [docs/AFFISCHER.md](AFFISCHER.md). Varje affisch får en egen delningsbild som ritas av `tools/posters.py image` (F-005). Tills det finns två affischer är bläddringsknapparna avstängda och listan har bara en rad.
- Kodändringen är provad lokalt (dator- och mobilbredd, tangentbord, minskad rörelse, inga konsolfel). **Inte verifierad på den publicerade adressen** eftersom agenten stoppas av Cloudflares skydd, och inte provad på ägarens telefon.

## Nästa steg
- **D-006 (ny stil, utkast):** ägaren bedömer utkastet med genererade figurer i `drafts/2026-11-14-v3/` (byggs med `tools/compose_v3.py`). Ingenting av det är publicerat.
- Ägaren kollar affischen från 16 november (fakta och publicering). Nästa affisch görs när läget ändras, t.ex. efter talmannens besked efter 17 november (se AFFISCHER.md).
- Affischen behöver uppdateras när regeringsläget ändras.

## Engångsåtgärder
- **Klar (2026-11-14):** repot är kopplat till Cloudflare Workers med den egna domänen `cirkusen.trythis.one`. `workers.dev`-adresserna är avstängda.
- **Möjlig (ej föreslagen än):** en säkerhetsregel i Cloudflare som släpper igenom agentens kontroller, så att agenten kan verifiera publiceringen själv.

- **Gjort 2026-11-16 (ägarens miljö "Default", personlig):** `www.svt.se`, `svt.se`, `www.sverigesradio.se`, `www.tv4.se` och `www.riksdagen.se` är tillagda i molnmiljöns tillåtna adresser så att agenten kan läsa nyheterna. **Ändå misslyckades hämtningen** av sidorna (namnet gick inte att slå upp), så agenten fick lita på webbsökning. Ofullständigt löst: kontrollera om miljön behöver startas om eller om hämtningsverktyget har en egen lista.

## Beslut
- **2026-11-14:** Cloudflare Workers i stället för GitHub Pages, så att repot kan vara privat och bara `public/` publiceras (ägarens val).
- **2026-11-14:** Typsnitten ligger lokalt i stället för att hämtas från Google Fonts, så att inga besökaruppgifter skickas till tredje part.
- **2026-11-14:** Nya affischer byggs av ägaren och agenten tillsammans. Besökare ska inte kunna skapa egna affischer på sidan (F-002).
- **2026-11-14:** Bara vyn "Karikatyraffischen" publiceras. Artefaktens andra vyer ("Regeringscirkusen 2026" och "Manegen – interaktiv") är inte med.

## Föreslagna körningar
_Inga just nu._

## Senaste ändringar
| Datum | Agent | Vad |
|---|---|---|
| 2026-11-16 | Claude | Dagens affisch (16 november, dag 64): C valde S:s paket, Kristersson rapporterar 17 november (F-006). Provad lokalt. |
| 2026-11-15 | Claude | Delningsbild som ritas automatiskt för varje affisch (F-005), provad lokalt. Agentreglerna v1.9, inget i repot behövde ändras. |
| 2026-11-14 | Claude | D-006 steg 7: M spegelvänd och figurerna jämnare placerade i utkastet. Inte publicerat. |
| 2026-11-14 | Claude | D-006 steg 6: alla figurer genererade och inlagda i utkastet, med skyltar och skuggor som kod. Inte publicerat. |
| 2026-11-14 | Claude | D-006 steg 5: test med genererad figur (S) inlagd i ett eget utkast. Inte publicerat. |
