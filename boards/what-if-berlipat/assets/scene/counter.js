// Counter text for What If Berlipat: exact counts, short-scale names and fit-to-width sizing.
const SCALE = ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion"];

// Items on day d (day 1 = one item).
export const countOnDay = (day) => 2n ** BigInt(day - 1);

// "295,147,905,\n179,352,825,856": one line up to five groups, then the last four groups get their own line.
export function formatCount(value) {
  const groups = value.toLocaleString("en-US").split(",");
  if (groups.length <= 5) return groups.join(",");
  return groups.slice(0, -4).join(",") + ",\n" + groups.slice(-4).join(",");
}

// "295 quintillion" from a million up; smaller counts read fine as digits.
export function nameCount(value) {
  const digits = value.toString();
  const group = Math.floor((digits.length - 1) / 3);
  if (group < 2) return "";
  const head = Number(digits.slice(0, digits.length - group * 3 + 1)) / 10;
  const shown = head >= 10 ? Math.floor(head) : Math.floor(head * 10) / 10;
  return `${shown} ${SCALE[group]}`;
}

// Largest size (px) at which the longest line fits `maxWidth`, measured with the real face.
const measure = document.createElement("canvas").getContext("2d");
export function fitCount(text, { maxWidth = 768, max = 236, min = 96 } = {}) {
  measure.font = "800 100px Archivo";
  measure.fontStretch = "extra-condensed";
  const widest = Math.max(...text.split("\n").map((line) => measure.measureText(line).width));
  return Math.max(min, Math.min(max, Math.floor((maxWidth / widest) * 100)));
}
