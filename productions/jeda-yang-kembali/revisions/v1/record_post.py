import json,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent
r=P/'PUBLISHING.json';d=json.loads(r.read_text(encoding='utf-8'))
result=json.loads((P/'buffer_result.json').read_text(encoding='utf-8'))
assert not result.get('isError')
post=json.loads(next(x['text'] for x in result['content'] if x['type']=='text'))
p=d['posts'][-1];p.update(buffer_post_id=post['id'],status=post['status'],observed=post,observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
intended=json.loads((P/'buffer_payload.json').read_text(encoding='utf-8'))
p['encoding_repair_pending']=post['text']!=intended['text']
r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'id':post['id'],'status':post['status'],'encoding_repair_pending':p['encoding_repair_pending']}))
