import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';

// Use the exact pinned engine's own mixer and muxer. The video stream is copied, never re-encoded.
const project=process.cwd();
for(const file of ['audio-tags.html','assemble.py']){const p=path.join(project,file);fs.writeFileSync(p,fs.readFileSync(p,'utf8').replaceAll('data-volume="0.09"','data-volume="1"'));}
execFileSync('python',['build-index.py'],{cwd:project});
const engineDir=process.argv[2];if(!engineDir)throw Error('Pass the installed hyperframes@0.8.195 dist directory.');
const engine=await import(pathToFileURL(path.join(engineDir,'chunk-HJINEUHY.js')).href);
const work=path.join(project,'verification/audio-correction');fs.mkdirSync(work,{recursive:true});
const final=path.resolve(project,'../exports/hujan-bukan-sekadar-ember.mp4');
const original=path.join(work,'before-audio-correction.mp4');
if(!fs.existsSync(original))fs.copyFileSync(final,original);
const video=path.join(work,'video-only.mp4');
execFileSync('ffmpeg',['-v','error','-y','-i',original,'-map','0:v:0','-an','-c:v','copy',video]);
const html=fs.readFileSync(path.join(project,'index.html'),'utf8');
const elements=engine.parseAudioElements(html);
if(elements.length!==2)throw Error('Expected exactly narration and rain tracks');
const audioPath=path.join(work,'audio.m4a');
const mixed=await engine.processCompositionAudio(elements,project,path.join(work,'processing'),audioPath,84.69);
fs.writeFileSync(path.join(work,'mixer-result.json'),JSON.stringify(mixed,null,2));
if(!mixed.success)throw Error(JSON.stringify(mixed));
const staged=path.join(work,'corrected.mp4');
const muxed=await engine.muxVideoWithAudio(video,audioPath,staged);
if(!muxed.success)throw Error(JSON.stringify(muxed));
const streamHash=file=>execFileSync('ffmpeg',['-v','error','-i',file,'-map','0:v:0','-c','copy','-f','streamhash','-hash','sha256','-'],{encoding:'utf8'}).trim();
const before=streamHash(original),after=streamHash(staged);
if(before!==after)throw Error('Encoded video stream changed');
fs.copyFileSync(staged,final);
const receipt={engine:'hyperframes@0.8.195',operation:'processCompositionAudio + muxVideoWithAudio',reason:'Volume lanes multiply the static track gain; rain static gain changed from 0.09 to unity while retaining its 0–0.09 envelope.',elements,video_stream_before:before,video_stream_after:after,video_unchanged:true,output_sha256:crypto.createHash('sha256').update(fs.readFileSync(final)).digest('hex'),mixer:mixed,muxer:muxed};
fs.writeFileSync(path.join(work,'receipt.json'),JSON.stringify(receipt,null,2));
console.log(JSON.stringify({success:true,video_unchanged:true,path:final}));
