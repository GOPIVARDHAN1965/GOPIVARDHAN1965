"""Generates terminal.svg — the animated header for the profile README.
Edit LINES, then run: python3 make_terminal.py
Uses SMIL animation (works inside GitHub's <img>); no JS, no external fonts."""
from html import escape

LINES = [  # (command, output, output style)
    ("whoami", "GopiVardhan Gunta", "name"),
    ("cat role.txt", "Data Engineer & AI Consultant · Tallahassee, FL", "out"),
    ("echo $LIGHT_MODE", "undefined (on purpose)", "dim"),
]
W, PAD, FS = 860, 32, 17          # width, padding, font size
CHAR = FS * 0.6                   # monospace advance width
TYPE, PAUSE = 0.06, 0.35          # seconds per char, pause after each output

rows, defs, y, t = [], [], 78, 0.4
for i, (cmd, out, style) in enumerate(LINES):
    # command: revealed char by char through a growing clip rect
    n = len(cmd) + 2
    widths = ";".join(str(round(k * CHAR, 1)) for k in range(n + 1))
    defs.append(
        f'<clipPath id="c{i}"><rect x="{PAD}" y="{y - FS}" height="{FS + 8}" width="0">'
        f'<animate attributeName="width" begin="{t:.2f}s" dur="{n * TYPE:.2f}s" values="{widths}" '
        f'calcMode="discrete" fill="freeze"/></rect></clipPath>'
    )
    rows.append(f'<text x="{PAD}" y="{y}" clip-path="url(#c{i})"><tspan class="p">$</tspan> {escape(cmd)}</text>')
    t += n * TYPE + 0.15
    oy = y + (40 if style == "name" else 26)
    rows.append(
        f'<text x="{PAD}" y="{oy}" class="{style}" opacity="0">{escape(out)}'
        f'<set attributeName="opacity" to="1" begin="{t:.2f}s"/></text>'
    )
    t += PAUSE
    y = oy + 38

# final prompt with blinking cursor
rows.append(
    f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s"/>'
    f'<text x="{PAD}" y="{y}" class="p">$</text>'
    f'<rect x="{PAD + 2 * CHAR}" y="{y - FS + 3}" width="{CHAR}" height="{FS}" fill="#39ff88">'
    f'<animate attributeName="opacity" values="1;0;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite" calcMode="discrete"/></rect></g>'
)
H = y + 30

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GopiVardhan Gunta — Data Engineer &amp; AI Consultant">
<style>
text {{ font: {FS}px "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace; fill: #efe9dd; white-space: pre; }}
.p {{ fill: #39ff88; }}
.name {{ font-size: 34px; font-weight: 800; letter-spacing: -1px; }}
.out {{ fill: #cfc8ba; }}
.dim {{ fill: #6a6358; }}
</style>
<defs>{"".join(defs)}</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#070606" stroke="#2a2622"/>
<circle cx="{PAD}" cy="26" r="6" fill="#2a2622"/><circle cx="{PAD + 20}" cy="26" r="6" fill="#2a2622"/><circle cx="{PAD + 40}" cy="26" r="6" fill="#2a2622"/>
<text x="{W - PAD}" y="31" text-anchor="end" class="dim" style="font-size:13px">~/gopivardhan_gunta</text>
{chr(10).join(rows)}
</svg>
'''
open("terminal.svg", "w").write(svg)
print(f"terminal.svg {W}x{H}, animation {t:.1f}s")
