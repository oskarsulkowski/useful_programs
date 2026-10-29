"""Generate the projectile-motion figures using only the Python standard library.

Run from this directory with: python3 generuj_wykresy.py
"""

from html import escape
from math import cos, hypot, pi, radians, sin
from pathlib import Path


OUT = Path(__file__).parent / "wykresy"
OUT.mkdir(exist_ok=True)

V0 = 36.0
ANGLE_DEG = 40.0
G = 9.81
MASS = 0.145
AIR_DENSITY = 1.225
DRAG_COEFFICIENT = 0.47
DIAMETER = 0.073
AREA = pi * (DIAMETER / 2) ** 2
DT = 0.002
COLORS = ("#2463a6", "#d47722", "#168578", "#8455a4")


def ideal_state(time):
    angle = radians(ANGLE_DEG)
    vx0 = V0 * cos(angle)
    vy0 = V0 * sin(angle)
    return (
        vx0 * time,
        vy0 * time - 0.5 * G * time**2,
        vx0,
        vy0 - G * time,
    )


def derivative(state):
    _, _, vx, vy = state
    speed = hypot(vx, vy)
    drag_factor = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * AREA * speed / MASS
    return vx, vy, -drag_factor * vx, -G - drag_factor * vy


def add_scaled(state, slope, factor):
    return tuple(value + factor * change for value, change in zip(state, slope))


def rk4_step(state, step):
    k1 = derivative(state)
    k2 = derivative(add_scaled(state, k1, step / 2))
    k3 = derivative(add_scaled(state, k2, step / 2))
    k4 = derivative(add_scaled(state, k3, step))
    return tuple(
        value + step * (a + 2 * b + 2 * c + d) / 6
        for value, a, b, c, d in zip(state, k1, k2, k3, k4)
    )


def simulate_drag():
    time = 0.0
    angle = radians(ANGLE_DEG)
    state = (0.0, 0.0, V0 * cos(angle), V0 * sin(angle))
    samples = [(time, state)]
    while time < 30:
        next_state = rk4_step(state, DT)
        next_time = time + DT
        if next_state[1] < 0:
            fraction = state[1] / (state[1] - next_state[1])
            landing_state = tuple(
                start + fraction * (end - start)
                for start, end in zip(state, next_state)
            )
            samples.append((time + fraction * DT, landing_state))
            return samples
        time, state = next_time, next_state
        samples.append((time, state))
    raise RuntimeError("The drag simulation did not reach the ground.")


def make_chart(filename, title, x_label, y_label, series, x_limits, y_limits):
    width, height = 900, 520
    left, top, right, bottom = 90, 75, 35, 75
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_min, x_max = x_limits
    y_min, y_max = y_limits

    def sx(value):
        return left + (value - x_min) / (x_max - x_min) * plot_width

    def sy(value):
        return top + (y_max - value) / (y_max - y_min) * plot_height

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="DejaVu Sans, Arial, sans-serif" fill="#233044">',
        f'<text x="{left}" y="38" font-size="21" font-weight="bold">{escape(title)}</text>',
    ]

    for index in range(6):
        x_value = x_min + (x_max - x_min) * index / 5
        y_value = y_min + (y_max - y_min) * index / 5
        x_pos, y_pos = sx(x_value), sy(y_value)
        svg.extend(
            [
                f'<line x1="{x_pos:.2f}" y1="{top}" x2="{x_pos:.2f}" '
                f'y2="{top + plot_height}" stroke="#dce3eb"/>',
                f'<line x1="{left}" y1="{y_pos:.2f}" x2="{left + plot_width}" '
                f'y2="{y_pos:.2f}" stroke="#dce3eb"/>',
                f'<text x="{x_pos:.2f}" y="{top + plot_height + 24}" '
                f'text-anchor="middle" font-size="12">{x_value:.3g}</text>',
                f'<text x="{left - 12}" y="{y_pos + 4:.2f}" text-anchor="end" '
                f'font-size="12">{y_value:.3g}</text>',
            ]
        )

    svg.extend(
        [
            f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" '
            f'y2="{top + plot_height}" stroke="#233044" stroke-width="1.5"/>',
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" '
            'stroke="#233044" stroke-width="1.5"/>',
            f'<text x="{left + plot_width / 2}" y="{height - 18}" '
            f'text-anchor="middle" font-size="15">{escape(x_label)}</text>',
            f'<text x="23" y="{top + plot_height / 2}" text-anchor="middle" '
            f'font-size="15" transform="rotate(-90 23 {top + plot_height / 2})">'
            f'{escape(y_label)}</text>',
            f'<defs><clipPath id="plot"><rect x="{left}" y="{top}" '
            f'width="{plot_width}" height="{plot_height}"/></clipPath></defs>',
            '<g clip-path="url(#plot)" fill="none" stroke-width="2.8" '
            'stroke-linejoin="round" stroke-linecap="round">',
        ]
    )

    for label, points, color in series:
        coordinates = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in points)
        svg.append(
            f'<polyline points="{coordinates}" stroke="{color}" '
            f'aria-label="{escape(label)}"/>'
        )
    svg.append("</g>")

    legend_x = left + 14
    for index, (label, _, color) in enumerate(series):
        x_pos = legend_x + index * 205
        svg.extend(
            [
                f'<line x1="{x_pos}" y1="58" x2="{x_pos + 24}" y2="58" '
                f'stroke="{color}" stroke-width="3"/>',
                f'<text x="{x_pos + 31}" y="62" font-size="12">{escape(label)}</text>',
            ]
        )
    svg.extend(["</g>", "</svg>"])
    (OUT / filename).write_text("\n".join(svg), encoding="utf-8")


