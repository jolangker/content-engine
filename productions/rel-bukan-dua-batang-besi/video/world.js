import * as T from './vendor/three.module.js';

const canvas=document.getElementById('rail-world');
const renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});
renderer.setSize(1080,1920,false);renderer.setPixelRatio(1);
renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.16;
const scene=new T.Scene();scene.background=new T.Color('#C5D5D8');scene.fog=new T.Fog('#C5D5D8',45,180);
const camera=new T.PerspectiveCamera(40,1080/1920,.02,350);
scene.add(new T.HemisphereLight('#fff2d8','#49635c',2.3));
const sun=new T.DirectionalLight('#fff0d6',3.4);sun.position.set(-12,18,9);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-17,right:17,top:17,bottom:-17,near:.1,far:65});sun.shadow.bias=-.00035;sun.shadow.normalBias=.025;scene.add(sun);
const rim=new T.DirectionalLight('#cae1e7',1.2);rim.position.set(14,7,-15);scene.add(rim);
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const mix=(a,b,p)=>a+(b-a)*p;const seed=i=>{let x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)};
const mats={};
function texture(c1,c2,scale=1){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');x.fillStyle=c1;x.fillRect(0,0,256,256);x.fillStyle=c2;for(let i=0;i<2400;i++){x.globalAlpha=.07+seed(i+73)*.23;x.fillRect(seed(i)*256,seed(i+5000)*256,1+seed(i+9)*5,1+seed(i+8)*4)}const t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(scale,scale);t.colorSpace=T.SRGBColorSpace;return t;}
const tex={soil:texture('#75604A','#bcaa85',12),grass:texture('#52684A','#87965b',35),concrete:texture('#aca99a','#5d625e',1),plaster:texture('#C6C1AD','#e3d9bd',2),road:texture('#656c69','#b4b7a8',7)};
function material(color,opts={}){const key=color+JSON.stringify(opts);return mats[key]??=(new T.MeshStandardMaterial({color,roughness:.85,...opts}));}
function obj(geo,mat,pos,parent=scene){const m=new T.Mesh(geo,mat);m.position.set(...pos);m.castShadow=m.receiveShadow=true;parent.add(m);return m;}
function box(pos,size,color,parent=scene,opts={}){return obj(new T.BoxGeometry(...size),typeof color==='string'?material(color,opts):color,pos,parent)}
function cyl(pos,r,h,color,parent=scene,opts={}){return obj(new T.CylinderGeometry(r,r,h,16),typeof color==='string'?material(color,opts):color,pos,parent)}
function ball(pos,size,color,parent=scene){const m=obj(new T.SphereGeometry(1,20,14),material(color),pos,parent);m.scale.set(...size);return m}
function group(pos=[0,0,0],parent=scene){const g=new T.Group();g.position.set(...pos);parent.add(g);return g}
function rod(a,b,r,color,parent=scene){const av=new T.Vector3(...a),bv=new T.Vector3(...b),d=bv.clone().sub(av);const m=cyl(av.clone().add(bv).multiplyScalar(.5).toArray(),r,d.length(),color,parent);m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d.normalize());return m}
const grassMat=material('#8a9a73',{map:tex.grass});const soilMat=material('#ad9574',{map:tex.soil});const concrete=material('#b5b4a5',{map:tex.concrete});const steel=material('#8E9997',{metalness:.68,roughness:.48});
box([0,-.75,0],[700,.4,700],grassMat);
box([10,-.49,0],[5,.08,300],material('#7c8078',{map:tex.road}));
// The formation continues down the route; the foreground diagnostic section is local.
const formation=group();box([0,-.36,0],[4.7,.54,22],soilMat,formation);box([0,-.05,0],[4.2,.10,22],concrete,formation);
const verge=group();box([-4,-.47,0],[3,.12,100],grassMat,verge);box([4,-.47,0],[2.5,.12,100],grassMat,verge);
const pad=box([-4.2,-.35,1.8],[2.3,.15,2.8],concrete);
function house(x,z,s){const h=group([x,-.5,z]);box([0,1.8*s,0],[4*s,3.6*s,5*s],material('#d0c7ad',{map:tex.plaster}),h);const roof=box([0,3.8*s,0],[4.6*s,.20*s,5.7*s],'#8F5140',h);roof.rotation.z=.1;box([-.8*s,1.7*s,2.51*s],[.9*s,1.2*s,.05],'#34525a',h);box([.8*s,.85*s,2.52*s],[.9*s,1.7*s,.05],'#65513E',h);for(let j=0;j<3;j++)box([-2.01*s,1.8*s,(-1.5+j*1.5)*s],[.06,.9*s,.7*s],'#34525a',h);}
for(let i=0;i<12;i++)house((i%2?1:-1)*(15+seed(i)*12),-40+i*12,.7+seed(i+99)*.4);
function tree(x,z,s){const g=group([x,-.5,z]);cyl([0,1.7*s,0],.14*s,3.4*s,'#65513E',g);for(let j=0;j<6;j++)ball([(seed(j+30)*2-1)*s,(3.0+seed(j+200)*1.3)*s,(seed(j+70)*2-1)*s],[1.0*s,.9*s,1.0*s],j%2?'#52684A':'#6A8052',g)}
for(let i=0;i<65;i++)tree((i%2?1:-1)*(9+seed(i+600)*42),-85+seed(i+300)*170,.7+seed(i+120)*.9);
for(let z=-60;z<65;z+=5){for(const x of [-6,6]){cyl([x,.1,z],.045,1.3,'#756a59');if(z<60)for(const y of [.05,.55])rod([x,y,z],[x,y,z+5],.018,'#8E9997');}if(z%15===0){cyl([12,3.2,z],.13,7.2,'#75604A');rod([12,6.6,z],[11,6.6,z],.04,'#65513E');rod([11,6.6,z],[11,6.2,z+15],.016,'#3d4845');}}
const equipment=group([5,-.4,6]);box([0,.4,0],[1.5,.8,2],'#CCA84F',equipment);box([0,.86,0],[1.25,.13,1.7],'#25494C',equipment);for(const x of [-.62,.62])for(const z of [-.65,.65]){const w=cyl([x,.1,z],.28,.15,'#283C3D',equipment);w.rotation.z=Math.PI/2}
// Track panel: recognisable rail I-profile with head, web, foot, pads, clips and sleepers.
const panel=group();const sleepers=[],clips=[],railSeats=[];
for(let z=-10.5;z<=10.5;z+=.65){const sl=group([0,.28,z],panel);const geom=new T.BoxGeometry(2.6,.22,.25);const sm=obj(geom,concrete,[0,0,0],sl);sleepers.push(sl);for(const x of [-.74,.74]){const seat=group([x,.15,0],sl);box([0,-.012,0],[.28,.035,.29],'#283C3D',seat);railSeats.push(seat);for(const side of [-1,1]){const cg=group([side*.13,.04,0],seat);const curve=new T.CatmullRomCurve3([new T.Vector3(-.07,.0,-.06),new T.Vector3(-.03,.065,-.06),new T.Vector3(.035,.055,.03),new T.Vector3(.08,.015,.07)]);obj(new T.TubeGeometry(curve,12,.018,6,false),steel,[0,0,0],cg);clips.push({g:cg,side});}}}
function makeRails(parent,length){const out=[];for(const x of [-.74,.74]){const g=group([x,.56,0],parent);box([0,-.08,0],[.15,.035,length],steel,g);box([0,0,0],[.035,.16,length],steel,g);box([0,.098,0],[.075,.045,length],steel,g);out.push(g)}return out}
const rails=makeRails(panel,22);
const extensions=group();for(const z of [-105,105]){const g=group([0,0,z],extensions);makeRails(g,188);for(let zz=-90;zz<=90;zz+=.75)box([0,.28,zz],[2.6,.22,.25],concrete,g);box([0,.10,0],[3.8,.24,188],'#696B64',g)}
// Seeded angular stones, not rounded pebble symbols.
const rockGeo=new T.DodecahedronGeometry(1,0);const rockMat=material('#8d8b7f',{roughness:1});
const ballast=group();const shoulder=group();const dummy=new T.Object3D();
function rockField(parent,count,wide){const m=new T.InstancedMesh(rockGeo,rockMat,count);m.castShadow=m.receiveShadow=true;const data=[];for(let i=0;i<count;i++){let x=(seed(i+4000)-.5)*(wide?4.25:2.7);let z=(seed(i+8000)-.5)*22;let y=.05+seed(i+2500)*.16;if(wide&&Math.abs(x)<1.3)x=Math.sign(x||1)*(1.35+seed(i+123)*.7);let size=.055+seed(i+88)*.045;dummy.position.set(x,y,z);dummy.rotation.set(seed(i)*2,seed(i+33)*3,seed(i+22)*3);dummy.scale.set(size,size*(.65+seed(i+900)*.6),size*(.7+seed(i+1000)*.5));dummy.updateMatrix();m.setMatrixAt(i,dummy.matrix);m.setColorAt(i,new T.Color().setHSL(.10,.05,.34+seed(i+565)*.22));data.push({x,y,z,size})}m.instanceMatrix.needsUpdate=true;parent.add(m);return {m,data}}
rockField(ballast,5600,false);rockField(shoulder,2700,true);
const falling=group();const fallingRocks=[];for(let i=0;i<60;i++){const m=obj(rockGeo,rockMat,[0,0,0],falling);m.scale.set(.07,.06,.08);fallingRocks.push(m)}
const macro=group([0,0,0]);const macroRocks=[];for(let i=0;i<13;i++){const m=obj(rockGeo,material(i%2?'#898b81':'#676f6a'),[(i%4)*.23-.4,.18+Math.floor(i/4)*.18,0],macro);m.rotation.set(seed(i),seed(i+2),seed(i+7));m.scale.set(.15,.12,.14);macroRocks.push(m)}
const fines=group();for(let i=0;i<110;i++){const m=obj(new T.IcosahedronGeometry(.025,0),material('#8f7054'),[(seed(i+90)-.5)*1.5,.18+seed(i+20)*.15,(seed(i+60)-.5)*1.0],fines)}
const screen=group([1.5,.8,0]);for(let i=-6;i<=6;i++){rod([-.7,i*.07,0],[.7,i*.07,0],.008,'#8E9997',screen);rod([i*.11,-.45,0],[i*.11,.45,0],.008,'#8E9997',screen)}
box([0,0,-.45],[1.5,.95,.07],'#65513E',screen);for(const x of [-.72,.72])for(const y of [-.47,.47])rod([x,y,0],[x,y,-.45],.018,'#8E9997',screen);
const hopper=group();box([0,1.9,0],[1.8,.7,1.5],'#CCA84F',hopper);box([0,1.52,0],[.55,.12,.6],'#53615f',hopper);
// Drain: one continuous open channel, lower outlet visible; diagnostic flow is a notation layer.
const drain=group();box([2.7,-.38,0],[.72,.08,24],concrete,drain);for(const x of [2.31,3.09])box([x,-.18,0],[.08,.38,24],concrete,drain);const outlet=group([2.7,-.36,11.5],drain);box([0,-.12,1.1],[.8,.07,2.4],concrete,outlet);
const waterMat=material('#4292AA',{roughness:.22,metalness:.15,transparent:true,opacity:.83});
const channelWater=box([2.7,-.27,0],[.62,.018,23],waterMat,drain);
const puddle=ball([-4.1,-.255,1.7],[1.0,.012,1.0],'#4292AA');puddle.material=waterMat;
const flow=group();const drops=[];for(let i=0;i<44;i++){const m=ball([0,0,0],[.04,.025,.07],'#2B9FCE',flow);m.castShadow=false;drops.push(m)}
const rain=group();const rainDrops=[];for(let i=0;i<130;i++){const m=rod([0,0,0],[0,.18,0],.008,'#99c8d1',rain);m.castShadow=false;rainDrops.push(m)}
const section=group();box([0,-.34,0],[3.8,.55,.08],soilMat,section);box([0,-.05,0],[3.8,.08,.09],concrete,section);
// Schematic load arrows, explicitly captioned as such.
const loads=group();const loadArrows=[];for(let i=0;i<5;i++){const a=new T.ArrowHelper(new T.Vector3(0,-1,0),new T.Vector3((i-2)*.4,1.2,0),.8,0xE56E43,.12,.07);loads.add(a);loadArrows.push(a)}
const sideArrows=group();for(const side of [-1,1])sideArrows.add(new T.ArrowHelper(new T.Vector3(-side,0,0),new T.Vector3(side*2.0,.5,0),.5,0xE56E43,.13,.08));
// Wheel set and a carriage share physical rail spacing and contact height.
const wheelset=group();const wheels=[];for(const x of [-.74,.74]){const w=cyl([x,1.12,0],.44,.13,'#53615f',wheelset,{metalness:.6,roughness:.45});w.rotation.z=Math.PI/2;wheels.push(w);const flange=cyl([x+(x>0?-.065:.065),1.12,0],.48,.025,'#3f504f',wheelset,{metalness:.6,roughness:.45});flange.rotation.z=Math.PI/2;}rod([-.83,1.12,0],[.83,1.12,0],.075,'#53615f',wheelset);
const train=group();const trainWheels=[];for(let j=0;j<2;j++){const car=group([0,0,-j*8],train);box([0,1.9,0],[2.7,2.3,7.3],'#d5d3bd',car);box([0,1.1,0],[2.72,.38,7.25],'#3C6261',car);box([0,3.1,0],[2.6,.18,7.2],'#8E9997',car);for(const side of [-1,1])for(let k=0;k<6;k++)box([side*1.36,2.25,-2.7+k*1.05],[.015,.75,.68],'#294c57',car);for(const z of [-2.3,2.3])for(const x of [-.74,.74]){const w=cyl([x,1.12,z],.44,.13,'#3d4b4d',car);w.rotation.z=Math.PI/2;trainWheels.push(w)}box([0,2.2,3.67],[2,.85,.035],'#294c57',car)}
// Maintenance head: panel lift first; tines then insert and squeeze under the sleeper.
const tamper=group();box([0,2.2,0],[3,.32,.8],'#CCA84F',tamper);for(const x of [-1.3,1.3])rod([x,.65,0],[x,2.1,0],.045,'#8E9997',tamper);const tineGroups=[];for(const side of [-1,1]){const g=group([0,0,side*.28],tamper);for(const x of [-.9,-.4,.4,.9]){rod([x,.18,0],[x,1.9,0],.035,'#53615f',g);box([x,.10,0],[.09,.25,.10],'#53615f',g)}tineGroups.push({g,side})}
// Adult rig. No toy head, giant eyes, or independent hands disconnected from arms.
const builder=group([-3.4,-.27,0]);
const hips=group([0,.82,0],builder);box([0,0,0],[.33,.23,.23],'#65513E',hips);
const torso=group([0,.92,0],builder);box([0,.25,0],[.47,.52,.25],'#3C6261',torso);box([-.13,.25,.134],[.07,.5,.02],'#CCA84F',torso);box([.13,.25,.134],[.07,.5,.02],'#CCA84F',torso);
const neck=cyl([0,.57,0],.055,.13,'#AB8567',torso);const head=group([0,.72,0],torso);ball([0,0,0],[.105,.135,.102],'#AB8567',head);ball([0,-.01,.107],[.027,.031,.026],'#AB8567',head);for(const x of [-.045,.045])ball([x,.03,.092],[.012,.009,.008],'#283C3D',head);const cap=cyl([0,.12,0],.115,.09,'#CCA84F',head);box([0,.087,.10],[.21,.025,.14],'#CCA84F',head);
const arms=[];for(const side of [-1,1]){const g=group([side*.27,.45,0],torso);cyl([0,-.14,0],.065,.27,'#3C6261',g);const elbow=group([0,-.28,0],g);cyl([0,-.13,0],.045,.26,'#AB8567',elbow);ball([0,-.28,0],[.05,.075,.045],'#AB8567',elbow);arms.push({g,elbow,side})}
const legs=[];for(const side of [-1,1]){const g=group([side*.11,.84,0],builder);cyl([0,-.19,0],.076,.36,'#65513E',g);const knee=group([0,-.38,0],g);cyl([0,-.16,0],.062,.32,'#65513E',knee);box([0,-.36,.06],[.16,.14,.28],'#283C3D',knee);legs.push({g,knee,side})}
const chair=group([-4.2,-.27,1.8]);const seat=box([0,.46,0],[.56,.05,.54],'#CCA84F',chair);const back=box([0,.77,-.25],[.56,.52,.055],'#3C6261',chair);for(const side of [-1,1]){rod([side*.25,0,-.24],[side*.25,.5,.25],.022,'#8E9997',chair);rod([side*.25,0,.25],[side*.25,.5,-.24],.022,'#8E9997',chair)}
const wheelLoadBase={};
// Start and end poses per shot. Positions in world metres, not a generic wrapper zoom.
const shots=[
 [[-6.0,4.3,8.8],[-5.0,3.5,7.4],[-.8,.45,.5],44],
 [[2.9,1.9,3.7],[2.0,1.45,2.4],[0,.48,0],36],
 [[4.3,3.3,3.9],[3.2,2.3,2.6],[0,.35,0],40],
 [[1.9,1.4,1.55],[1.42,1.02,1.0],[.74,.54,0],38],
 [[3.6,2.8,3.5],[2.4,1.6,2.1],[0,.25,0],42],
 [[-5.7,3.4,6.6],[-5.0,2.8,5.4],[-1.8,.3,1.2],44],
 [[-7.5,3.2,6.9],[-6.7,2.7,5.8],[-4.15,.55,1.9],42],
 [[4.6,4.3,4.6],[3.8,2.9,3.4],[1.1,-.02,0],40],
 [[4.5,2.0,6],[3.7,1.6,8],[2.3,-.05,4],40],
 [[2.8,2.2,3],[1.7,1.4,2],[.55,.35,0],40],
 [[3.6,2.5,3.5],[2.7,1.8,2.5],[0,.75,0],40],
 [[-6.8,4.8,9.5],[-9.2,6.5,12.5],[-1.3,.65,1.4],44]
];

