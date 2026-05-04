"""Planetary Explorer — Astronomy Lab
=====================================
Loads planet data from planets.json and displays an ASCII map of the solar
system. The user can choose between browsing worlds or other sky objects.

Run:
    python planets.py
"""

import json
import math
import os
import textwrap

AU_TO_LIGHT_YEARS = 1 / 63241.077
AU_TO_MILES = 92_955_807.3
SILLY_SPEED_MPH = 60
FIELD_LABEL_WIDTH = 22
NEIGHBOR_LABEL_WIDTH = 14
SKY_GRAPH_WIDTH = 30


# ── Load data ──────────────────────────────────────────────────────────────

def _load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return json.load(f)


def load_planets():
    return _load_json("planets.json")


def load_sky_objects():
    return _load_json("stars.json")


def _planets_by_name(planets):
    return {planet["name"].lower(): planet for planet in planets}


def _axis_position(distance_au, min_au, max_au, left, right):
    """Map a positive AU value onto a horizontal log-scale axis."""
    if max_au <= min_au:
        return left

    t = (math.log10(distance_au) - math.log10(min_au)) / (math.log10(max_au) - math.log10(min_au))
    t = max(0.0, min(1.0, t))
    return left + round(t * (right - left))


def _log_positions_for_items(items, distance_key, left, right):
    """Return x-coordinates for any objects that have positive AU distances."""
    distances = [item[distance_key] for item in items if item[distance_key] > 0]
    if not distances:
        return [left for _ in items]

    min_au = min(distances)
    max_au = max(distances)
    return [
        _axis_position(item[distance_key], min_au, max_au, left, right)
        for item in items
    ]


def _sky_distance_summary(obj, planets_by_name):
    """Return a baseline distance summary for a sky object.

    For deep-sky objects, astronomy references usually quote distance from Earth,
    and the Sun is close enough to Earth that both baselines are effectively the
    same at classroom scale. For Venus in the sky-object list, we use the rough
    Earth-distance stored in stars.json and the average Sun-distance from
    planets.json.
    """
    earth_ly = obj.get("distance_from_earth_ly", obj.get("distance_light_years"))
    sun_ly = obj.get("distance_from_sun_ly", earth_ly)
    if earth_ly is None:
        return None

    earth_au = earth_ly / AU_TO_LIGHT_YEARS
    sun_au = sun_ly / AU_TO_LIGHT_YEARS
    basis_note = obj.get("distance_baseline")

    if not basis_note and obj.get("object_type") == "planet":
        planet = planets_by_name.get(obj["name"].lower())
        if planet:
            sun_au = planet["distance_au"]
            sun_ly = sun_au * AU_TO_LIGHT_YEARS
        basis_note = (
            "Earth distance is a rough observing baseline for this date. "
            "Sun distance uses the world's average orbital distance."
        )

    if not basis_note:
        basis_note = (
            "Distances for stars, constellations, and asterisms are usually "
            "quoted from Earth. On this scale, the Sun is only 1 AU away from "
            "Earth, so both baselines are effectively the same."
        )

    return {
        "earth_au": earth_au,
        "earth_ly": earth_ly,
        "sun_au": sun_au,
        "sun_ly": sun_ly,
        "basis_note": basis_note,
    }


def _sky_distance_scale(sky_objects, planets_by_name):
    distances = []
    for obj in sky_objects:
        summary = _sky_distance_summary(obj, planets_by_name)
        if summary is None:
            continue
        distances.extend([summary["earth_au"], summary["sun_au"]])

    if not distances:
        return {"min_au": 1.0, "max_au": 1.0}

    return {"min_au": min(distances), "max_au": max(distances)}


def _fmt_au(au):
    if au >= 1_000_000:
        return f"{au / 1_000_000:.1f} million AU"
    if au >= 1_000:
        return f"{au:,.0f} AU"
    return f"{au:.3f} AU"


def _fmt_ly(ly):
    if ly >= 1:
        return f"{ly:g} ly"
    return f"{ly:.7f} ly"


def _fmt_distance_pair(au, ly):
    return f"~{_fmt_ly(ly)}  ({_fmt_au(au)})"


