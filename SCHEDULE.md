# Updating "Tonight" (the daily activities)

The **🌙 Tonight** button in the map reads `schedule.json` in this folder. Edit that file, check it, and push. The app picks up the change the next time it opens with signal. No rebuild is needed.

## Quick steps (for Hermes, from a photo of the daily sheet or hotel app)

1. Read the photo. Note each activity's **start time**, **end time** if given, **name**, and **place**.
2. Under `"days"`, find the date (format `2026-11-10`) and add one line per activity:
   ```json
   {"time": "11:00", "title": "Aqua gym", "venue": "aq-pool"},
   {"time": "21:30", "end": "22:30", "title": "Michael Jackson tribute", "venue": "c-15", "note": "Theme: white clothes"}
   ```
   - `time` / `end`: resort time, 24-hour. A time before 05:00, like `00:30`, counts as the **night before**, so put it under the evening's date.
   - `venue`: an id from the table below. If the place isn't in the table (e.g. "main pool" without saying which hotel), leave `venue` out and write `"where": "Main pool"`. The activity is listed without a map pin.
   - `note` (optional): price, theme, "18+", "not included", etc.
   - `short` (optional): a short label for the map, like `"Show"`.
3. **Daily regulars** are in `"every_day"` and show every day automatically. To change one for a single day, add a day item with the **same title** (e.g. `{"time": "21:30", "title": "Night show", "venue": "c-15", "note": "Tonight: Grease"}`). It replaces that day's regular. To drop one for a day: `{"title": "Bike tour", "cancelled": true}`.
4. Set `"updated"` to today's date, e.g. `"Nov 10"`.
5. Check: `python3 -I check_schedule.py`. It lists each day as the app will show it and stops with an error if a time or venue is wrong.
6. Publish from this folder:
   ```
   git add schedule.json && git commit -m "Schedule for Nov 10"
   git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin main
   ```
   (A plain `git push` fails on this Mac because the saved git login is a different GitHub account. The command above uses the `lmsnyri` login from the GitHub CLI.) The live page updates within a minute or two. Check it at https://lmsnyri.github.io/resort-map/schedule.json.

Only places in the purple (Aquamarine), yellow (Punta Cana) and green (Turquesa) sections and the common areas are allowed. Activities at other hotels (pink Legend, red Ambar, teal Esmeralda), such as the Oniria or Matum theaters, aren't included, so leave them out.

## Venue ids

| id | place |
|---|---|
| `aq-1` | Aquamarine Lobby / Front Desk |
| `aq-2` | Flamboyan Lobby Bar |
| `aq-3` | Acuario Buffet |
| `aq-4` | El Olivo Restaurant |
| `aq-5` | Aquamarine Shop |
| `aq-6` | Aquamarine Towel Center |
| `aq-7` | Relax Bar |
| `aq-8` | Lobby – Grand Aquamarine & Luxury Ambar |
| `aq-9` | Mashua Nikkei Restaurant |
| `aq-pool` | Aquamarine Pool |
| `aq-atm` | ATM (Aquamarine lobby) |
| `aq-ent` | Aquamarine Entertainment |
| `pc-1` | Punta Cana Lobby 1 / Front Desk |
| `pc-2` | Palma Lobby Bar |
| `pc-3` | Nacar Buffet |
| `pc-4a` | Punta Cana Shops |
| `pc-4b` | Punta Cana Shops (south) |
| `pc-5` | Tour Desk |
| `pc-6` | Punta Cana Lobby 2 |
| `pc-7` | Mai Tai Lobby Bar (Punta Cana) |
| `pc-8` | Bouganvillia Buffet |
| `pc-9` | Maiko Restaurant (Japanese) |
| `pc-10` | Nomad Restaurant |
| `pc-11` | Flame Restaurant |
| `pc-12` | Il Capriccio (Italian) |
| `pc-13` | Hibiscus Bar |
| `pc-14` | Flamboyan Bar |
| `pc-15` | Solecito Bar |
| `pc-16` | Guest Service |
| `pc-17` | Gym |
| `pc-18` | Punta Cana Towel Center |
| `pc-19a` | La Juana Bar (beach, north) |
| `pc-19b` | La Juana Bar (beach, south) |
| `pc-pool1` | Punta Cana Pool (Flamboyan) |
| `pc-pool2` | Punta Cana Pool (Hibiscus) |
| `pc-pool3` | Punta Cana Beach Pool |
| `pc-atm` | ATM (Punta Cana Lobby 2) |
| `pc-ent1` | Punta Cana Entertainment (theater side) |
| `pc-ent2` | Punta Cana Entertainment (pool) |
| `tq-1` | Turquesa Lobby |
| `tq-2` | Mai Tai Lobby Bar (Turquesa) |
| `tq-3` | Las Dalias Buffet |
| `tq-4` | Turquesa Minimarket |
| `tq-5` | Los Corales Pool Restaurant |
| `tq-6` | Tropical Bar |
| `tq-7` | Turquesa Jacuzzi |
| `tq-8` | Game Zone |
| `tq-9` | Takara (Asian fusion) |
| `tq-10` | Turquesa Towel Center |
| `tq-pool` | Turquesa Pool |
| `c-1` | Sports Area (tennis, football) |
| `c-2` | Water Park |
| `c-3` | Spa Kids |
| `c-4` | Minigolf |
| `c-5` | Spa |
| `c-7` | Convention Center |
| `c-8` | Medical Center & Pharmacy |
| `c-10` | Bahia Principe Village |
| `c-11` | Mini Market |
| `c-12` | Casino |
| `c-13` | Sports Bar & Karaoke |
| `c-15` | Tropicana Theater |
| `c-16` | Merengue Bar |
| `c-17` | Wedding Gazebo |
| `c-18` | La Isla (food truck, shop, kids club) |
| `c-19` | Beach House Las Olas |
| `lo-blue` | Blue Beach Restaurant (Las Olas) |
| `lo-tequila` | Tequila (Mexican, Las Olas) |
| `lo-greek` | The Greek (Las Olas) |
| `lo-thali` | Thali (Indian, Las Olas) |
| `lo-rodizio` | Rodizio (Las Olas) |
| `lo-fish` | Fish Market (Las Olas) |
| `c-20` | Privilege Beach Club |
| `c-21` | Wave Rider |
| `c-atm` | ATM (Village) |
| `beach-n` | Beach (north, by Las Olas) |
| `beach-m` | Beach (middle, by La Isla) |
| `beach-s` | Beach (south, by Solecito) |