function renderAt(t){
 const plan=window.RAIL_PLAN;let si=plan.findIndex(s=>t<s.end);if(si<0)si=plan.length-1;const s=plan[si];const u=clamp((t-s.start)/s.duration);let motion=u;if(s.phase_points){let j=s.phase_points.findIndex(p=>p[0]>=u);if(j<1)j=1;const a=s.phase_points[j-1],b=s.phase_points[j];motion=mix(a[1],b[1],clamp((u-a[0])/(b[0]-a[0])))}if(window.STATIC_STORYBOARD)motion=.68;const q=smooth(motion/.77);const action=(start,end)=>smooth((motion-start)/(end-start));
 const [a,b,target,fov]=shots[si];camera.position.set(...a.map((v,i)=>mix(v,b[i],q)));camera.fov=fov;camera.lookAt(...target);camera.updateProjectionMatrix();
 // Reset every channel explicitly: rendering out of order yields the same picture.
 panel.position.set(0,0,0);panel.rotation.set(0,0,0);rails.forEach(r=>r.position.y=.56);
 for(let i=0;i<sleepers.length;i++){const g=sleepers[i];g.position.x=0;g.position.y=.28;g.visible=si>=2;}
 clips.forEach(({g,side})=>{g.visible=si>=3;g.position.x=side*.13;g.position.y=.04});
 ballast.visible=si>=4;ballast.position.y=0;shoulder.visible=si>=5;shoulder.position.y=0;
 formation.visible=si>=7;drain.visible=si>=7;extensions.visible=si===11;
 wheelset.visible=si===1||si===2||si===4;wheelset.position.set(0,0,0);wheelset.rotation.set(0,0,0);
 train.visible=si===11;train.position.set(0,0,mix(-16,20,action(.06,.77)));trainWheels.forEach(w=>w.rotation.x=-t*3);
 tamper.visible=si===10;tamper.position.set(0,0,0);
 macro.visible=false;fines.visible=false;screen.visible=false;screen.rotation.set(0,0,0);hopper.visible=false;
 loads.visible=[1,2,4,8,11].includes(si);loads.position.set(0,0,0);loadArrows.forEach((a,i)=>{a.position.set((i-2)*.4,1.2,0);a.setLength(.8,.12,.07)});sideArrows.visible=si===5;
 falling.visible=si===4||si===5;fallingRocks.forEach((m,i)=>{const p=(motion*2+seed(i+5))%1;const x=si===5?1.5+(seed(i)-.5)*.7:(seed(i)-.5)*2;m.position.set(x,.12+(1-p)*2,(seed(i+62)-.5)*1.6)});
 rain.visible=si===6;rainDrops.forEach((m,i)=>{const p=(motion*3+seed(i+25))%1;m.position.set((seed(i+9)-.5)*10,1+(1-p)*5,(seed(i+42)-.5)*8)});
 flow.visible=si>=6&&si<=8;drops.forEach((m,i)=>{const p=(motion*.85+i/44)%1;let x,y,z;if(si===6){x=(seed(i+3)-.5)*2.4;y=.45-p*.5;z=(seed(i+5)-.5)*2;}else if(si===7){x=mix(.2,2.7,clamp(p*2));y=mix(.15,-.25,clamp(p*2));z=p<.5?0:(p-.5)*16;}else{x=2.7;y=-.22;z=mix(0,13,p)}m.position.set(x,y,z)});
 puddle.visible=si===6||si===7;puddle.scale.set(1,.012,1);channelWater.visible=si>=7;
 section.visible=si===1||si===7||si===8;section.position.set(0,0,.6);
 builder.visible=[0,5,6,11].includes(si);builder.position.set(-3.4,-.27,.1);builder.rotation.set(0,.6,0);torso.rotation.set(0,0,0);hips.position.y=.82;head.rotation.set(0,0,0);
 arms.forEach(({g,elbow,side})=>{g.rotation.set(0,0,side*.08);elbow.rotation.x=-.12});legs.forEach(({g,knee})=>{g.rotation.set(0,0,0);knee.rotation.set(0,0,0)});
 chair.position.set(-4.2,-.27,1.8);chair.rotation.set(0,0,0);chair.scale.set(1,1,1);chair.visible=si===0||si===5||si===6||si===11;
 if(si===0){const p=action(.04,.48);rails.forEach(r=>r.position.y=mix(1.5,-.13,p));builder.position.set(-1.9,-.5,1.7);builder.rotation.y=.1;arms[1].g.rotation.z=-1.2*action(.48,.68);arms[1].elbow.rotation.x=-1.2;head.rotation.y=.18;chair.scale.z=.22;}
 if(si===1){rails.forEach(r=>r.position.y=-.13-.06*action(.37,.6));wheelset.position.y=mix(.7,-.69,action(.12,.36));loads.position.y=-.45;loadArrows.forEach((a,i)=>{a.position.x=(i-2)*.17;a.setLength(.75,.12,.07)});}
 if(si===2){sleepers.forEach((g,i)=>g.position.x=-3.1*(1-action(.10+i*.002,.40+i*.002)));loadArrows.forEach((a,i)=>{a.position.x=(i-2)*.48;a.setLength(.7,.12,.07)});wheelset.visible=motion>.53;}
 if(si===3){clips.forEach(({g,side})=>{g.position.x=side*(.13+.18*(1-action(.42,.66)));g.position.y=.04+.08*(1-action(.12,.35))});railSeats.forEach(seat=>seat.position.y=.15+.08*(1-action(.08,.30)));}
 else railSeats.forEach(seat=>seat.position.y=.15);
 if(si===4){panel.position.y=.65*(1-action(.1,.48));ballast.position.y=-.5*(1-action(.1,.5));macro.visible=motion>.5;macro.position.set(.4,.06,.5);macro.scale.setScalar(.48);macroRocks.forEach((m,i)=>{m.position.x=(i%4)*.23-.4+(i%2?1:-1)*.25*(1-action(.50,.75))});falling.visible=motion<.52;hopper.visible=falling.visible;hopper.position.x=0;wheelset.visible=motion>.80;loadArrows.forEach((a,i)=>a.setLength(1.05,.12,.07));}
 if(si===5){shoulder.position.y=-.6*(1-action(.05,.4));falling.visible=motion<.45;hopper.visible=falling.visible;hopper.position.x=1.5;builder.position.set(-4.1,-.27,1.5);builder.rotation.y=-.5;arms[0].g.rotation.x=-.8;chair.scale.z=mix(.2,1,action(.55,.80));const move=action(.48,.77);camera.position.lerp(new T.Vector3(-6.7,2.6,5.8),move);camera.lookAt(new T.Vector3(...target).lerp(new T.Vector3(-3.6,.45,1.5),move));sideArrows.visible=motion<.56;}
 if(si===6){builder.position.set(-4.1,-.27,2.5);builder.rotation.y=Math.PI;legs[0].g.rotation.x=-.3*Math.sin(action(.05,.20)*Math.PI);const take=action(.50,.65);builder.position.y+=.10*Math.sin(take*Math.PI);torso.rotation.x=-.15*take;arms[0].g.rotation.x=-1.2*take;arms[1].g.rotation.x=-.8*take;head.rotation.x=.30*take;chair.position.y+=take*.38;chair.rotation.z=-.18*take;}
 if(si===7){formation.position.y=-.32*(1-action(.05,.35));drain.position.y=-.5*(1-action(.10,.45));const dry=1-action(.65,.95);puddle.scale.set(dry,.012,dry);}
 else{formation.position.y=0;drain.position.y=0;}
 if(si===8){section.position.z=4.0;loads.position.z=4;loadArrows.forEach((a,i)=>{a.position.x=(i-2)*.4;a.setLength(1.1,.12,.07)});}
 if(si===9){fines.visible=true;fines.position.set(0,mix(.5,0,action(.08,.37)),0);screen.visible=motion>.43;screen.position.set(mix(2.2,.4,action(.43,.65)),.72,0);screen.rotation.x=-Math.PI/2;if(motion>.43){const transfer=action(.43,.60);fines.position.set(.4*transfer,mix(0,.64,transfer)-.48*action(.65,.86),0);macro.visible=true;macro.position.set(.4,.72,0);macro.scale.setScalar(.48);macroRocks.forEach((m,i)=>{m.position.x=(i%4)*.23-.4;});}fines.scale.setScalar(1);}
 else fines.scale.setScalar(1);
 if(si===10){const lift=.10*action(.05,.28)*(1-action(.78,.92));panel.position.y=lift;tamper.position.y=.7*(1-action(.2,.47));tineGroups.forEach(({g,side})=>{g.position.z=side*mix(.36,.13,action(.48,.7));g.position.y=action(.78,.95)*1.0});}
 if(si===11){loadArrows.forEach((a,i)=>{a.position.x=(i-2)*.4;a.setLength(1.1,.12,.07)});loads.visible=motion<.35;builder.position.set(-4.2,-.27,1.85);builder.rotation.y=0;const sit=action(.72,.91);builder.position.y-=sit*.38;legs.forEach(({g,knee})=>{g.rotation.x=-sit*1.35;knee.rotation.x=sit*1.5});torso.rotation.x=-.05*sit;arms[0].g.rotation.x=-.45*sit;arms[1].g.rotation.x=-.35*sit;const callback=action(.66,.88);camera.position.lerp(new T.Vector3(-6.7,2.6,5.8),callback);camera.lookAt(new T.Vector3(...target).lerp(new T.Vector3(-3.7,.6,1.6),callback));}
 // Macro stones appear in a teaching window only; the rest of the bed retains identity.
 const note=document.getElementById('schematic-note');note.style.opacity=loads.visible||flow.visible||sideArrows.visible||si===9?'1':'0';note.textContent=si===9?'Skema pembersihan balas':'Skema gaya / aliran';
 renderer.render(scene,camera);
 window.RAIL_STATE={t,scene:si+1,camera:camera.position.toArray(),target,trackHeight:panel.position.y};
}
window.addEventListener('hf-seek',e=>renderAt(e.detail.time));window.railRenderAt=renderAt;renderAt(window.__hfThreeTime||0);
