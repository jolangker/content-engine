// Signing credentials arrive on stdin and are never written to the repository.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const dir=path.dirname(fileURLToPath(import.meta.url));
const receiptPath=path.join(dir,'PUBLISHING.json');
process.stdin.setRawMode?.(true);process.stdin.setEncoding('utf8');process.stdin.resume();
console.log('Ready for signed upload JSON on stdin (input echo disabled).');
let input='';
process.stdin.on('data',async chunk=>{
 input+=chunk;
 if(!/[\r\n]/.test(input))return;
 process.stdin.pause();
 try {
  const signed=JSON.parse(input.trim());input='';
  const receipt=JSON.parse(await readFile(receiptPath,'utf8'));
  const asset=receipt.assets.at(-1);
  const local=await readFile(path.join(dir,asset.local_file));
  if(createHash('sha256').update(local).digest('hex')!==asset.sha256)throw Error('Local export hash changed');
  if(signed.upload_params.public_id!==asset.public_id)throw Error('Signed public ID mismatch');
  if(!/^(api|api-eu|api-ap)\.cloudinary\.com$/.test(signed.host))throw Error('Unexpected Cloudinary host');
  const form=new FormData();form.set('file',new Blob([local],{type:'video/mp4'}),'jeda-yang-kembali.mp4');
  form.set('api_key',signed.api_key);form.set('signature',signed.signature);
  for(const [key,value] of Object.entries(signed.upload_params))form.set(key,String(value));
  asset.status='unknown';asset.attempt_started_at=new Date().toISOString();
  await writeFile(receiptPath,JSON.stringify(receipt,null,2)+'\n');
  const response=await fetch(`https://${signed.host}/v1_1/${signed.cloud_name}/video/upload`,{method:'POST',body:form,signal:AbortSignal.timeout(180000)});
  const result=await response.json();
  if(!response.ok||result.error){
   asset.status='error';asset.error={http_status:response.status,message:String(result.error?.message||'Upload rejected').replaceAll(signed.api_key,'[redacted]').replaceAll(signed.signature,'[redacted]')};
   await writeFile(receiptPath,JSON.stringify(receipt,null,2)+'\n');throw Error(`Cloudinary upload HTTP ${response.status}`);
  }
  if(result.public_id!==asset.public_id)throw Error('Returned public ID mismatch');
  for(const key of ['asset_id','public_id','resource_type','secure_url','bytes','width','height','duration','format','type','created_at','etag','version'])if(result[key]!==undefined)asset[key]=result[key];
  asset.status='uploaded';asset.uploaded_at=result.created_at;
  await writeFile(receiptPath,JSON.stringify(receipt,null,2)+'\n');
  const download=await fetch(asset.secure_url,{signal:AbortSignal.timeout(180000)});
  if(!download.ok)throw Error(`Original public URL HTTP ${download.status}`);
  const body=Buffer.from(await download.arrayBuffer());const sha=createHash('sha256').update(body).digest('hex');
  if(body.length!==local.length||sha!==asset.sha256)throw Error('Hosted original bytes or SHA-256 mismatch');
  asset.status='verified';asset.verified_at=new Date().toISOString();asset.download_verification={bytes:body.length,sha256:sha,content_type:download.headers.get('content-type'),http_status:download.status};
  await writeFile(receiptPath,JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify({status:asset.status,public_id:asset.public_id,secure_url:asset.secure_url,bytes:asset.bytes,sha256:sha,duration:asset.duration}));
  process.exit(0);
 }catch(error){console.error(error.message);process.exit(1);}
});
