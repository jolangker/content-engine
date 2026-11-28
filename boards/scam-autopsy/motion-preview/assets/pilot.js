// Seekable at every frame, including backwards in the HyperFrames editor.
const e = Exhibits;
const group = (id, contents) => `<g id="${id}">${contents}</g>`;
const stage = e.base('MESSAGE SCAMS') +
  group('threadTitle', e.heading('THE BAIT','Wrong','number?')) +
  group('hookTitle', e.heading('THE HOOK MOMENT','Wrong','number?')) +
  group('moneyTitle', e.heading('WHERE THE MONEY LEAVES','Who gets','paid?')) +
  group('tellTitle', e.heading('THE ONE TELL','Still','talking?')) +
  e.exhibit(group('thread', e.phone()) + group('money', e.diagram())) +
  e.source(5) + e.label(582,1098,'AI voice',31);
document.getElementById('case').innerHTML = e.svg(stage, 'pilot');

// Clause starts follow the forced alignment of the full take (rounded to frames).
const lines = [
  [0.20, ['Wrong number?']], [1.50, ['Watch the next text.']],
  [3.13, ["They know you're not Nina,"]], [4.60, ['but they still want to talk.']],
  [6.63, ['Later, the stranger','suggests an investment.']],
  [9.63, ['Money sent to','the fake platform']],
  [11.23, ['goes to the scammer.']], [12.73, ['You can leave the','text unanswered.']]
];
const captionArt = lines.map(([,line],i) => group('caption'+i,e.caption(line))).join('');
document.getElementById('captions').innerHTML = e.svg(captionArt, 'captions');
const el = id => document.getElementById(id);
const part = name => document.querySelector('[data-part="'+name+'"]');
function progress(t, start, duration) { return Math.max(0, Math.min(1,(t-start)/duration)); }
function appear(node, yes) { node.style.visibility = yes ? 'visible' : 'hidden'; }
function ink(node, fraction) {
  node.style.strokeDasharray = '1 1';
  node.style.strokeDashoffset = String(1 - fraction);
}
function renderAt(t) {
  const moneyIn = 6.57, tellIn = 12.60;
  const transfer = t >= moneyIn && t < tellIn;
  const ending = t >= tellIn;
  appear(el('threadTitle'), t < 4.42);
  appear(el('hookTitle'), t >= 4.42 && t < moneyIn);
  appear(el('moneyTitle'), transfer);
  appear(el('tellTitle'), ending);
  appear(el('thread'), !transfer);
  appear(el('money'), transfer);

  const settle = (1-progress(t,0,.78))**3;
  const lift = progress(t,6.26,.31)**2;
  const returnSettle = (1-progress(t,tellIn,.45))**3;
  part('device').setAttribute('transform', ending
    ? `translate(0 ${40*returnSettle})`
    : `translate(${-92*settle} ${90*settle-62*lift}) rotate(${-4*settle} 520 950)`);
  const reply = progress(t,2.90,.32);
  const follow = progress(t,4.42,.36);
  for (const [node,amount] of [[part('reply'),reply],[part('follow'),follow]]) {
    node.style.opacity=amount;
    node.setAttribute('transform',`translate(0 ${32*(1-amount)**2})`);
  }
  ink(part('ring'), progress(t,ending?tellIn+.15:4.92,.66));
  const slipSettle = (1-progress(t,moneyIn,.54))**3;
  part('transfer').setAttribute('transform',`translate(154 ${665+117*slipSettle}) rotate(${4*slipSettle} 375 200)`);
  ink(part('route'),progress(t,9.77,1.44));
  part('recipient').style.opacity=progress(t,11.11,.32);
  lines.forEach(([start],i) => appear(el('caption'+i), t>=start && t<(lines[i+1]?.[0]??16.5)));
}
renderAt(0);
window.__hf = window.__hf || {};
window.__hf.buildReady = { fonts: Promise.all([document.fonts.load('850 129px Archivo'),document.fonts.load('600 58px Archivo'),document.fonts.load('30px "IBM Plex Mono"')]) };
window.addEventListener('hf-seek', event => renderAt(event.detail.time));
window.__renderAt = renderAt;
