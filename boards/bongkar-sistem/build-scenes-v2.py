"""Bongkar Sistem v2: full-environment, material-led static identity studies.
Original illustrative geometry, not engineering drawings or an episode revision.
Run Blender background --factory-startup --python this-file -- wide contact overhead.
"""
from pathlib import Path
import bpy, math, random, sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'assets'/'renders-v2'; OUT.mkdir(parents=True,exist_ok=True)
M={}; random.seed(225)
COLORS={'ink':'#173B42','paper':'#F8F4E8','cream':'#E8E2D3','plaster':'#C6C1AD',
 'roof':'#8F5140','tile':'#A66750','grass':'#52684A','leaf':'#486849','leaf2':'#6A8052',
 'soil':'#75604A','concrete':'#9D9B91','stone':'#696B64','steel':'#8E9997',
 'teal':'#3C6261','dark':'#283C3D','water':'#4292AA','yellow':'#CCA84F',
 'wood':'#65513E','skin':'#AB8567','white':'#E9E7DC','glass':'#69878C'}
def rgba(h):
 h=h.lstrip('#');v=[int(h[i:i+2],16)/255 for i in (0,2,4)]
 return tuple(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v)+(1,)
def mat(key):
 if key in M:return M[key]
 m=bpy.data.materials.new(key);m.use_nodes=True;nodes=m.node_tree.nodes;links=m.node_tree.links
 bs=nodes.get('Principled BSDF');base=rgba(COLORS[key]);bs.inputs['Base Color'].default_value=base
 bs.inputs['Roughness'].default_value=.25 if key in ['water','glass'] else .7
 bs.inputs['Metallic'].default_value=.65 if key=='steel' else .1 if key=='teal' else 0
 if key=='water':bs.inputs['Coat Weight'].default_value=.4
 if key not in ['water','glass','skin','yellow']:
  geo=nodes.new('ShaderNodeNewGeometry');noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=16 if key in ['plaster','concrete','soil'] else 7
  links.new(geo.outputs['Position'],noise.inputs['Vector']);ramp=nodes.new('ShaderNodeValToRGB')
  ramp.color_ramp.elements[0].color=tuple(x*.65 for x in base[:3])+(1,);ramp.color_ramp.elements[1].color=tuple(min(x*1.18,1) for x in base[:3])+(1,)
  links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
  bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.015 if key in ['concrete','soil'] else .003
  links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],bs.inputs['Normal'])
 M[key]=m;return m
def finish(o,key):o.data.materials.append(mat(key));return o
def box(name,loc,size,key,bevel=.008):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);finish(o,key)
 if bevel:
  b=o.modifiers.new('Real edge radius','BEVEL');b.width=bevel;b.segments=2
  o.modifiers.new('Corner normals','WEIGHTED_NORMAL')
 return o
def rod(name,a,b,r,key,vertices=24):
 a,b=Vector(a),Vector(b);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(a+b)/2)
 o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();finish(o,key)
 for p in o.data.polygons:p.use_smooth=True
 return o
def ball(name,loc,scale,key):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=10,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;finish(o,key)
 for p in o.data.polygons:p.use_smooth=True
 return o
def ring(name,loc,r,minor,key,rotation=(0,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=minor,major_segments=48,minor_segments=8,location=loc,rotation=rotation)
 o=bpy.context.object;o.name=name;finish(o,key);return o
def pipe(name,points,r,key):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3
 s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,co in zip(s.points,points):p.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);finish(o,key);return o
def leaf_tree(x,y,h=6):
 rod('Tree trunk',(x,y,0),(x+.13,y,h*.64),h*.025,'wood',12)
 for i in range(10):
  angle=i*2.4;px=x+math.cos(angle)*h*.22;py=y+math.sin(angle)*h*.2;pz=h*(.62+random.random()*.28)
  rod('Branch',(x,y,h*.45),(px,py,pz),.04,'wood',8)
  for j in range(9):
   bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=h*.13,location=(px+random.uniform(-.7,.7),py+random.uniform(-.7,.7),pz+random.uniform(-.5,.5)))
   o=bpy.context.object;o.scale=(1,.7,.75);finish(o,'leaf' if j%2 else 'leaf2')
   for face in o.data.polygons:face.use_smooth=True