def mechanical_energy(state):
    _, y, vx, vy = state
    return 0.5 * MASS * (vx**2 + vy**2) + MASS * G * y


def main():
    drag = simulate_drag()
    drag_times = [item[0] for item in drag]
    drag_states = [item[1] for item in drag]
    ideal_flight = 2 * V0 * sin(radians(ANGLE_DEG)) / G
    ideal_range = V0**2 * sin(2 * radians(ANGLE_DEG)) / G
    ideal_height = (V0 * sin(radians(ANGLE_DEG))) ** 2 / (2 * G)
    apex_index = max(range(len(drag)), key=lambda index: drag[index][1][1])
    drag_flight, drag_landing = drag[-1]
    drag_height = drag[apex_index][1][1]
    drag_apex_time = drag[apex_index][0]
    ideal_times = [ideal_flight * index / 1000 for index in range(1001)]
    ideal_states = [ideal_state(time) for time in ideal_times]

    make_chart(
        "tor_ruchu.svg",
        "Tor ruchu: model idealny i opór aerodynamiczny",
        "Położenie poziome x [m]",
        "Wysokość y [m]",
        [
            ("Bez oporu", [(s[0], s[1]) for s in ideal_states], COLORS[0]),
            ("Z oporem", [(s[0], s[1]) for s in drag_states], COLORS[1]),
        ],
        (0, ideal_range * 1.05),
        (0, ideal_height * 1.12),
    )
    make_chart(
        "wysokosc_czas.svg",
        "Wysokość w funkcji czasu",
        "Czas t [s]",
        "Wysokość y [m]",
        [
            ("Bez oporu", [(t, s[1]) for t, s in zip(ideal_times, ideal_states)], COLORS[0]),
            ("Z oporem", [(t, s[1]) for t, s in drag], COLORS[1]),
        ],
        (0, ideal_flight * 1.03),
        (0, ideal_height * 1.12),
    )
    make_chart(
        "polozenie_poziome.svg",
        "Położenie poziome w funkcji czasu",
        "Czas t [s]",
        "Położenie x [m]",
        [
            ("Bez oporu", [(t, s[0]) for t, s in zip(ideal_times, ideal_states)], COLORS[0]),
            ("Z oporem", [(t, s[0]) for t, s in drag], COLORS[1]),
        ],
        (0, ideal_flight * 1.03),
        (0, ideal_range * 1.05),
    )
    make_chart(
        "predkosci.svg",
        "Składowe prędkości w modelu z oporem",
        "Czas t [s]",
        "Prędkość [m/s]",
        [
            ("vx", [(t, s[2]) for t, s in drag], COLORS[0]),
            ("vy", [(t, s[3]) for t, s in drag], COLORS[2]),
        ],
        (0, drag_flight),
        (min(-V0 * 0.22, 1.1 * min(s[3] for s in drag_states)), V0 * 0.8),
    )
    ideal_energy = 0.5 * MASS * V0**2
    make_chart(
        "energia.svg",
        "Energia mechaniczna: zachowanie i rozpraszanie",
        "Czas t [s]",
        "Energia [J]",
        [
            ("Bez oporu", [(t, ideal_energy) for t in ideal_times], COLORS[0]),
            (
                "Z oporem",
                [(t, mechanical_energy(s)) for t, s in drag],
                COLORS[1],
            ),
        ],
        (0, ideal_flight * 1.03),
        (0, ideal_energy * 1.08),
    )

    print(f"v0 = {V0:.2f} m/s; alpha = {ANGLE_DEG:.2f} deg; g = {G:.2f} m/s^2")
    print(f"Bez oporu: czas lotu = {ideal_flight:.3f} s")
    print(f"Bez oporu: zasięg = {ideal_range:.3f} m; wysokość maks. = {ideal_height:.3f} m")
    print(
        f"Z oporem: czas lotu = {drag_flight:.3f} s; zasięg = {drag_landing[0]:.3f} m"
    )
    print(
        f"Z oporem: wysokość maks. = {drag_height:.3f} m "
        f"po {drag_apex_time:.3f} s"
    )
    print(f"Wykresy zapisano w: {OUT}")


if __name__ == "__main__":
    main()
