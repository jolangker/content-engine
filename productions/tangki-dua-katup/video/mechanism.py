"""Original shaded cistern illustration, shared by every view.

API: svg(view='tank', state=None, prefix='s01') -> str.
State keys: water (0..1 normal, up to 1.2 fault overflow), flapAngle (0..75),
leverAngle (normally 0..-16), floatY (absolute downward offset, default follows
water), exterior (0..1), lidY, fill, flush, refill, overflow (flow opacity).

Use svg's default `preserveAspectRatio='xMidYMid meet'`. The 900x1050 master
coordinates are unchanged in all macro viewBoxes. Animated IDs are PREFIX-
water, -water-body, -water-surface, -float, -lever, -flapper, -chain,
-tank-front, -lid, -fill-flow, -flush-flow, -refill-flow, -overflow-flow.

Fixed pivots: lever (155,300), flapper (650,795). `pose` returns transform,
chain d and water y values for deterministic GSAP attribute interpolation.
`chain_path` couples chain endpoints to lever/flapper rotation, preserving
an illustrative 490-unit length with a perpendicular quadratic bow. This
shows take-up/release without a stretching chain; it is not a catenary model.

Important topology: x270 fill riser; x645 overflow riser top y350; normal
water surface y410; outlet x568 y810; fill exits into tank at (300,425),
refill hose terminates ABOVE overflow lip at (645,323). The flush throat and
overflow share a downstream outlet but their inlet paths are distinct. The
overflow branch enters the outlet at y852, BELOW the closed seat (y805..828),
within the illustrated ceramic floor thickness; it does not cross the seal.
"""
from __future__ import annotations

import math


VIEWS = {
    'whole': '40 90 840 900',
    'tank': '70 125 800 830',
    'lever': '85 165 650 710',
    'flapper': '390 570 410 410',
    'float': '145 285 410 590',
    'fill': '145 260 410 650',
    'refill': '220 230 560 550',
    'overflow': '420 250 380 650',
}


def rotated(point, pivot, angle):
    rad = math.radians(angle)
    x, y = point[0] - pivot[0], point[1] - pivot[1]
    return (pivot[0] + x * math.cos(rad) - y * math.sin(rad),
            pivot[1] + x * math.sin(rad) + y * math.cos(rad))


def chain_path(leverAngle=0, flapAngle=0):
    a = rotated((535, 300), (155, 300), leverAngle)
    b = rotated((525, 778), (650, 795), flapAngle)
    chord = math.hypot(b[0] - a[0], b[1] - a[1])
    midpoint = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    perpendicular = (-(b[1] - a[1]) / max(chord, 1e-9),
                     (b[0] - a[0]) / max(chord, 1e-9))
    def length(bow):
        control = (midpoint[0] + perpendicular[0] * bow,
                   midpoint[1] + perpendicular[1] * bow)
        previous, total = a, 0
        for step in range(1, 21):
            t = step / 20
            point = ((1-t)**2*a[0] + 2*(1-t)*t*control[0] + t*t*b[0],
                     (1-t)**2*a[1] + 2*(1-t)*t*control[1] + t*t*b[1])
            total += math.hypot(point[0]-previous[0],point[1]-previous[1])
            previous = point
        return total
    lo, hi = 0., 980.
    if chord >= 490:
        hi = 0.  # An impossible pose stays straight; caller verifies distances.
    else:
        for _ in range(18):
            mid = (lo+hi)/2
            if length(mid) < 490:
                lo = mid
            else:
                hi = mid
    bow = (lo+hi)/2
    control = (midpoint[0] + perpendicular[0] * bow,
               midpoint[1] + perpendicular[1] * bow)
    return f'M {a[0]:.3f} {a[1]:.3f} Q {control[0]:.3f} {control[1]:.3f} {b[0]:.3f} {b[1]:.3f}'