def _log_bar_position(distance_au, min_au, max_au):
    return _axis_position(distance_au, min_au, max_au, 0, SKY_GRAPH_WIDTH - 1)


def _make_log_bar(distance_au, min_au, max_au):
    chars = ["."] * SKY_GRAPH_WIDTH
    chars[_log_bar_position(distance_au, min_au, max_au)] = "*"
    return "[" + "".join(chars) + "]"


def _print_sky_distance_block(obj, planets_by_name, sky_scale):
    summary = _sky_distance_summary(obj, planets_by_name)
    if summary is None:
        _print_field("Distance:", "(varies / not one single distance)")
        return

    _print_field("Distance basis:", "Approx. from Earth")
    _print_field("From Earth:", _fmt_distance_pair(summary["earth_au"], summary["earth_ly"]))
    _print_field("From Sun:", _fmt_distance_pair(summary["sun_au"], summary["sun_ly"]))
    _print_field(
        "Log scale:",
        f"{_fmt_au(sky_scale['min_au'])} to {_fmt_au(sky_scale['max_au'])}",
    )
    print(f"  {'':<{FIELD_LABEL_WIDTH}} Earth {_make_log_bar(summary['earth_au'], sky_scale['min_au'], sky_scale['max_au'])}")
    print(f"  {'':<{FIELD_LABEL_WIDTH}} Sun   {_make_log_bar(summary['sun_au'], sky_scale['min_au'], sky_scale['max_au'])}")

    wrapped = textwrap.fill(
        summary["basis_note"],
        width=60,
        initial_indent=f"  {'Baseline note:':<{FIELD_LABEL_WIDTH}} ",
        subsequent_indent=f"  {'':<{FIELD_LABEL_WIDTH}} ",
    )
    print(wrapped)


def _observing_time_sort_key(local_time):
    if not local_time:
        return None

    text = local_time.strip().lower()
    if text == "any time after dark":
        return 20 * 60 + 30

    clock, meridiem = text.split()
    hour_text, minute_text = clock.split(":")
    hour = int(hour_text)
    minute = int(minute_text)

    if meridiem == "am":
        hour = 0 if hour == 12 else hour
        return (24 * 60) + (hour * 60) + minute

    hour = 12 if hour == 12 else hour + 12
    return (hour * 60) + minute


def _trip_visibility_rows(planets, sky_objects):
    rows = []
    seen_names = set()

    def maybe_add(name, sky_position, note):
        if not sky_position or not sky_position.get("local_time"):
            return

        key = name.lower()
        if key in seen_names:
            return

        seen_names.add(key)
        rows.append(
            {
                "name": name,
                "time": sky_position["local_time"],
                "sort_key": _observing_time_sort_key(sky_position["local_time"]),
                "direction": sky_position["compass"],
                "altitude": f"{sky_position['alt_deg']}°",
                "note": note or sky_position.get("note", ""),
            }
        )

    for planet in planets:
        maybe_add(planet["name"], planet.get("sky_position"), planet.get("sky_position", {}).get("note"))

    for obj in sky_objects:
        maybe_add(obj["name"], obj.get("sky_position"), obj.get("sky_position", {}).get("note"))

    rows.sort(key=lambda row: (row["sort_key"], row["name"]))
    return rows


def show_trip_visibility_table(planets, sky_objects):
    rows = _trip_visibility_rows(planets, sky_objects)
    bar = "─" * 76

    print(f"\n  {bar}")
    print(f"  {'VISIBLE OBJECTS FOR MAY 13 TRIPS':^76}")
    print(f"  {bar}")
    print(f"  {'Time':<20} {'Object':<14} {'Dir':<6} {'Alt':<5}")
    print(f"  {bar}")

    if not rows:
        print("  No objects in the current data set are marked visible for the trip.")
    else:
        item_rule = "  " + ("-" * 72)
        for index, row in enumerate(rows):
            print(f"  {row['time']:<20} {row['name']:<14} {row['direction']:<6} {row['altitude']:<5}")
            wrapped = textwrap.fill(
                row["note"],
                width=58,
                initial_indent="  Note: ",
                subsequent_indent="        ",
            )
            print(wrapped)
            if index < len(rows) - 1:
                print(item_rule)

    print(f"  {bar}\n")
    input("  Press Enter to return to the main menu...")


