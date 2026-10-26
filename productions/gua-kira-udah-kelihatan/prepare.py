"""Prepare the selected script and self-contained board assets; no API calls."""
from pathlib import Path
import importlib.util
import json
import re
import shutil

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
V = P / 'video'
BOARD = ROOT / 'boards/ruang-di-antara'

LINES = [
    ('The canceled plan', 'Lo mendadak irit ngomong setelah rencana kalian batal.', 'Rencana batal', 'conversational, quietly disappointed'),
    ('The inside view', 'Di kepala lo udah jelas: gua kecewa. Tapi yang sampai ke dia apa?', 'Udah kelihatan?', ''),
    ('The concept', 'Ada konsep yang relevan: illusion of transparency, atau ilusi transparansi.', 'Illusion of transparency', 'clear, gently explanatory'),
    ('What it means', 'Kita bisa mengira orang lain lebih jelas membaca perasaan kita daripada yang sebenarnya.', 'Terasa jelas', ''),
    ('The internal experience', 'Lo ngerasain kecewanya langsung, lengkap sama harapan yang tadi lo bawa.', '', 'intimate, reflective'),
    ('Estimating another view', 'Saat membayangkan pandangan dia, pengalaman lo sendiri bisa tetap jadi patokan.', 'Dari dalam', ''),
    ('The external view', 'Padahal yang terlihat mungkin cuma jawaban pendek dan lo yang lebih diam.', 'Dari luar', 'observant, measured'),
    ('A missing meaning', 'Dia mungkin sadar ada perubahan, tapi belum tahu apa yang bikin lo kecewa.', 'Belum tentu jelas', ''),
    ('A limit of interpretation', 'Ini kemungkinan penjelasan. Satu kejadian belum cukup buat menilai kepedulian dia.', '', 'gentle, precise'),
    ('The useful distinction', 'Kuatnya perasaan dan jelasnya pesan adalah dua hal yang perlu dibedakan.', 'Rasa / pesan', 'quietly firm'),
    ('Make room to speak', 'Coba beri dia informasi yang selama ini cuma ada di kepala lo.', '', 'open, inviting'),
    ('Name the feeling', 'Gua kecewa rencana kita batal.', 'Gua kecewa', 'sincere, speaking to a partner'),
    ('Name the context', 'Gua tadi udah nungguin waktu bareng.', 'Nungguin waktu bareng', ''),
    ('What the words offer', 'Sekarang ada perasaan dan konteks yang bisa ditanggapi. Memahami tetap butuh usaha bersama.', 'Bisa ditanggapi', 'warm, grounded'),
    ('Keep responsibility visible', 'Kalau udah jelas disampaikan tapi terus diabaikan, lihat juga pola responsnya.', 'Lihat responsnya', 'calm, gently firm'),
    ('Answer the opening', 'Jadi, jangan cuma mengukur seberapa kuat lo merasa. Cek juga apa yang udah lo sampaikan.', 'Apa yang tersampaikan?', 'intimate, reflective'),
]

def main():
    spec=importlib.util.spec_from_file_location('narration_policy',ROOT/'.agents/skills/shortform-production/scripts/narration.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    voice,resolution=mod.resolve_voice(ROOT)
    lines=[{'id':i+1,'title':title,'text':text,'emphasis':emphasis,'delivery':tag,'dramatic':i+1 in (8,10)} for i,(title,text,emphasis,tag) in enumerate(LINES)]
    words=sum(len(re.findall(r'\S+',x['text'])) for x in lines)
    doc=f'''# SCRIPT — Gua kira udah kelihatan

Version 1; agent-verified under the activated after-hook policy. {words} spoken words.
Hook 2 was human-selected; the script as a whole is agent-verified, not human-approved.

**Voice:** ElevenLabs / {voice} / eleven_v4; resolved from root .env.
**Voice settings:** Native speed 1, one continuous full-script request.
**Voice direction:** Intimate conversational Indonesian lo-gua; curiosity before explanation, restrained disappointment, no diagnostic or presenter cadence.
**Timing:** Initial estimates only. Final scene timing follows measured word alignment. Speech may cross composition boundaries.

'''
    for x in lines:
        doc+=f"## Line {x['id']} — {x['title']} (Frame {x['id']})\n\n**Time:** Estimated; mapped after synthesis.\n**Delivery:** {x['delivery'] or 'Continue naturally.'}\n\n    {x['text']}\n\n**On-screen:** {x['emphasis'] or 'No emphasis copy.'}\n\n"
    doc+='''## Evidence and editorial verification

SOURCES.md C1-C3 support the definition and proposed explanation; C4-C6 bound the fictional scene and application. No research statistic or couple-specific causal claim is used. Lines 4-10 make the explanation and scene discussion central; lines 11-14 derive one concrete application. Line 15 preserves responsibility for repeated disregard. The closing answers what information was communicated, without promising a partner's response.

The English name and Indonesian gloss are spoken early. The exact user-selected hook spans Lines 1-2. Two charcoal shots are planned at Frames 8 (the meaning may remain unknown) and 10 (the distinction becomes clear); they emphasize turns without inventing harm.
'''
    (P/'SCRIPT.md').write_text(doc,encoding='utf-8')
    (V/'SCRIPT.md').write_text(doc,encoding='utf-8')
    (V/'script_data.json').write_text(json.dumps(lines,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    tagged='\n\n'.join((f"[{x['delivery']}] " if x['delivery'] else '')+x['text'] for x in lines)
    request={'provider':'elevenlabs','lang':'id','voice':voice,'voice_resolution':resolution,'tts_model':'eleven_v4','speed':1,'lines':[{'id':'narration','text':tagged}],'bgm':{'mode':'none'}}
    (V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for file in (BOARD/'assets').iterdir():
        if file.is_file() and file.suffix in ('.ttf','.txt'):
            shutil.copy2(file,V/'assets/fonts'/file.name)
    shutil.copy2(BOARD/'frame.md',V/'frame.md')
    shutil.copytree(BOARD/'components',V/'assets/board/components',dirs_exist_ok=True)
    shutil.copytree(BOARD/'assets/audio/sfx',V/'assets/board/audio/sfx',dirs_exist_ok=True)
    print(json.dumps({'script_words':words,'voice':voice,'model':'eleven_v4','scene_count':len(lines),'synthesis_started':False}))

if __name__=='__main__': main()