def pose(water=1, flapAngle=0, leverAngle=0, floatY=None, **kwargs):
    dy = (1 - water) * 365
    fy = min(332, max(-45, dy)) if floatY is None else floatY
    return {
        'waterY': dy,
        'floatY': fy,
        'flapAngle': flapAngle,
        'leverAngle': leverAngle,
        'chainD': chain_path(leverAngle, flapAngle),
        'flapperTransform': f'rotate({flapAngle} 650 795)',
        'leverTransform': f'rotate({leverAngle} 155 300)',
        'floatTransform': f'translate(0 {fy})',
        'waterTransform': f'translate(0 {dy})',
    }


def svg(view='tank', state=None, prefix='s01'):
    st = {'water': 1, 'flapAngle': 0, 'leverAngle': 0, 'exterior': 0,
          'lidY': -58, 'fill': 0, 'flush': 0, 'refill': 0, 'overflow': 0}
    st.update(state or {})
    p = prefix
    q = pose(**st)
    viewbox = VIEWS.get(view, VIEWS['tank'])
    # No CSS filters: geometry and gradients supply all illustrated depth.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" class="mechanism" viewBox="{viewbox}" role="img" aria-label="Ilustrasi potongan tangki kloset tipe tuas dan flapper" preserveAspectRatio="xMidYMid meet">
<defs>
  <linearGradient id="{p}-ceramic" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".48" stop-color="#F8F9F5"/><stop offset="1" stop-color="#D0D8D5"/></linearGradient>
  <linearGradient id="{p}-side" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#D5DDDA"/><stop offset="1" stop-color="#AAB9BA"/></linearGradient>
  <linearGradient id="{p}-inside" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#D6E0DC"/><stop offset="1" stop-color="#F2F5EF"/></linearGradient>
  <linearGradient id="{p}-metal" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#647D8A"/><stop offset=".28" stop-color="#E2E8E9"/><stop offset=".5" stop-color="#A6B4BE"/><stop offset=".7" stop-color="#F4F6F4"/><stop offset="1" stop-color="#637C88"/></linearGradient>
  <linearGradient id="{p}-poly" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#EDF1EF"/><stop offset=".45" stop-color="#BBC9CC"/><stop offset="1" stop-color="#758D99"/></linearGradient>
  <linearGradient id="{p}-blue" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#7398E1"/><stop offset=".43" stop-color="#2459C4"/><stop offset="1" stop-color="#153A85"/></linearGradient>
  <linearGradient id="{p}-rubber" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#4E6B82"/><stop offset="1" stop-color="#172B3B"/></linearGradient>
  <linearGradient id="{p}-orange" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#E78558"/><stop offset=".6" stop-color="#C94422"/><stop offset="1" stop-color="#8A2B18"/></linearGradient>
  <linearGradient id="{p}-waterfill" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#71B9BF" stop-opacity=".48"/><stop offset="1" stop-color="#167580" stop-opacity=".22"/></linearGradient>
  <clipPath id="{p}-tank-clip"><path d="M174 248 L727 248 L704 786 Q703 814 675 814 L213 814 Q184 814 182 785 Z"/></clipPath>
  <clipPath id="{p}-overflow-clip"><path d="M628 350 L661 350 L661 784 L628 784 Z"/></clipPath>
</defs>

<!-- Ground shadow belongs to the illustration, not a flat diagram card. -->
<ellipse cx="469" cy="929" rx="307" ry="28" fill="#172B3B" opacity=".075"/>

<!-- Outlet continuation, visible below the cut tank floor. -->
<g id="{p}-outlet" stroke="#536775" stroke-width="3" stroke-linejoin="round">
 <path d="M530 804 L530 909 Q570 932 610 909 L610 804" fill="url(#{p}-poly)"/>
 <ellipse cx="570" cy="909" rx="40" ry="14" fill="#667F8A"/>
 <path d="M551 841 L551 906" stroke="#E8EFEC" stroke-width="7" opacity=".7"/>
</g>