# ── ASCII solar-system map ─────────────────────────────────────────────────
#
# Layout (not to scale — distances are on a log scale so every planet fits):
#
#   number row  →  1    2   3      4                  5        6         7      8
#   symbol row  →  .    o   @      .                  O        O         0      0
#   orbit line  →  ☀────┴────┴───┴──────┴──────────────────┴───────┴──────────┴──►
#   name row    →  Mer  Ven Ear    Mar                Jup     Sat       Ura    Nep

MAP_WIDTH    = 76   # printable columns for the orbit line
SUN_X        = 2    # column for the ☀ symbol
PLANET_LEFT  = 6    # leftmost column a planet can occupy
PLANET_RIGHT = 72   # rightmost column a planet can occupy


def _log_positions(planets):
    """Return a list of x-coordinates for each planet, spaced on a log scale."""
    return _log_positions_for_items(planets, "distance_au", PLANET_LEFT, PLANET_RIGHT)


def draw_map(planets):
    positions = _log_positions(planets)

    num_row   = [" "] * (MAP_WIDTH + 2)
    sym_row   = [" "] * (MAP_WIDTH + 2)
    orbit_row = [" "] * (MAP_WIDTH + 2)
    name_row  = [" "] * (MAP_WIDTH + 2)

    # Build the orbit line
    orbit_row[SUN_X] = "☀"
    for x in range(SUN_X + 1, MAP_WIDTH + 1):
        orbit_row[x] = "─"
    orbit_row[MAP_WIDTH] = "►"

    # Place each planet on all four rows
    for p, x in zip(planets, positions):
        num_row[x]   = str(p["number"])
        sym_row[x]   = p["symbol"]
        orbit_row[x] = "┴"          # vertical connector from planet to orbit line
        abbr = p["name"][:3]
        for j, ch in enumerate(abbr):
            name_row[x + j] = ch

    bar = "─" * MAP_WIDTH
    print(f"\n  {bar}")
    print(f"  {'THE SOLAR SYSTEM + PLUTO  (log scale — not to scale)':^{MAP_WIDTH}}")
    print(f"  {bar}\n")
    print("  " + "".join(num_row[:MAP_WIDTH + 1]))
    print("  " + "".join(sym_row[:MAP_WIDTH + 1]))
    print("  " + "".join(orbit_row[:MAP_WIDTH + 1]))
    print("  " + "".join(name_row[:MAP_WIDTH + 1]))
    print()
    print("  Symbol key:  . = small rocky   @ = Earth   O = gas giant   0 = ice giant   * = dwarf planet")
    print(f"  {bar}")


# ── Planet detail view ─────────────────────────────────────────────────────

def _fmt_year(days):
    """Format an orbital period in days, adding Earth-years in parentheses."""
    years = days / 365.25
    return f"{days:,.0f} days  ({years:.2f} Earth years)"


def _neighbor_summary(planets, idx, step):
    neighbor_idx = idx + step
    if neighbor_idx < 0 or neighbor_idx >= len(planets):
        return None

    p = planets[idx]
    q = planets[neighbor_idx]
    delta_au = abs(q["distance_au"] - p["distance_au"])
    delta_ly = delta_au * AU_TO_LIGHT_YEARS
    travel_years = (delta_au * AU_TO_MILES) / SILLY_SPEED_MPH / 24 / 365.25

    return {
        "name": q["name"],
        "distance_au": delta_au,
        "distance_ly": delta_ly,
        "travel_years_60mph": travel_years,
    }


def _fmt_visibility(flag):
    return "Yes" if flag else "No"


def _print_field(label, value):
    print(f"  {label:<{FIELD_LABEL_WIDTH}} {value}")


