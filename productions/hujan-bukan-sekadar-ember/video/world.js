import * as T from './vendor/three.module.js';

// Original episode geometry. All motion is reconstructed from absolute timeline time.
const C={sky:'#8CCFE8',ink:'#173B42',cream:'#FFF5DE',grass:'#75A954',light:'#A3C76C',earth:'#B77C51',deep:'#875B43',sand:'#D7B286',stone:'#758184',steel:'#9BAFB2',teal:'#178A91',water:'#2B9FCE',warm:'#E56E43',yellow:'#F4C44B',white:'#F7F5EB',skin:'#D9AE85',roof:'#D66B44',wood:'#855C40'};
const scene=new T.Scene();scene.background=new T.Color(C.sky);
const canvas=document.getElementById('world');
const renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true});
renderer.setSize(1080,1920,false);renderer.setPixelRatio(1);renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.25;
const camera=new T.OrthographicCamera(-5.1,5.1,9.06,-9.06,.1,100);
scene.add(new T.HemisphereLight(C.cream,C.teal,2.3));
const sun=new T.DirectionalLight(C.cream,3.4);sun.position.set(-5,11,6);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-9;sun.shadow.camera.right=9;sun.shadow.camera.top=9;sun.shadow.camera.bottom=-9;sun.shadow.normalBias=.025;sun.shadow.bias=-.0004;scene.add(sun);
const materials={};
function mat(c){return materials[c]??=(new T.MeshStandardMaterial({color:C[c]||c,roughness:.78,metalness:c==='steel'?.18:0}));}
function mesh(geo,c,p,parent=scene){let m=new T.Mesh(geo,mat(c));m.position.set(...p);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function box(p,s,c,parent=scene){return mesh(new T.BoxGeometry(...s),c,p,parent);}
function ball(p,s,c,parent=scene){let m=mesh(new T.SphereGeometry(1,24,16),c,p,parent);m.scale.set(...s);return m;}
function cyl(p,r,h,c,parent=scene){return mesh(new T.CylinderGeometry(r,r,h,40),c,p,parent);}
function rod(a,b,r,c,parent=scene){const av=new T.Vector3(...a),bv=new T.Vector3(...b),d=bv.clone().sub(av);let m=cyl(av.clone().add(bv).multiplyScalar(.5).toArray(),r,d.length(),c,parent);m.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),d.normalize());return m;}
function pipe(points,r,c,parent=scene){let curve=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)),false,'catmullrom',.01);let m=mesh(new T.TubeGeometry(curve,80,r,12,false),c,[0,0,0],parent);return {mesh:m,curve};}
function group(p=[0,0,0]){const g=new T.Group();g.position.set(...p);scene.add(g);return g;}
const land=group();box([0,-.5,0],[8.7,.8,6.5],'earth',land);box([0,-1.05,0],[8.7,.3,6.5],'deep',land);box([0,-.12,0],[8.8,.18,6.6],'grass',land);
for(let i=0;i<30;i++){let x=((i*71)%83)/10-4.1,z=((i*37)%61)/10-3;ball([x,-.38-(i%3)*.16,3.26],[.07+(i%3)*.03,.045,.04],'sand',land);}
const floor=box([0,-1.35,0],[200,.1,200],'sky');floor.receiveShadow=true;
function tree(x,z,s){let g=group([x,0,z]);rod([0,0,0],[0,2.1*s,0],.12*s,'wood',g);for(let i=0;i<3;i++)ball([(i-1)*.32*s,(1.75+i*.34)*s,0],[.67*s,.75*s,.65*s],i%2?'grass':'light',g);}
tree(-3.5,-2.3,.9);tree(3.5,-2.25,.72);tree(-3.5,2.2,.55);
for(let i=0;i<3;i++){let g=group([-4+i*4,6.6+(i%2),-5]);for(let j=0;j<3;j++)ball([(j-1)*.55,(j%2)*.17,0],[.65,.3,.3],'white',g);}
// House roof pitches down toward the visible front gutter (positive z).
const house=group([-1.75,0,-.65]);box([0,1.02,0],[3.15,2.05,2.7],'cream',house);
house.scale.y=1.42;
box([-.7,.74,1.37],[.65,1.5,.08],'wood',house);box([-.68,.78,1.42],[.5,1.35,.035],'teal',house);ball([-.51,.77,1.47],[.035,.035,.02],'yellow',house);
for(const x of [.6]){box([x,1.3,1.385],[.85,.78,.08],'white',house);box([x,1.3,1.44],[.68,.63,.03],'water',house);box([x,1.3,1.47],[.045,.67,.02],'cream',house);box([x,1.3,1.47],[.72,.045,.02],'cream',house);}
const shape=new T.Shape();shape.moveTo(-1.74,0);shape.lineTo(0,1.03);shape.lineTo(1.74,0);shape.closePath();let roofgeo=new T.ExtrudeGeometry(shape,{depth:3,bevelEnabled:false});let roof=mesh(roofgeo,'roof',[0,2.03,-1.5],house);roof.rotation.y=Math.PI/2;
// Replace extrusion orientation with two explicit pitched panels for a readable tiled roof.
roof.visible=false;
for(let side of [-1,1]){let p=box([0,2.5,side*.77],[3.55,.15,1.85],'roof',house);p.rotation.x=side*.51;for(let j=0;j<8;j++){let strip=box([-1.54+j*.44,2.585,side*.77],[.035,.035,1.86],'warm',house);strip.rotation.x=side*.51;}}
rod([-1.82,2.94,0],[1.82,2.94,0],.09,'warm',house);
// Patio and chair: the planted prop remains at the same world coordinates.
for(let i=0;i<4;i++)box([-2.7+i*.55,.02,1.5],[.49,.08,.46],'sand');
const chair=group([-.65,0,2.25]);let seat=box([0,.49,0],[.62,.08,.58],'cream',chair),back=box([0,.9,-.28],[.62,.72,.075],'cream',chair);back.rotation.x=-.13;
for(let x of [-.25,.25]){rod([x,.03,-.27],[x,.77,.24],.035,'wood',chair);rod([x,.03,.27],[x,.74,-.25],.035,'wood',chair);}
// Friendly recurring builder with articulated sleeves/arms.
const builder=group([-.1,0,1.7]);builder.rotation.y=-.2;
box([0,.76,0],[.48,.58,.31],'teal',builder);box([0,.79,.168],[.19,.17,.035],'yellow',builder);
const legs=[],boots=[],shins=[];for(let x of [-.14,.14]){legs.push(rod([x,.14,0],[x,.5,0],.105,'teal',builder));boots.push(box([x,.1,.08],[.22,.2,.36],'ink',builder));let shin=rod([x,.13,.4],[x,.47,.4],.09,'teal',builder);shin.visible=false;shins.push(shin);}
ball([0,1.28,0],[.25,.28,.24],'skin',builder);ball([0,1.49,0],[.28,.15,.265],'yellow',builder);box([0,1.45,.18],[.54,.05,.31],'yellow',builder);
for(let x of [-.085,.085])ball([x,1.31,.224],[.024,.03,.017],'ink',builder);ball([0,1.2,.242],[.04,.017,.013],'wood',builder);
const arms=[];for(let side of [-1,1]){let g=new T.Group();g.position.set(side*.24,1.0,0);builder.add(g);rod([0,0,0],[side*.13,-.31,.06],.085,'cream',g);ball([side*.14,-.34,.07],[.085,.085,.085],'skin',g);arms.push(g);}
const bucket=group([.35,0,2.3]);cyl([0,.24,0],.25,.43,'steel',bucket);cyl([0,.46,0],.22,.025,'water',bucket);let bh=mesh(new T.TorusGeometry(.25,.018,8,24,Math.PI),'ink',[0,.54,0],bucket);bh.rotation.z=0;
// Tank, stable pad and a deliberate sectional front wall.
const tank=group([2,0,.25]);box([0,.09,0],[2.25,.22,2.25],'stone',tank);
const shellmat=mat('teal');shellmat.side=T.DoubleSide;
const tankBack=mesh(new T.CylinderGeometry(.91,.91,2.35,64,1,true,Math.PI*.5,Math.PI),'teal',[0,1.39,0],tank);
const tankFront=mesh(new T.CylinderGeometry(.91,.91,2.35,64,1,true,-Math.PI*.5,Math.PI),'teal',[0,1.39,0],tank);
cyl([0,.235,0],.91,.10,'teal',tank);const rim=mesh(new T.TorusGeometry(.91,.045,10,64),'teal',[0,2.58,0],tank);rim.rotation.x=Math.PI/2;
const lidGroup=new T.Group();tank.add(lidGroup);const lid=cyl([0,2.67,0],.97,.12,'teal',lidGroup);cyl([0,2.76,0],.18,.08,'ink',lidGroup);
const water=mesh(new T.CylinderGeometry(.865,.865,1,64),'water',[0,.8,0],tank);water.material=new T.MeshStandardMaterial({color:C.water,roughness:.23,transparent:true,opacity:.88});
const bands=[];for(let y of [.42,.8,1.2,1.6,2,2.42]){let b=mesh(new T.TorusGeometry(.924,.027,8,64,Math.PI),'steel',[0,y,0],tank);b.rotation.x=Math.PI/2;b.rotation.z=Math.PI/2;bands.push(b);}
const vent=group([2,2.74,.25]);pipe([[0,0,0],[0,.35,0],[.25,.4,0],[.32,.22,0]],.065,'white',vent);
function screen(x,y,z,size,parent=scene){let g=new T.Group();g.position.set(x,y,z);parent.add(g);for(let i=0;i<7;i++){let q=-size/2+i*size/6;rod([q,-size/2,0],[q,size/2,0],.008,'ink',g);rod([-size/2,q,0],[size/2,q,0],.008,'ink',g);}return g;}
screen(.32,.2,.01,.13,vent);
const gutter=group();pipe([[-3.4,2.12,.93],[-1.8,2.12,.93],[-.08,2.12,.93],[-.08,2.85,1.05],[.4,2.85,1.05]],.085,'white',gutter);
// The gutter's slight upward elbow above is omitted from the hydraulic path below: downspout connects from the gutter at 2.12.
gutter.clear();pipe([[-3.4,3.01,.93],[-1.8,3.01,.93],[-.12,3.01,.93]],.09,'white',gutter);
pipe([[-.12,3.01,.93],[.1,3.0,.93],[.18,2.97,.93],[.18,2.91,.93]],.10,'white',gutter);
const leafScreen=group([.18,2.9,.93]);let screenPlate=screen(0,0,0,.40,leafScreen);screenPlate.rotation.x=-Math.PI/2;for(let a of [-.23,.23]){rod([a,0,-.23],[a,0,.23],.035,'steel',leafScreen);rod([-.23,0,a],[.23,0,a],.035,'steel',leafScreen);}
const debris=[];for(let i=0;i<5;i++){let l=ball([-.05+(i%3)*.07,.055+i*.018,-.12+(i%2)*.16],[.10,.025,.05],i%2?'yellow':'wood',leafScreen);l.rotation.y=i*.8;debris.push(l);}
const connection=group();pipe([[.18,1.73,.93],[.18,1.45,.93],[.55,1.43,.93],[.75,2.15,.8],[1.08,2.3,.25]],.082,'white',connection);
// Tank inlet is slightly below the collecting gutter; visual scale is schematic.
connection.clear();pipe([[.18,1.73,.93],[.18,1.45,.93],[.6,1.45,.93],[.75,1.95,.7],[1.12,2.0,.25]],.08,'white',connection);
// The sloping approach is schematic but must not rise against gravity: corrected to a constant falling run.
connection.clear();pipe([[.18,2.84,.93],[.18,2.76,.93],[.7,2.75,.93],[1.12,2.48,.25]],.08,'white',connection);
const ff=group([.18,0,.93]);const ffBack=mesh(new T.CylinderGeometry(.20,.20,2.25,40,1,true,Math.PI*.5,Math.PI),'white',[0,1.575,0],ff);ffBack.material.side=T.DoubleSide;
const ffFront=mesh(new T.CylinderGeometry(.20,.20,2.25,40,1,true,-Math.PI*.5,Math.PI),'white',[0,1.575,0],ff);ffFront.material.side=T.DoubleSide;
cyl([0,.42,0],.22,.08,'white',ff);pipe([[0,.42,0],[0,.24,0],[.22,.18,0]],.035,'white',ff);const ffwater=cyl([0,.7,0],.17,1,'earth',ff);for(let x of [-.2,.2])rod([x,.45,0],[x,2.7,0],.016,'white',ff);
// For hydraulic consistency the tank receives into its side BELOW the tee; fill in this simplified episode is below that inlet until overflow shot.
const overflow=group();const outpath=pipe([[2.86,2.25,.25],[3.22,2.25,.25],[3.28,1.7,.25],[3.28,.3,1.45],[3.65,.10,2.5]],.095,'white',overflow);screen(3.65,.12,2.57,.19,overflow);
const bed=group([3.2,0,2.4]);box([0,.01,0],[1.45,.1,1.1],'deep',bed);for(let i=0;i<6;i++)ball([-.6+i*.24,-.03,.47],[.15,.10,.12],'stone',bed);
const tap=group([2.0,.75,1.13]);pipe([[0,0,0],[0,0,.2],[0,-.12,.26]],.045,'steel',tap);rod([-.12,.1,.13],[.12,.1,.13],.025,'yellow',tap);
const can=group([2.0,0,1.65]);cyl([0,.28,0],.24,.42,'yellow',can);rod([.15,.26,0],[.5,.6,0],.065,'yellow',can);let handle=mesh(new T.TorusGeometry(.22,.027,8,24,Math.PI),'yellow',[-.2,.37,0],can);handle.rotation.z=Math.PI/2;
const plant=group([1.3,0,2.6]);cyl([0,.2,0],.32,.37,'roof',plant);cyl([0,.4,0],.34,.07,'roof',plant);rod([0,.4,0],[0,1.05,0],.028,'grass',plant);for(let i=0;i<5;i++){let a=i*2.4;ball([Math.cos(a)*.17,.55+i*.09,Math.sin(a)*.17],[.19,.05,.09],'light',plant);}
// Clearly theatrical visitor: an oversized mosquito with little luggage.
const bug=group([3.8,3.2,1.2]);ball([0,0,0],[.22,.14,.34],'ink',bug);ball([0,.04,.32],[.14,.14,.15],'ink',bug);rod([0,.04,.4],[0,-.04,.7],.015,'ink',bug);const wings=[];for(let s of [-1,1]){wings.push(ball([s*.23,.13,-.02],[.30,.025,.17],'white',bug));for(let i=0;i<3;i++)rod([s*.13,-.06,-.16+i*.17],[s*.4,-.3,-.1+i*.17],.014,'ink',bug);}
box([.48,-.3,-.06],[.28,.32,.19],'warm',bug);rod([.4,-.09,-.06],[.56,-.09,-.06],.018,'ink',bug);for(let x of [.39,.56])ball([x,-.49,-.06],[.04,.04,.03],'ink',bug);
// A seeded rain field and finite flow dots; no random runtime or free-running loop.
const rain=[];for(let i=0;i<90;i++){let x=((i*47)%89)/10-4.4,z=((i*31)%59)/10-2.9;rain.push(rod([x,0,z],[x+.035,.18,z],.012,'water'));}
const flows=[];function flow(points,count=20,color='water'){let path=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)),false,'catmullrom',.01),dots=[];for(let i=0;i<count;i++)dots.push(ball([0,0,0],[.045,.06,.045],color));let f={path,dots};flows.push(f);return f;}
const roofFlow=flow([[-3,4.05,-.65],[-3,3.6,0],[-3,3.02,.93],[-1,3.02,.93],[.18,2.85,.93]],26);
const downFlow=flow([[.18,2.76,.93],[.18,1.6,.93],[.18,.5,.93]],10,'sand');
const inFlow=flow([[.18,2.76,.93],[.7,2.75,.93],[1.12,2.48,.25],[1.7,2.48,.25]],12);
const dustFlow=flow([[.18,2.88,.93],[.18,2.76,.93],[.7,2.75,.93],[1.12,2.48,.25]],7,'sand');dustFlow.dots.forEach(d=>d.scale.multiplyScalar(.6));
const overflowFlow=flow([[2.86,2.25,.25],[3.22,2.25,.25],[3.28,1.7,.25],[3.28,.3,1.45],[3.65,.10,2.5]],20);
const drainFlow=flow([[.4,.18,.93],[.6,.02,.95]],4,'sand');
const tapFlow=flow([[2,.63,1.39],[2,.53,1.5]],5);
const pourFlow=flow([[1.589,.851,2.6],[1.3,.68,2.6],[1.3,.4,2.6]],8);
const clamp=x=>Math.max(0,Math.min(1,x)),smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
const lerp=(a,b,x)=>a+(b-a)*x;
let plan=window.EPISODE_PLAN||[];
function route(f,t,visible,speed=1){f.dots.forEach((d,i)=>{d.visible=visible;let u=((t*speed*.18+i/f.dots.length)%1+1)%1;d.position.copy(f.path.getPointAt(u));});}
function show(g,value){g.visible=value;}
function pose(t){
  const timing=window.EPISODE_TIMING||{starts:[0,15,29,48,66,79],ends:[15,29,48,66,79,94]};
  let n=timing.starts.reduce((v,s,i)=>t>=s?i:v,0),s=timing.starts[n],d=timing.ends[n]-s,q=clamp((t-s)/d),local=t-s;
  // Planned-state stills use this same renderer; motion is enabled only after the board is verified.
  const staticMode=window.STATIC_STORYBOARD===true;
  let phase=staticMode?.7:q;
  const cues=window.EPISODE_CUES||{};
  const reached=(name,fallback)=>staticMode?fallback:t>=(cues[name]??1e5);
  const progress=(name,duration=.5)=>staticMode?1:smooth((t-(cues[name]??0))/duration);
  tank.visible=reached('tank',n>0||phase>.56);gutter.visible=reached('gutter',n>0||phase>.45);connection.visible=tank.visible;leafScreen.visible=reached('screen',n>=1);ff.visible=reached('firstflush',n>=2);
  tank.position.y=.35*(1-progress('tank'));gutter.position.y=.25*(1-progress('gutter'));leafScreen.position.y=2.9+.25*(1-progress('screen'));ff.position.y=.25*(1-progress('firstflush'));
  lidGroup.visible=reached('lid',n>3||(n===3&&phase>.52));vent.visible=lidGroup.visible;overflow.visible=reached('overflow',n>=4);lidGroup.position.y=.8*(1-progress('lid',.8));
  tankFront.visible=!(n===2||n===4);ffFront.visible=!(n===2);bands.forEach(b=>b.visible=tankFront.visible);
  // Tank inlet/outlet levels are schematic; tank section fills from diverted input and later reaches its overflow.
  let level=n<2?.25:n===2?lerp(.3,1.15,progress('bypass',3)):n===3?1.2:n===4?lerp(1.2,2.02,progress('full',2)):1.8;
  water.scale.y=level;water.position.y=.28+level/2;
  ffwater.scale.y=n===2?lerp(.15,2.2,staticMode?1:smooth((t-cues.firstflush)/(cues.bypass-cues.firstflush))):(n>2?2.2:.15);ffwater.position.y=.48+.5*ffwater.scale.y;
  if(n===2&&reached('drain',phase>.78)){ffwater.scale.y=lerp(2.2,.15,progress('drain',4));ffwater.position.y=.48+.5*ffwater.scale.y;}
  bucket.visible=n===0;can.visible=n===5;
  chair.visible=n>=3||n===0;
  chair.scale.setScalar(n===3?lerp(.4,1,smooth(phase*5)):1);
  bug.visible=n===3&&reached('bug',true);bug.position.set(lerp(4.6,2.8,progress('bug',.65)),3.15+Math.sin(local*2)*.05,1.2);
  if(n===3&&reached('lid',phase>.53))bug.position.x=lerp(2.8,3.7,progress('lid',1));
  wings.forEach((w,i)=>w.rotation.z=(i?1:-1)*Math.sin(local*32)*.25);
  builder.position.set(n===5?1.35:-.1,0,n===5?1.5:1.9);builder.rotation.y=n===5?0:-.35;
  builder.rotation.z=n===3&&phase>.15&&phase<.42?-.15:0;
  arms[0].rotation.z=n===0&&phase<.4?-.8:n===3&&phase>.18&&phase<.43?-.8:0;
  arms[1].rotation.z=n===0&&phase<.4?.9:n===3&&phase>.18&&phase<.43?.8:n===5&&phase<.35?-.8:0;
  const pouring=n===5&&reached('pour',phase>.2)&&!reached('maintain',phase>.42);
  can.position.set(2,.05,1.5);can.rotation.z=0;
  if(n===5&&reached('pour',phase>.2)){builder.position.set(.35,0,2.55);builder.rotation.y=0;can.position.set(.85,pouring?.6:.05,2.6);can.rotation.z=pouring?-.55:0;arms[1].rotation.z=pouring?.7:0;}
  legs.forEach(l=>{l.rotation.x=0;l.position.y=.32;l.position.z=0;});boots.forEach(b=>b.position.z=.08);shins.forEach(s=>s.visible=false);
  if(n===5&&reached('sit',phase>.7)){let p=progress('sit',.8);builder.position.set(lerp(.35,-.65,p),0,lerp(2.55,2.17,p));arms[0].rotation.z=.1;arms[1].rotation.z=-.1;legs.forEach(l=>{l.rotation.x=p*Math.PI/2;l.position.y=lerp(.32,.47,p);l.position.z=.18*p;});boots.forEach(b=>b.position.z=lerp(.08,.45,p));shins.forEach(s=>s.visible=p>.8);}
  debris.forEach((l,i)=>{l.visible=n===1||n>=2;l.position.y=.055+i*.018;});
  const raining=n<5&&!(n===2&&reached('drain',phase>.78));
  rain.forEach((r,i)=>{r.visible=raining;r.position.y=1.4+(((i*.193-local*.8)%1+1)%1)*4.6;});
  route(roofFlow,t,gutter.visible&&raining);
  route(downFlow,t,n===2&&!reached('bypass',phase>.5));
  route(inFlow,t,tank.visible&&raining&&(n!==2||reached('bypass',phase>.42)));
  route(dustFlow,t,n===1&&reached('dust',phase>.5));
  route(overflowFlow,t,n===4&&overflow.visible);route(drainFlow,t,n===2&&reached('drain',phase>.78),.3);route(tapFlow,t,n===5&&!reached('pour',phase>.2));route(pourFlow,t,pouring);
  // Camera is moved in world space: changes in occlusion and perspective are genuine 3D.
  const shots=[{p:[9,8,13],at:[0,1.6,0],zoom:.83},{p:[6,6,11],at:[-.4,1.2,.4],zoom:1.25},{p:[2,4.2,12],at:[.6,1.65,.7],zoom:2.0},{p:[8,6,11],at:[1.4,1.5,.9],zoom:1.12},{p:[7,7,13],at:[1.75,1,.8],zoom:1.05},{p:[9,8,13],at:[0,1.3,.2],zoom:.87}];
  let shot=shots[n],move=staticMode?1:smooth(phase*3);
  camera.position.set(...shot.p);camera.position.x+=n===2?(1-move)*1.2:(1-move)*.5;camera.lookAt(...shot.at);camera.zoom=shot.zoom*(.97+.03*move);camera.updateProjectionMatrix();
  if(n===5&&!staticMode){let returnWide=progress('sit',1.7);camera.zoom=lerp(1.24,.87,returnWide);camera.lookAt(lerp(.8,0,returnWide),lerp(1.15,1.3,returnWide),lerp(1.3,.2,returnWide));camera.updateProjectionMatrix();}
  renderer.render(scene,camera);
  const title=document.getElementById('scene-title'),label=document.getElementById('scene-label'),section=document.getElementById('section-label');
  if(title&&plan[n]){title.textContent=plan[n].title;label.textContent=plan[n].label;}
  if(section)section.style.opacity=n===2||n===4?'1':'0';
  window.__worldFrame={time:t,scene:n+1,phase,section:n===2||n===4};
}
window.renderWorld=pose;
window.addEventListener('hf-seek',e=>pose(e.detail.time));
pose(window.__hfThreeTime||0);
window.__worldReady=true;