<!-- Rear ceramic surface and true illustrated thickness. -->
<path d="M128 228 L194 187 L810 187 L766 227 L738 820 Q737 853 702 863 L190 863 Q153 860 151 823 Z" fill="url(#{p}-ceramic)" stroke="#617986" stroke-width="3"/>
<path d="M766 227 L810 187 L784 781 Q782 815 738 837 L738 820 Z" fill="url(#{p}-side)" stroke="#617986" stroke-width="3"/>
<path d="M161 242 L210 211 L777 211 L727 248 L704 786 Q703 814 675 814 L213 814 Q184 814 182 785 Z" fill="url(#{p}-inside)" stroke="#8EA2A6" stroke-width="2.5"/>
<path d="M161 242 L210 211 L777 211 L727 248 Z" fill="#F9FBF6" stroke="#8EA2A6" stroke-width="2"/>

<!-- Water is behind all functional parts. Translation shifts level while
the stationary tank clip masks its lower edge. normal level y410 < lip y350. -->
<g clip-path="url(#{p}-tank-clip)">
 <g id="{p}-water" transform="{q['waterTransform']}">
  <path id="{p}-water-body" d="M173 410 L731 410 L731 1250 L173 1250 Z" fill="url(#{p}-waterfill)"/>
  <ellipse id="{p}-water-surface" cx="452" cy="410" rx="281" ry="25" fill="#B1D5D2" fill-opacity=".72" stroke="#438F96" stroke-width="2.5"/>
  <path d="M196 414 Q452 445 711 414" fill="none" stroke="#F7FFFA" stroke-width="4" opacity=".65"/>
 </g>
</g>

<!-- Fixed supply and fill valve body: external functional illustration only. -->
<g id="{p}-fill-assembly" stroke="#536775" stroke-width="2.5" stroke-linejoin="round">
 <path d="M255 866 L255 923 Q255 938 235 938 L191 938" fill="none" stroke="#536775" stroke-width="22"/>
 <path d="M255 866 L255 923 Q255 938 235 938 L191 938" fill="none" stroke="#B7C4C9" stroke-width="15"/>
 <path d="M244 385 L244 837 Q269 850 294 837 L294 385" fill="url(#{p}-metal)"/>
 <ellipse cx="269" cy="837" rx="25" ry="9" fill="#8CA0A8"/>
 <path d="M252 420 L252 820" stroke="#F5F9F4" stroke-width="5" opacity=".75"/>
 <path d="M226 350 L226 386 Q270 407 315 386 L315 350" fill="url(#{p}-rubber)"/>
 <ellipse cx="270" cy="350" rx="45" ry="17" fill="#65808D"/>
 <ellipse cx="270" cy="346" rx="30" ry="10" fill="#273F50"/>
 <path d="M306 370 L330 378 L330 412 L303 414 Z" fill="url(#{p}-poly)"/>
 <ellipse cx="317" cy="414" rx="15" ry="6" fill="#536775"/>
 <!-- Float control link slides against its guide. -->
 <path d="M303 367 L337 380 L337 795" fill="none" stroke="#667F89" stroke-width="7"/>
 <path d="M303 367 L337 380" fill="none" stroke="#CBD7D7" stroke-width="3"/>
 <path d="M234 829 L304 829 L304 850 L234 850 Z" fill="url(#{p}-poly)"/>
 <ellipse cx="269" cy="830" rx="35" ry="11" fill="#CAD4D2"/>
</g>

<!-- Cup float retains volume and the central fixed riser remains visible. -->
<g id="{p}-float" transform="{q['floatTransform']}" stroke="#344F67" stroke-width="2.5">
 <g transform="translate(0 -48)">
 <path d="M211 448 L211 504 Q269 530 327 504 L327 448" fill="url(#{p}-blue)"/>
 <ellipse cx="269" cy="448" rx="58" ry="21" fill="#7196DA"/>
 <ellipse cx="269" cy="448" rx="27" ry="10" fill="#8DA5B1"/>
 <path d="M217 459 Q268 481 320 459" fill="none" stroke="#ACCAEE" stroke-width="4" opacity=".72"/>
 <path d="M222 479 L222 499" stroke="#91B1EC" stroke-width="6" opacity=".65"/>
 <path d="M323 454 L345 454 L345 470 L324 470" fill="#617FA2"/>
 </g>
</g>