def _print_sky_position(sp):
    """Print the Where to find it block from a sky_position dict."""
    print("  Where to find it (May 13, 2026, Goldendale WA)")
    if sp is None or sp.get("az_deg") is None:
        note = sp["note"] if sp else "No sky position data available."
        wrapped = textwrap.fill(
            note,
            width=60,
            initial_indent=f"  {'Note:':<{FIELD_LABEL_WIDTH}} ",
            subsequent_indent=f"  {'':<{FIELD_LABEL_WIDTH}} ",
        )
        print(wrapped)
    else:
        _print_field("Time:", sp["local_time"] + " PDT")
        _print_field("Direction:", f"{sp['compass']}  ({sp['az_deg']}° azimuth)")
        _print_field("Altitude:", f"~{sp['alt_deg']}° above the horizon")
        wrapped = textwrap.fill(
            sp["note"],
            width=60,
            initial_indent=f"  {'Note:':<{FIELD_LABEL_WIDTH}} ",
            subsequent_indent=f"  {'':<{FIELD_LABEL_WIDTH}} ",
        )
        print(wrapped)


def _print_neighbor_block(direction_label, neighbor, none_text):
    print(f"    {direction_label}:")
    if neighbor is None:
        print(f"      {'Object:':<{NEIGHBOR_LABEL_WIDTH}} {none_text}")
        return

    print(f"      {'Object:':<{NEIGHBOR_LABEL_WIDTH}} {neighbor['name']}")
    print(f"      {'Distance (AU):':<{NEIGHBOR_LABEL_WIDTH}} {neighbor['distance_au']:.3f}")
    print(f"      {'Distance (ly):':<{NEIGHBOR_LABEL_WIDTH}} {neighbor['distance_ly']:.7f}")
    print(
        f"      {'Time @ 60 mph:':<{NEIGHBOR_LABEL_WIDTH}} "
        f"~{neighbor['travel_years_60mph']:,.0f} years"
    )


def display_planet(p, planets, idx):
    bar = "─" * 52
    print(f"\n  {bar}")
    print(f"  {p['number']}. {p['name'].upper()}")
    print(f"  {bar}")
    _print_field("Type:", p['type'].title())

    # textwrap keeps long etymology strings readable in an 80-column terminal
    wrapped = textwrap.fill(
        p["etymology"],
        width=60,
        initial_indent=f"  {'Etymology:':<{FIELD_LABEL_WIDTH}} ",
        subsequent_indent=f"  {'':<{FIELD_LABEL_WIDTH}} ",
    )
    print(wrapped)

    _print_field("Distance:", f"{p['distance_au']:.3f} AU from the Sun")
    _print_field("Mass:", f"{p['mass_earth']} × Earth's mass")
    _print_field("Temperature:", f"{p['avg_temp_c']}°C  (average surface / cloud-top)")
    _print_field("Moons:", p['moons'])
    _print_field("Diameter:", f"{p['diameter_km']:,} km")
    _print_field("Year length:", _fmt_year(p['year_days']))
    _print_field("Naked eye:", _fmt_visibility(p['visible_naked_eye']))
    _print_field("Goldendale telescope:", _fmt_visibility(p['visible_goldendale_telescope']))

    inward = _neighbor_summary(planets, idx, -1)
    outward = _neighbor_summary(planets, idx, 1)

    print("  Nearest neighbors")
    _print_neighbor_block("Toward Sun", inward, "none (this is the innermost world)")
    _print_neighbor_block("Away From Sun", outward, "none (this is the outermost world)")
    print("    Note: values use average orbital distances (AU), not exact closest approach.")
    if "sky_position" in p:
        _print_sky_position(p["sky_position"])


    # ── STUDENT EXERCISE ──────────────────────────────────────────────────
    # Goal: add one new attribute to every planet in planets.json, then
    # display it here so it shows up when a user selects a planet.
    #
    # Step 1 — Open planets.json and add your new key/value to each planet.
    #          Example ideas:
    #            "gravity_earth"  — surface gravity as a multiple of Earth's
    #            "rotation_hours" — length of one day in hours
    #            "has_rings"      — true or false
    #            "atmosphere"     — dominant gas(es) in the atmosphere
    #
    # Step 2 — Add a print() line below that shows the new value.
    #          Follow the same format as the lines above.  Example:
    #
    #   print(f"  Gravity:      {p['gravity_earth']} × Earth's gravity")
    #
    # ──────────────────────────────────────────────────────────────────────

    print(f"  {bar}\n")


# ── Main loop ──────────────────────────────────────────────────────────────

