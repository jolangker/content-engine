import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
words = json.load(open(ROOT / 'assets/voice/narration/narration-full.words.json', encoding='utf-8'))
audio_meta = json.load(open(ROOT / 'audio_meta.json', encoding='utf-8'))
total_duration = audio_meta['total_duration_s']

def norm(text):
    return ''.join(re.findall(r'\w+', text.lower()))

# 7 Segmen narasi sesuai pembagian SCRIPT.md
scene_narrations = [
    {
        "n": 1,
        "id": "01-ekspektasi-pulang",
        "title": "Ekspektasi di Jalan Pulang",
        "text": "Lo seharian capek banget. Hari itu rasanya berat, dan di sepanjang jalan pulang, lo udah ngebayangin satu hal: pengen disambut hangat, ditemenin, atau sesederhana ditanya, “Hari ini gimana?”"
    },
    {
        "n": 2,
        "id": "02-respons-kontras",
        "title": "Respons Kontras & Sinyal Tubuh",
        "text": "Tapi begitu sampai rumah, situasinya beda. Dia cuma menyapa sekilas, lalu lanjut sibuk sama kegiatannya sendiri. Lo mulai menarik diri. Duduk agak jauh, helaan nafas lo dibikin lebih berat, dan nada bicara lo berubah pendek-pendek."
    },
    {
        "n": 3,
        "id": "03-jurang-persepsi",
        "title": "Jurang Persepsi",
        "text": "Di kepala lo, monolognya mulai ramai: “Masa kayak gini aja nggak peka? Gestur gue udah sejelas ini, masa harus disuruh dulu?” Lo merasa sinyal lo udah segede lampu sorot. Tapi di mata dia, lo cuma kelihatan lagi capek atau pengen tenang."
    },
    {
        "n": 4,
        "id": "04-illusion-transparency",
        "title": "Illusion of Transparency",
        "text": "Di psikologi, jurang persepsi ini dikenal sebagai illusion of transparency. Kecenderungan kita melebih-lebihkan sejauh mana isi pikiran, emosi, dan kebutuhan kita bisa terbaca oleh orang lain. Karena perasaan itu begitu nyata dan berisik di dalam diri kita, otak kita berasumsi orang luar pasti bisa menangkapnya dengan mudah."
    },
    {
        "n": 5,
        "id": "05-jebakan-kedekatan",
        "title": "Jebakan Kedekatan",
        "text": "Apalagi sama pasangan. Makin dekat hubungan kita, makin kuat godaan buat percaya bahwa kalau dia beneran sayang, dia harusnya otomatis tahu. Padahal, orang yang paling tulus menyayangi lo sekalipun, tetap nggak dibekali kemampuan membaca pikiran. Dia bukan cenayang."
    },
    {
        "n": 6,
        "id": "06-komunikasi-lugas",
        "title": "Alternatif Komunikasi Lugas",
        "text": "Waktu kita memilih diam dan menunggu dia menebak, kita sebenarnya lagi menyiapkan diri buat kecewa pada ekspektasi yang kita bangun sendiri. Lalu, apa alternatifnya? Coba ubah kode yang samar jadi kalimat yang lugas dan terukur: “Hari ini gue capek banget dan rasanya lagi sensitif. Gue nggak butuh solusi, tapi boleh nggak kita duduk bareng dulu setengah jam?”"
    },
    {
        "n": 7,
        "id": "07-refleksi-penutup",
        "title": "Refleksi Penutup",
        "text": "Sebelum lo terlanjur menyimpulkan bahwa dia nggak peduli... Coba ingat lagi: kebutuhan itu udah beneran keluar lewat kata-kata, atau baru sebatas skenario yang cuma lo putar di kepala lo sendiri?"
    }
]

# Match words cursor
cursor = 0
scene_map = []

for sc in scene_narrations:
    target_norm = norm(sc['text'])
    start_word_idx = cursor
    collected = ""
    while cursor < len(words) and len(collected) < len(target_norm):
        collected += norm(words[cursor]['text'])
        cursor += 1
    
    end_word_idx = cursor
    sc_words = words[start_word_idx:end_word_idx]
    
    scene_map.append({
        "n": sc['n'],
        "id": sc['id'],
        "title": sc['title'],
        "word_start": start_word_idx,
        "word_end": end_word_idx,
        "speech_start": sc_words[0]['start'],
        "speech_end": sc_words[-1]['end'],
        "words": sc_words
    })

print(f"Matched {len(scene_map)} scenes with {cursor}/{len(words)} words.")

# Calculate scene boundaries
frames = []
for i, sc in enumerate(scene_map):
    # Scene 1 starts at 0
    start = 0.0 if i == 0 else sc['speech_start'] - 0.15
    if i + 1 < len(scene_map):
        end = scene_map[i+1]['speech_start'] - 0.15
    else:
        end = total_duration
    
    duration = round(end - start, 3)
    frames.append({
        "n": sc['n'],
        "id": sc['id'],
        "title": sc['title'],
        "start": round(start, 3),
        "duration": duration,
        "speech_start": round(sc['speech_start'], 3),
        "speech_end": round(sc['speech_end'], 3),
        "word_count": len(sc['words']),
        "words": [
            {
                "text": w['text'],
                "start": round(w['start'], 3),
                "end": round(w['end'], 3)
            }
            for w in sc['words']
        ]
    })

(ROOT / 'timing.json').write_text(json.dumps(frames, indent=2, ensure_ascii=False), encoding='utf-8')
print("Saved timing.json")

# Build caption groups (kelompok 3-5 kata untuk karaoke subtitle pill)
caption_groups = []
group_size = 4
for f in frames:
    f_words = f['words']
    for i in range(0, len(f_words), group_size):
        chunk = f_words[i:i+group_size]
        caption_groups.append({
            "frame": f['n'],
            "start": chunk[0]['start'],
            "end": chunk[-1]['end'],
            "text": ' '.join(w['text'] for w in chunk),
            "words": chunk
        })

(ROOT / 'caption_groups.json').write_text(json.dumps(caption_groups, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Saved caption_groups.json ({len(caption_groups)} groups)")