<!-- Overflow is a fixed open-top tube, with a separate bottom branch. -->
<g id="{p}-overflow-tube" stroke="#536775" stroke-width="2.5" stroke-linejoin="round">
 <path d="M620 350 L620 790 Q620 814 602 823 L581 833 L581 860 L614 847 Q669 834 669 790 L669 350" fill="url(#{p}-poly)"/>
 <path d="M628 366 L628 786 Q628 804 611 813" fill="none" stroke="#EFF3EC" stroke-width="5" opacity=".75"/>
 <ellipse cx="645" cy="350" rx="25" ry="10" fill="#D2DDDB"/>
 <ellipse cx="645" cy="350" rx="17" ry="6" fill="#3E5A68"/>
 <path d="M620 749 L669 749" stroke="#8B9EA6" stroke-width="4"/>
</g>

<!-- Small refill hose ends above the overflow opening: air gap remains. -->
<g id="{p}-refill-hose" stroke-linecap="round" fill="none">
 <path d="M307 358 C361 267 477 273 543 292 C590 306 645 269 645 323" stroke="#172B3B" stroke-width="15"/>
 <path d="M307 358 C361 267 477 273 543 292 C590 306 645 269 645 323" stroke="#8A9EA8" stroke-width="9"/>
 <path d="M307 355 C361 264 477 270 543 289 C590 303 642 268 642 318" stroke="#D3DEDC" stroke-width="2.5"/>
 <path d="M667 344 L680 337 L680 308 L660 308" stroke="#7E959D" stroke-width="7"/>
</g>

<!-- Outlet seat, flapper hinge and buoyant cone share one assembly axis. -->
<g id="{p}-valve-seat" stroke="#536775" stroke-width="2.5">
 <path d="M487 805 L487 828 Q568 859 648 828 L648 805" fill="url(#{p}-poly)"/>
 <ellipse cx="568" cy="805" rx="81" ry="26" fill="#D3DFDA"/>
 <ellipse cx="568" cy="805" rx="58" ry="17" fill="#172B3B"/>
 <path d="M638 788 L638 772 L663 772 L663 795" fill="url(#{p}-poly)"/>
</g>
<g id="{p}-flapper" transform="{q['flapperTransform']}" stroke="#172B3B" stroke-width="2.5" stroke-linejoin="round">
 <path d="M505 795 L505 809 Q568 836 632 809 L632 795" fill="#173D67"/>
 <path d="M530 810 Q568 858 605 810" fill="url(#{p}-blue)"/>
 <ellipse cx="568" cy="795" rx="64" ry="22" fill="url(#{p}-blue)"/>
 <ellipse cx="568" cy="789" rx="47" ry="13" fill="#5780CF"/>
 <path d="M615 787 L650 787 L659 797 L621 805" fill="url(#{p}-blue)"/>
 <circle cx="650" cy="795" r="8" fill="url(#{p}-metal)"/>
 <path d="M519 787 L519 777 Q525 765 532 777 L532 786" fill="none" stroke="#658BD0" stroke-width="6"/>
</g>

<!-- Lever is one rigid rotating part. Chain endpoint helper follows it. -->
<g id="{p}-lever" transform="{q['leverTransform']}" stroke="#536775" stroke-width="2.5" stroke-linejoin="round">
 <path d="M153 293 L521 292 L538 300 L521 307 L153 307 Z" fill="url(#{p}-metal)"/>
 <path d="M168 296 L515 296" stroke="#F5F8F3" stroke-width="3"/>
 <circle cx="535" cy="300" r="7" fill="#DCE5E1"/>
 <path d="M153 291 L110 289 Q91 287 87 299 Q85 309 103 313 L151 313" fill="url(#{p}-orange)"/>
 <path d="M96 296 L143 299" stroke="#F4AF81" stroke-width="3"/>
</g>
<circle cx="155" cy="300" r="16" fill="url(#{p}-metal)" stroke="#536775" stroke-width="2.5"/>
<circle cx="155" cy="300" r="5" fill="#536775"/>
<path id="{p}-chain-shadow" d="{q['chainD']}" fill="none" stroke="#4C6371" stroke-width="6" stroke-linecap="round" opacity=".3"/>
<path id="{p}-chain" d="{q['chainD']}" fill="none" stroke="#607F8C" stroke-width="4.5" stroke-dasharray="4 6" stroke-linecap="round"/>