def shrub(x,y,s=1):
 for i in range(9):
  angle=i*2.4;ball('Shrub foliage',(x+math.cos(angle)*s*.35,y+math.sin(angle)*s*.35,s*(.2+random.random()*.4)),(s*.25,s*.21,s*.15),'leaf' if i%2 else 'leaf2')
def plant(x,y,s=1):
 rod('Terracotta pot',(x,y,.05),(x,y,.45*s),.22*s,'roof');ring('Pot rim',(x,y,.45*s),.23*s,.025,'tile')
 for i in range(9):
  a=i*2.4;z=.65*s+random.random()*.35*s;px=x+math.cos(a)*.3*s;py=y+math.sin(a)*.3*s
  rod('Plant stem',(x,y,.42*s),(px,py,z),.008,'leaf',6)
  leaf=ball('Plant leaf',(px,py,z),(.17*s,.055*s,.018*s),'leaf2');leaf.rotation_euler=(.3,random.uniform(-.6,.6),a)
def house(x,y,s=1,detail=True):
 box('Foundation',(x,y,.12*s),(8.2*s,7.2*s,.24*s),'concrete')
 box('Plaster house',(x,y,1.65*s),(8*s,7*s,3.1*s),'plaster')
 # Roof is thin construction, with tile rows and real eaves rather than a solid toy triangle.
 angle=math.atan2(1.45,4.5);length=math.sqrt(4.5**2+1.45**2)
 for side in [-1,1]:
  roof=box('Roof plane',(x+side*2.25*s,y,3.92*s),(length*s,7.8*s,.08*s),'roof');roof.rotation_euler[1]=side*angle
  if detail:
   for ix in range(12):
    xx=(ix+.5)*4.5/12
    for iy in range(20):
     yy=-3.8+(iy+.5)*7.6/20;tile=box('Individual roof tile',(x+side*xx*s,y+yy*s,(4.65-xx*1.45/4.5+.07)*s),(.415*s,.365*s,.035*s),'tile' if (ix+iy)%4 else 'roof',0)
     tile.rotation_euler[1]=side*angle
 rod('Roof ridge',(x,y-4*s,4.68*s),(x,y+4*s,4.68*s),.08*s,'roof')
 for dx in [-4.1,4.1]:
  box('Eaves fascia',(x+dx*s,y,3.17*s),(.15*s,7.8*s,.17*s),'wood')
 for dx in [-2.3,1.2]:
  box('Front window recess',(x+dx*s,y-3.515*s,1.9*s),(1.6*s,.04*s,1.35*s),'dark')
  box('Front glazing',(x+dx*s,y-3.55*s,1.9*s),(1.42*s,.03*s,1.2*s),'glass')
  for dd in [-.77,0,.77]:box('Window mullion',(x+(dx+dd)*s,y-3.59*s,1.9*s),(.045*s,.05*s,1.35*s),'white',0)
  box('Window sill',(x+dx*s,y-3.62*s,1.2*s),(1.85*s,.2*s,.09*s),'concrete')
 box('Door recess',(x+3*s,y-3.53*s,1.22*s),(1.02*s,.05*s,2.3*s),'dark')
 box('Timber door',(x+3*s,y-3.57*s,1.22*s),(.88*s,.04*s,2.2*s),'wood')
 for yy in [y-1.4*s,y+1.5*s]:
  box('Side glazing',(x+4.02*s,yy,1.9*s),(.04*s,1.35*s,1.25*s),'glass')
  for yoff in [-.7,.7]:box('Side frame',(x+4.06*s,yy+yoff*s,1.9*s),(.04*s,.055*s,1.4*s),'white')