def display_sky_object(obj, number, planets_by_name, sky_scale):
    bar = "─" * 52
    print(f"\n  {bar}")
    print(f"  {number}. {obj['name'].upper()}")
    print(f"  {bar}")
    _print_field("Object type:", obj["object_type"].title())

    if obj["constellation"]:
        _print_field("Constellation:", obj["constellation"])
    else:
        _print_field("Constellation:", "(none)")

    _print_sky_distance_block(obj, planets_by_name, sky_scale)

    _print_field("Naked eye:", _fmt_visibility(obj["visible_naked_eye"]))
    _print_field("Goldendale telescope:", _fmt_visibility(obj["visible_goldendale_telescope"]))

    wrapped = textwrap.fill(
        obj["notes"],
        width=60,
        initial_indent=f"  {'Notes:':<{FIELD_LABEL_WIDTH}} ",
        subsequent_indent=f"  {'':<{FIELD_LABEL_WIDTH}} ",
    )
    print(wrapped)
    if "sky_position" in obj:
        _print_sky_position(obj["sky_position"])
    print(f"  {bar}\n")


def browse_worlds(planets):
    planet_map = {str(p["number"]): idx for idx, p in enumerate(planets)}

    while True:
        draw_map(planets)
        choice = input("  Enter a world number (1–9), B to go back, or Q to quit: ").strip()

        if choice.lower() == "q":
            return "quit"
        if choice.lower() == "b":
            return "back"

        if choice in planet_map:
            idx = planet_map[choice]
            display_planet(planets[idx], planets, idx)
            input("  Press Enter to return to the map...")
        else:
            print(f"\n  '{choice}' is not a valid choice. Please enter 1–9, B, or Q.\n")


def draw_sky_object_list(sky_objects, planets_by_name, sky_scale):
    bar = "─" * 76
    print(f"\n  {bar}")
    print(f"  {'SKY OBJECTS  (stars, planets, constellations, asterisms)':^76}")
    print(f"  {bar}")
    for i, obj in enumerate(sky_objects, start=1):
        print(f"  {i:>2}. {obj['name']:<14}  [{obj['object_type']}]")
    print(f"  {bar}")


def browse_sky_objects(sky_objects, planets_by_name, sky_scale):
    while True:
        draw_sky_object_list(sky_objects, planets_by_name, sky_scale)
        choice = input("  Enter an object number, B to go back, or Q to quit: ").strip()

        if choice.lower() == "q":
            return "quit"
        if choice.lower() == "b":
            return "back"

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sky_objects):
                display_sky_object(sky_objects[idx], idx + 1, planets_by_name, sky_scale)
                input("  Press Enter to return to the list...")
                continue

        print(f"\n  '{choice}' is not a valid choice. Please enter 1–{len(sky_objects)}, B, or Q.\n")


def main():
    planets = load_planets()
    sky_objects = load_sky_objects()
    planets_by_name = _planets_by_name(planets)
    sky_scale = _sky_distance_scale(sky_objects, planets_by_name)
    menu_actions = {
        "1": lambda: browse_worlds(planets),
        "2": lambda: browse_sky_objects(sky_objects, planets_by_name, sky_scale),
        "3": lambda: show_trip_visibility_table(planets, sky_objects),
    }

    while True:
        bar = "─" * 76
        print(f"\n  {bar}")
        print(f"  {'ASTRONOMY EXPLORER':^76}")
        print(f"  {bar}")
        print("  Choose a category:")
        print("    1) Worlds (planets + dwarf planets in our solar system)")
        print("    2) Sky Objects (stars, planets, constellations, asterisms)")
        print("    3) Trip Visibility Table")
        print("    Q) Quit")
        print(f"  {bar}")

        choice = input("  Enter your choice: ").strip().lower()

        if choice == "q":
            print("\n  Thanks for exploring astronomy!\n")
            break

        action = menu_actions.get(choice)
        if action:
            result = action()
            if result == "quit":
                print("\n  Thanks for exploring astronomy!\n")
                break
            continue

        print("\n  Invalid choice. Please enter 1, 2, 3, or Q.\n")


if __name__ == "__main__":
    main()
