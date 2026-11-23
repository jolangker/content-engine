/* Original recipient-side reconstructions. All coordinates use the 1080 × 1920 master. */
const Exhibits = (() => {
  const c = {
    desk: '#151A1C', slate: '#263034', bone: '#F3EFE4', paper: '#DED9C8',
    ink: '#1B2428', metal: '#A7B6B5', signal: '#FF725F', pen: '#B42D27'
  };
  const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;');
  function type(x, y, value, size, options = {}) {
    const { color = c.bone, weight = 600, mono = false, tracking = 0, anchor = 'start' } = options;
    return `<text x="${x}" y="${y}" font-family="${mono ? 'IBM Plex Mono' : 'Archivo'}" font-size="${size}"
      font-weight="${weight}" letter-spacing="${tracking}" text-anchor="${anchor}" fill="${color}">${escape(value)}</text>`;
  }
  function label(x, y, value, size = 30, color = c.metal) {
    return type(x, y, value, size, { mono: true, weight: 400, color });
  }
  // Whorls cut by a diagonal seam: the same small maker's mark on each case sheet.
  function seal(x, y, scale) {
    const ridges = Array.from({ length: 8 }, (_, i) => {
      const r = 7 + i * 4.3;
      return `<path d="M ${-r*.8} ${r*.69} C ${-r*1.33} ${r*.1} ${-r*.78} ${-r*1.2} ${r*.23} ${-r}
        C ${r*1.14} ${-r*.9} ${r*1.28} ${r*.45} ${r*.28} ${r*.95}"/> `;
    }).join('');
    return `<g transform="translate(${x} ${y}) scale(${scale}) rotate(-14)" fill="none" stroke="${c.signal}" stroke-linecap="round" stroke-width="2.4">${ridges}</g>`;
  }
  function defs() {
    return `<defs>
      <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" stroke="#3C4849" stroke-width="1.5" fill="none"/></pattern>
      <pattern id="fleck" width="11" height="9" patternUnits="userSpaceOnUse"><circle cx="1" cy="2" r=".8" fill="#68736F" opacity=".42"/></pattern>
      <linearGradient id="rim" x1="0" x2="1" y1="0" y2=".8"><stop stop-color="#778786"/><stop offset=".19" stop-color="#374244"/><stop offset=".51" stop-color="#626D6F"/><stop offset=".9" stop-color="#30393B"/></linearGradient>
      <clipPath id="well"><rect x="54" y="546" width="972" height="772"/></clipPath>
    </defs>`;
  }
  function base(pillar) {
    return `<rect width="1080" height="1920" fill="${c.desk}"/>
      ${seal(144,148,.85)} ${type(198,163,'Scam Autopsy',49,{weight:780,tracking:-2})}
      ${type(961,158,pillar,28,{mono:true,weight:400,color:c.metal,anchor:'end'})}
      <path d="M108 206H960" stroke="#607071" stroke-width="2"/>
      <rect x="54" y="450" width="972" height="609" fill="${c.slate}"/>
      <rect x="54" y="450" width="972" height="609" fill="url(#grid)"/>`;
  }
  function heading(tag, a, b) {
    return label(126,319,tag,30,c.signal) + type(120,421,a+' '+b,99,{weight:850,tracking:-5.4});
  }
  // Full reference sits on a separate paper slip. Its short dated credit stays beside the evidence.
  function source(section) {
    return `<g transform="translate(124 1061)"><rect width="457" height="55" fill="${c.slate}"/>
      ${label(16,38,'FTC · 14 APR 2025 · §' + section,31,c.bone)}</g>
      <g transform="translate(108 1370) rotate(-1.5 400 200)">
      ${slip(840,302)}
      ${label(32,58,'ADVISORY RECORD',33,c.ink)}
      <path d="M32 84H804" stroke="${c.ink}" stroke-width="2"/>
      ${type(31,162,'Top text scams of 2024',59,{weight:770,tracking:-2.2,color:c.ink})}
      ${label(34,232,'FTC  /  14 APRIL 2025  /  §' + section,33,c.ink)}</g>`;
  }
  function exhibit(content) {
    return `<g transform="translate(48 3) scale(.80)">${content}</g>`;
  }
  function plateTab(value) {
    return `<g transform="translate(102 579)"><rect width="444" height="51" fill="${c.paper}"/>
      ${label(16,36,value,29,c.ink)}</g>`;
  }
  function ring(path, color = c.pen) {
    return `<path data-part="ring" d="${path}" pathLength="1" fill="none" stroke="${color}" stroke-linecap="round" stroke-width="8"/>`;
  }
  function phone() {
    return `<g clip-path="url(#well)"><g data-part="device"><g transform="translate(125 640) rotate(-3 400 380)">
      <rect x="16" y="15" width="812" height="950" rx="72" fill="#101516"/>
      <rect width="812" height="950" rx="72" fill="url(#rim)"/>
      <rect x="10" y="10" width="792" height="930" rx="65" fill="#101617"/>
      <rect x="25" y="24" width="762" height="910" rx="53" fill="${c.slate}"/>
      <rect x="342" y="39" width="125" height="13" rx="6.5" fill="#121819"/>
      ${label(70,96,'UNSAVED NUMBER',27)}${type(65,155,'(202) 555-0146',53,{weight:650})}
      <path d="M25 194H787" stroke="#596766" stroke-width="2"/>
      <g data-part="incoming"><path d="M83 238H585Q613 238 613 268V334Q613 360 585 360H93L60 378V268Q60 238 83 238Z" fill="${c.bone}"/>
      ${type(87,317,'Nina, lunch today?',59,{color:c.ink,tracking:-1.8})}</g>
      <g data-part="reply"><path d="M354 393H731Q754 393 754 419V499L728 486H354Q326 486 326 459V420Q326 393 354 393Z" fill="#405050"/>
      ${type(352,454,'Wrong number.',52,{weight:600})}</g>
      <g data-part="follow"><path d="M85 530H684Q711 530 711 560V631Q711 658 685 658H94L60 676V559Q60 530 85 530Z" fill="${c.bone}"/>
      ${type(88,612,'Can we stay in touch?',57,{color:c.ink,tracking:-1.4})}
      ${ring('M272 550 C410 518 671 535 688 578 C710 626 510 655 358 643 C222 633 228 575 310 555 C372 540 443 540 477 542')}</g>
    </g></g></g>${plateTab('SMS / RECONSTRUCTION')}`;
  }
  function ticketPath(width,height) {
    let edge = '';
    for (let x=width; x>0; x-=28) edge += ` l-14 -12 l-14 12`;
    return `M0 0H${width}V${height}${edge}Z`;
  }
  function slip(w,h) {
    const d=ticketPath(w,h);
    return `<path d="${d}" fill="${c.paper}"/><path d="${d}" fill="url(#fleck)"/>`;
  }
  function diagram(kind = 'investment') {
    const job = kind === 'job';
    return `<g clip-path="url(#well)"><g data-part="transfer" transform="translate(154 665)">
      <path d="${ticketPath(756,467)}" transform="translate(14 18)" fill="#101617"/>
      ${slip(756,467)} ${label(40,62,'PAYMENT RECORD',32,c.ink)}
      <path d="M39 91H716" stroke="${c.ink}" stroke-width="3"/>
      ${label(44,148,'FROM',31,c.ink)}${type(42,215,'Your account',68,{color:c.ink,weight:710,tracking:-3})}
      <path d="M40 251H716" stroke="#69736D" stroke-width="2" stroke-dasharray="10 10"/>
      ${label(44,310,'SHOWN AS',31,c.ink)}${type(42,388,job?'Task deposit':'Investment',76,{color:c.ink,weight:790,tracking:-4})}
      <path data-part="route" d="M602 340H654Q673 340 673 361V544Q673 564 652 564H396" pathLength="1" fill="none" stroke="${c.signal}" stroke-width="10"/>
      <g data-part="recipient"><path d="M396 564l24 -18v36z" fill="${c.signal}"/>
      ${label(0,514,'ACTUAL RECIPIENT',29,c.metal)}${type(-4,590,'Scammer',82,{weight:820,tracking:-3,color:c.signal})}</g>
    </g></g>${plateTab('FUNDS / RECONSTRUCTION')}`;
  }
  function checkout() {
    return `<g clip-path="url(#well)"><g transform="translate(145 666) rotate(4 350 300)">
      <rect x="-15" y="14" width="765" height="570" fill="#101617"/>
      <rect width="762" height="568" fill="#3A4547"/>
      ${label(39,65,'MOCK EMAIL / PARCEL',32,c.bone)}
      <g transform="translate(25 100) rotate(-7 350 220)">${slip(728,495)}
      ${label(42,60,'LATCHMERE PARCEL • MOCK',30,c.ink)}<path d="M42 84H682" stroke="${c.ink}" stroke-width="3"/>
      ${type(38,178,'Redelivery',84,{weight:810,tracking:-5,color:c.ink})}
      ${type(41,260,'Fee due',52,{color:c.ink})}${type(668,261,'$1.50',73,{weight:800,anchor:'end',color:c.ink})}
      ${ring('M474 197 C553 164 691 180 705 233 C718 283 643 307 549 298 C451 287 445 234 483 209 C517 190 561 187 586 190')}
      <path d="M43 329H674" stroke="\#69736D" stroke-dasharray="7 9" stroke-width="2"/>
      ${label(42,397,'Illustrative charge',34,c.ink)}</g></g></g>${plateTab('FEE / RECONSTRUCTION')}`;
  }
  function caption(lines) {
    return lines.map((line,i)=>type(124,1168+i*59,line,53,{weight:600,tracking:-1.3})).join('');
  }
  function svg(body, id) {
    const markup = defs()+body;
    // A contact sheet mounts multiple plates in one document.
    const scoped = markup.replace(/id="(grid|fleck|rim|well)"/g, `id="${id}-$1"`)
      .replace(/url\(#(grid|fleck|rim|well)\)/g, `url(#${id}-$1)`);
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">${scoped}</svg>`;
  }
  return { c, base, heading, source, phone, diagram, checkout, caption, label, seal, svg, exhibit };
})();