def human(x,y,pose='operate'):
 # Adult proportions, approximately 1.76 m; no oversized eyes or toy joints.
 for side in [-1,1]:
  sx=x+side*.11;box('Work boot',(sx,y-.06,.085),(.16,.3,.17),'dark',.015)
  rod('Trouser lower',(sx,y,.18),(sx,y,.54),.074,'wood')
  rod('Trouser upper',(sx,y,.54),(sx,y,.94),.09,'wood')
 box('Pelvis',(x,y,.94),(.34,.23,.22),'wood',.025)
 body=box('Work shirt',(x,y,1.19),(.43,.28,.43),'teal',.035)
 rod('Neck',(x,y,1.39),(x,y,1.48),.06,'skin')
 ball('Head',(x,y,1.58),(.105,.105,.145),'skin')
 ball('Hardhat shell',(x,y,1.7),(.13,.14,.075),'yellow');ring('Hardhat brim',(x,y,1.66),.15,.012,'yellow')
 for side in [-1,1]:
  a=(x+side*.235,y,1.35);el=(x+side*.35,y-.13,1.13);hand=(x+side*.32,y-.32,1.22 if pose=='operate' else .98)
  rod('Sleeve upper',a,el,.065,'teal');rod('Sleeve lower',el,hand,.05,'teal');ball('Glove',hand,(.052,.065,.055),'cream')
def setup():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True;scene.cycles.max_bounces=4
 scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
 scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
 world=bpy.data.worlds.new('Physical outdoor light');world.use_nodes=True;scene.world=world
 bg=world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=rgba('#C5D5D8');bg.inputs['Strength'].default_value=.55
 bpy.ops.object.light_add(type='SUN');bpy.context.object.data.energy=2.1;bpy.context.object.data.angle=.15;bpy.context.object.rotation_euler=(.45,-.6,-.6)
 bpy.ops.object.light_add(type='AREA',location=(2,-10,15));l=bpy.context.object;l.data.energy=1000;l.data.size=8;l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
 bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='PERSP';cam.data.lens=38;scene.camera=cam
 return scene
def environment():
 # No pedestal or visible plot boundary: world extends far beyond the camera.
 box('Continuous ground',(0,0,-.2),(220,220,.4),'grass',0)
 box('Courtyard',(1,-6,.01),(17,8,.05),'concrete',0)
 for i in range(15):
  for j in range(8):
   if i<4 or j<2:
    box('Courtyard paver',(-6+i*.9,-9.5+j*.8,.06),(.87,.77,.04),'concrete',.005)
 house(-1,1)
 # Roof gutter and connecting route to a full-scale side installation.
 rod('Eaves gutter',(3.3,-3,3.14),(3.3,4.7,3.14),.09,'steel')
 pipe('Roof drain',[(3.3,-3,3.14),(4.15,-3,3.14),(4.5,-2.65,2.7),(4.5,-1.4,2.7)],.065,'cream')
 rod('Tank concrete plinth',(4.6,-.3,0),(4.6,-.3,.2),1.12,'concrete',48)
 rod('Steel storage body',(4.6,-.3,.2),(4.6,-.3,2.85),1,'teal',64)
 for z in [.35,.65,.95,1.25,1.55,1.85,2.15,2.45,2.72]:ring('Tank rolled rib',(4.6,-.3,z),1.01,.018,'teal')
 rod('Tank lid',(4.6,-.3,2.85),(4.6,-.3,2.93),1.04,'dark',64)
 box('Lid handle',(4.6,-.3,2.99),(.34,.06,.08),'steel')
 pipe('Bottom outlet',[(4.65,-1.29,.62),(4.65,-1.6,.62),(4.65,-1.85,.62),(4.65,-1.85,.45)],.055,'steel')
 valve=box('Valve handle',(4.65,-1.55,.77),(.4,.065,.035),'yellow')
 ring('Outlet fitting',(4.65,-1.3,.62),.086,.02,'steel',(math.pi/2,0,0))
 for z in [.62,1.4,2.3]:box('Pipe wall clip',(3.13,-2.65,z),(.1,.16,.04),'steel')
 rod('Vertical diversion chamber',(3.5,-2.9,.35),(3.5,-2.9,2.6),.13,'cream')
 for z in [.45,2.48]:ring('Chamber collar',(3.5,-2.9,z),.15,.025,'cream')
 pipe('Overflow route',[(5.58,-.3,2.5),(5.9,-.3,2.5),(5.9,-.3,.12),(6.8,-.3,.12)],.06,'cream')
 for xx in [-4.5,-2.5,0,2,7]:plant(xx,-6.7,1 if xx<6 else 1.4)
 for yy in [1,3.5,5.5]:shrub(7.6,yy,1.2)
 # Perimeter, street, and inhabited background create full-frame depth.
 box('Perimeter wall',(0,9,.85),(25,.22,1.7),'plaster')
 for xx in range(-12,14,3):box('Wall pier',(xx,9,1),(.32,.45,2),'cream')
 box('Street',(0,13,-.015),(170,5,.06),'stone',0)
 for xx,yy,ss in [(-12,23,.9),(2,23,1.1),(16,25,.9),(-25,25,.8)]:house(xx,yy,ss,False)
 for xx,yy,h in [(-12,7,7),(-7,12,8),(11,10,8),(17,20,10),(-20,25,8),(1,33,12)]:leaf_tree(xx,yy,h)
 for xx in [-14,14]:
  rod('Utility pole',(xx,12,0),(xx,12,8),.11,'wood')
  box('Crossarm',(xx,12,7.5),(2,.1,.1),'wood')
 for yy in [11.5,12,12.5]:pipe('Overhead utility wire',[(-35,yy,7.4),(0,yy,6.8),(35,yy,7.4)],.009,'dark')
 human(2.45,-4.5)
 # Sparse maintenance props, with realistic sizes.
 for x in [1,1.45]:box('Stacked paving repair',(x,-7.9,.12),(.4,.6,.15),'stone')
 box('Tool case',(3.2,-4.9,.2),(.6,.3,.4),'dark',.025)
 return valve