<!-- Flow marks are explanatory paths, not unsupported internal valve detail. -->
<g id="{p}-fill-flow" opacity="{st['fill']}" fill="none" stroke="#167580" stroke-width="13" stroke-linecap="round">
 <path class="flow-path" d="M317 422 L317 746" stroke-dasharray="13 20"/>
 <path d="M300 732 L317 753 L334 732" stroke-width="7"/>
 <path class="supply-path" d="M192 938 L232 938 Q255 938 255 918 L255 868" stroke-width="7" stroke-dasharray="8 12"/>
</g>
<g id="{p}-flush-flow" opacity="{st['flush']}" fill="none" stroke="#167580" stroke-linecap="round" stroke-linejoin="round">
 <path class="flow-path" d="M552 755 Q568 792 568 826 L568 905" stroke-width="19" stroke-dasharray="18 18"/>
 <path d="M548 890 L568 916 L588 890" stroke-width="8"/>
</g>
<g id="{p}-refill-flow" opacity="{st['refill']}" fill="none" stroke="#167580" stroke-linecap="round">
 <path class="hose-flow" d="M307 358 C361 267 477 273 543 292 C590 306 645 269 645 323" stroke-width="5" stroke-dasharray="8 14"/>
 <path class="flow-path" d="M645 327 L645 785 Q645 815 610 834 L570 852 L570 906" stroke-width="7" stroke-dasharray="10 16"/>
 <path d="M556 893 L570 910 L584 893" stroke-width="5"/>
</g>
<g id="{p}-overflow-flow" opacity="{st['overflow']}" fill="none" stroke="#167580" stroke-linecap="round">
 <path class="flow-path" d="M595 337 Q613 329 633 348 L645 374 L645 785 Q645 815 610 834 L570 852 L570 906" stroke-width="12" stroke-dasharray="12 18"/>
 <path d="M552 893 L570 914 L588 893" stroke-width="6"/>
</g>

<!-- Front slab can become opaque for the exterior view; section keeps ghost. -->
<g id="{p}-tank-front" opacity="{st['exterior']}">
 <path d="M128 228 L766 227 L738 820 Q737 853 702 863 L190 863 Q153 860 151 823 Z" fill="url(#{p}-ceramic)" stroke="#617986" stroke-width="3"/>
 <path d="M158 255 L180 804 Q181 835 209 840 L691 840" fill="none" stroke="#FFFFFF" stroke-width="8" opacity=".75"/>
 <ellipse cx="155" cy="300" rx="20" ry="18" fill="url(#{p}-metal)" stroke="#536775" stroke-width="3"/>
 <path d="M151 294 L108 292 Q91 289 87 300 Q85 310 103 314 L151 314" fill="url(#{p}-orange)" stroke="#536775" stroke-width="2.5"/>
</g>
<!-- Cut front edge makes the selective section tangible. -->
<path d="M128 228 L151 823 Q153 860 190 863 L702 863 Q737 853 738 820 L766 227" fill="none" stroke="#6B818B" stroke-width="4"/>
<path d="M151 252 L174 784 Q174 837 214 838 L684 838 Q714 837 716 800 L743 251" fill="none" stroke="#FFFFFF" stroke-width="5" opacity=".75"/>

<g id="{p}-lid" transform="translate(0 {st['lidY']})" stroke="#617986" stroke-width="2.5" stroke-linejoin="round">
 <path d="M118 220 L181 177 L816 177 L777 220 L777 238 L118 238 Z" fill="url(#{p}-ceramic)"/>
 <path d="M118 220 L777 220 L816 177 L816 195 L777 238 L777 220" fill="url(#{p}-side)"/>
 <path d="M137 215 L194 188 L789 188" fill="none" stroke="#FFFFFF" stroke-width="5"/>
</g>
</svg>'''


if __name__ == '__main__':
    from pathlib import Path
    Path(__file__).with_name('mechanism-preview.svg').write_text(svg(), encoding='utf-8')