def camera(pos,target,lens=38,dof=False):
 cam=bpy.context.scene.camera;cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 cam.data.dof.use_dof=dof
 if dof:cam.data.dof.focus_distance=(Vector(target)-cam.location).length;cam.data.dof.aperture_fstop=7.1
def water(state):
 if state=='before':return
 if state=='contact':
  for i in range(5):ball('Opening droplets',(4.65+random.uniform(-.035,.035),-1.85,.37-i*.055),(.022,.022,.035),'water')
 else:
  pipe('Visible outlet stream',[(4.65,-1.85,.46),(4.65,-1.85,.24),(4.65,-1.86,.07)],.023,'water')
  for i in range(12):
   a=i*2.4;r=.06+random.random()*.13;ball('Impact splash',(4.65+math.cos(a)*r,-1.86+math.sin(a)*r,.07+random.random()*.06),(.013,.013,.022),'water')
  ball('Wet ground',(4.65,-1.85,.077),(.3,.25,.009),'dark')
def save(name):
 scene=bpy.context.scene;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')))
 bpy.ops.render.render(write_still=True);print('RENDERED_V2='+name,flush=True)
def run(name,reuse=False):
 random.seed(225)
 if reuse:
  scene=bpy.context.scene;valve=next(o for o in scene.objects if o.name.startswith('Valve handle'))
  for o in list(scene.objects):
   if o.name.startswith(('Opening droplets','Visible outlet stream','Impact splash','Wet ground')):bpy.data.objects.remove(o,do_unlink=True)
  scene.render.resolution_x=1080;scene.render.resolution_y=1920;valve.rotation_euler[2]=0
 else:
  scene=setup();valve=environment()
 if name=='wide':camera((11,-16,6.8),(2,-.5,1.4),38);save('world-full')
 elif name=='contact':
  camera((7.3,-5.7,1.65),(4.65,-1.5,.65),52,True);water('after');valve.rotation_euler[2]=math.pi/2;save('contact-detail')
 elif name=='overhead':camera((8,-10,13),(3.2,-1.8,.7),38);save('route-overhead')
 elif name in ['before','touch','after']:
  scene.render.resolution_x=960;scene.render.resolution_y=600
  camera((6.7,-5.5,1.8),(4.65,-1.53,.67),62,True)
  state={'before':'before','touch':'contact','after':'after'}[name];water(state)
  valve.rotation_euler[2]=0 if name=='before' else math.pi/4 if name=='touch' else math.pi/2
  save('action-'+name)
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['wide','contact','overhead','before','touch','after']
 reuse='--reuse' in args
 if reuse:
  args.remove('--reuse');bpy.ops.wm.open_mainfile(filepath=str(OUT/'world-full.blend'))
 for name in args:
  run(name,reuse=reuse);reuse=True
