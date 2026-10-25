"""Original static 3D identity studies. Run with Blender --background --python.

These are fictional illustrative systems, not validated engineering models.
No external image assets or animation are used. Seeded geometry is reproducible.
"""
from pathlib import Path
import bpy, math, random, sys
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets' / 'renders'
OUT.mkdir(parents=True, exist_ok=True)
random.seed(51)

COLORS = {
 'sky':'#8CCFE8','ink':'#173B42','cream':'#FFF5DE','grass':'#75A954',
 'grasslight':'#A3C76C','earth':'#B77C51','deep':'#875B43','sand':'#D7B286',
 'rock':'#758184','steel':'#9BAFB2','teal':'#178A91','water':'#2B9FCE',
 'warm':'#E56E43','yellow':'#F4C44B','white':'#F7F5EB','dark':'#25494C',
 'skin':'#D9AE85','roof':'#D66B44','trunk':'#855C40',
}

def rgba(h):
    h=h.lstrip('#')
    vals=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals)+(1,)

M={}
def material(key, rough=.7, metal=0, noise=False):
    if key in M:return M[key]
    m=bpy.data.materials.new(key);m.diffuse_color=rgba(COLORS.get(key,key));m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=m.diffuse_color
    bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    if noise:
        ns=m.node_tree.nodes.new('ShaderNodeTexNoise');ns.inputs['Scale'].default_value=24
        geom=m.node_tree.nodes.new('ShaderNodeNewGeometry');m.node_tree.links.new(geom.outputs['Position'],ns.inputs['Vector'])
        bump=m.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.055
        m.node_tree.links.new(ns.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
    M[key]=m;return m

def apply(obj,key):
    obj.data.materials.append(material(key,rough=.35 if key=='steel' else .72,metal=.55 if key=='steel' else 0,noise=key in ['earth','deep','sand','rock']))
    return obj

def cube(name,loc,size,key,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);apply(o,key)
    if bevel:
        b=o.modifiers.new('Soft manufactured edges','BEVEL');b.width=bevel;b.segments=3
        n=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o

def ball(name,loc,scale,key,segments=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=12,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;apply(o,key)
    for p in o.data.polygons:p.use_smooth=True
    return o

def rod(name,a,b,r,key,vertices=18):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();apply(o,key)
    bevel=o.modifiers.new('Rounded lip','BEVEL');bevel.width=min(r*.16,.035);bevel.segments=2
    for p in o.data.polygons:p.use_smooth=True
    return o

def path(name,points,r,key):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.resolution_u=16;curve.bevel_depth=r;curve.bevel_resolution=4
    spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
    for p,co in zip(spline.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(o);apply(o,key);return o

def tree(x,y,s=1):
    rod('Tree trunk',(x,y,0),(x,y,2*s),.12*s,'trunk')
    for ox,oy,oz,r in [(-.35,0,1.9,.8),(.3,.08,2.25,.85),(0,-.1,2.75,.67)]:
        ball('Leaf crown',(x+ox*s,y+oy*s,oz*s),(r*s,.7*s,.7*s),'grasslight')

def cloud(x,y,z,s):
    for ox,oz,r in [(-.7,0,.6),(0,.18,.85),(.7,0,.6)]:ball('Cloud',(x+ox*s,y,z+oz*s),(r*s,.4*s,r*s*.56),'white')

def character(x,y,z=0,s=1,pose='confident',rotation=0):
    before=set(bpy.context.scene.objects)
    def pt(a,b,c):return(x+a*s,y+b*s,z+c*s)
    # One stable identity: yellow cap, teal overalls, cream shirt, dark boots.
    cube('Left boot',pt(-.15,-.08,.12),(.24*s,.43*s,.23*s),'ink',.06*s)
    cube('Right boot',pt(.15,-.08,.12),(.24*s,.43*s,.23*s),'ink',.06*s)
    rod('Left trouser',pt(-.15,0,.23),pt(-.15,0,.7),.115*s,'teal')
    rod('Right trouser',pt(.15,0,.23),pt(.15,0,.7),.115*s,'teal')
    cube('Overalls body',pt(0,0,.92),(.62*s,.4*s,.6*s),'teal',.13*s)
    cube('Overalls pocket',pt(0,-.218,.95),(.22*s,.035*s,.2*s),'yellow',.025*s)
    ball('Head',pt(0,-.005,1.52),(.29*s,.26*s,.32*s),'skin')
    ball('Cap crown',pt(0,0,1.74),(.335*s,.3*s,.19*s),'yellow')
    cube('Cap brim',pt(0,-.2,1.67),(.7*s,.49*s,.075*s),'yellow',.06*s)
    for eye in [-.095,.095]:ball('Eye',pt(eye,-.255,1.54),(.028*s,.016*s,.033*s),'ink',12)
    if pose=='surprise':
        arms=[(-.31,1.12,-.59,1.35),(.31,1.12,.63,1.44)]
        ball('Surprised mouth',pt(0,-.265,1.4),(.045*s,.018*s,.055*s),'ink',12)
    elif pose=='celebrate':arms=[(-.31,1.12,-.62,1.85),(.31,1.12,.63,1.85)]
    elif pose=='wait':arms=[(-.31,1.12,-.45,.87),(.31,1.12,.45,.87)]
    else:arms=[(-.31,1.12,-.48,.79),(.31,1.12,.6,1.25)]
    for a,c,b,d in arms:
        rod('Cream sleeve',pt(a,0,c),pt((a+b)/2,-.035,(c+d)/2),.115*s,'cream')
        rod('Forearm',pt((a+b)/2,-.035,(c+d)/2),pt(b,-.08,d),.085*s,'skin')
        ball('Hand',pt(b,-.08,d),(.1*s,.09*s,.1*s),'skin')
    if rotation:
        bpy.context.view_layer.update()
        from mathutils import Matrix
        transform=Matrix.Translation((x,y,z))@Matrix.Rotation(rotation,4,'Z')@Matrix.Translation((-x,-y,-z))
        for o in set(bpy.context.scene.objects)-before:o.matrix_world=transform@o.matrix_world

def earth(width=11,depth=9,stones=True):
    cube('Deep ground',(0,0,-2.4),(width,depth,1.5),'deep',.03)
    cube('Sandy layer',(0,0,-1.45),(width,depth,.45),'sand',.02)
    cube('Top soil',(0,0,-.65),(width,depth,1.15),'earth',.02)
    cube('Grass turf',(0,0,-.025),(width,depth,.18),'grass',.03)
    if stones:
        for i in range(65):
            x=random.uniform(-width/2+.15,width/2-.15);z=random.uniform(-3.05,-.35)
            ball('Soil pebble',(x,-depth/2-.012,z),(.03+random.random()*.07,.025,.025+random.random()*.04),'sand',12)

def house(x=1,y=1,s=1,cutaway=False):
    def pt(a,b,c):return(x+a*s,y+b*s,c*s)
    cube('Foundation',pt(0,0,.12),(3.5*s,2.9*s,.24*s),'white',.04)
    cube('Rear wall',pt(0,1.1,1.45),(3.2*s,.2*s,2.5*s),'cream',.04)
    cube('Side wall',pt(1.5,0,1.45),(.2*s,2.3*s,2.5*s),'cream',.04)
    if not cutaway:
        cube('House facade',pt(0,-1.12,1.45),(3.2*s,.2*s,2.5*s),'cream',.04)
        cube('Door',pt(-.35,-1.235,.98),(.67*s,.04*s,1.7*s),'teal',.02)
        for wx in [-1, .78]:
            cube('Window frame',pt(wx,-1.26,1.65),(.67*s,.06*s,.9*s),'white',.02)
            cube('Window glass',pt(wx,-1.3,1.65),(.53*s,.03*s,.74*s),'sky',.01)
            cube('Window mullion',pt(wx,-1.32,1.65),(.04*s,.03*s,.76*s),'white',.005)
    # A pitched solid roof with a readable terracotta thickness.
    verts=[(-1.85,-1.55,2.7),(1.85,-1.55,2.7),(0,-1.55,3.8),(-1.85,1.55,2.7),(1.85,1.55,2.7),(0,1.55,3.8)]
    verts=[pt(*v) for v in verts];mesh=bpy.data.meshes.new('Roof mesh');mesh.from_pydata(verts,[],[(0,1,2),(3,5,4),(0,2,5,3),(1,4,5,2),(0,3,4,1)]);mesh.update()
    roof=bpy.data.objects.new('Terracotta roof',mesh);bpy.context.collection.objects.link(roof);apply(roof,'roof')
    if cutaway:
        cube('Room rug',pt(0,-.2,.28),(2.55*s,1.8*s,.06*s),'yellow',.04)
        cube('Sofa seat',pt(.3,.1,.62),(1.65*s,.7*s,.4*s),'teal',.15)
        cube('Sofa back',pt(.3,.46,.97),(1.65*s,.23*s,.65*s),'teal',.12)
        for ax in [-.6,1.2]:cube('Sofa arm',pt(ax,.1,.88),(.2*s,.8*s,.52*s),'teal',.1)
        ball('Cushion',pt(-.18,.23,1.04),(.27*s,.15*s,.25*s),'yellow')

def mosquito(x,y,z,s=1,suitcase=True):
    ball('Mosquito body',(x,y,z),(.11*s,.2*s,.12*s),'ink')
    ball('Mosquito head',(x,y-.2*s,z+.1*s),(.14*s,.13*s,.13*s),'ink')
    for side in [-1,1]:
        wing=ball('Mosquito wing',(x+side*.2*s,y+.04*s,z+.16*s),(.24*s,.1*s,.03*s),'white');wing.rotation_euler[1]=side*.3
        ball('Mosquito eye',(x+side*.07*s,y-.305*s,z+.15*s),(.043*s,.025*s,.048*s),'white',12)
        for k in range(3):rod('Mosquito leg',(x+side*.06*s,y+(k-1)*.1*s,z-.04*s),(x+side*.26*s,y+(k-1)*.18*s,z-.3*s),.015*s,'ink',8)
    rod('Mosquito proboscis',(x,y-.29*s,z+.03*s),(x,y-.55*s,z-.06*s),.012*s,'ink',8)
    if suitcase:
        cube('Tiny traveller suitcase',(x+.4*s,y-.05*s,z-.26*s),(.3*s,.17*s,.37*s),'warm',.035*s)
        path('Suitcase handle',[(x+.34*s,y-.05*s,z-.07*s),(x+.34*s,y-.05*s,z+.02*s),(x+.46*s,y-.05*s,z+.02*s),(x+.46*s,y-.05*s,z-.07*s)],.014*s,'ink')

def setup(name,location,target,scale,res=(1080,1920)):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
    scene.cycles.use_denoising=True;scene.cycles.max_bounces=5
    scene.render.resolution_x=res[0];scene.render.resolution_y=res[1];scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.world.color=(.4,.4,.4);scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=rgba(COLORS['sky']);bg.inputs['Strength'].default_value=.65
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
    bpy.ops.object.light_add(type='AREA',location=(-5,-7,13));light=bpy.context.object;light.name='Large warm daylight';light.data.energy=2100;light.data.shape='DISK';light.data.size=7
    light.rotation_euler=(Vector((0,0,0))-light.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.light_add(type='AREA',location=(7,2,7));bpy.context.object.data.energy=1000;bpy.context.object.data.size=9
    bpy.context.object.rotation_euler=(Vector((0,0,1))-bpy.context.object.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.object.camera_add(location=location);cam=bpy.context.object;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;cam.data.lens=48;scene.camera=cam
    scene.render.filepath=str(OUT/(name+'.png'));return scene

def render(name):
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')))
    bpy.ops.render.render(write_still=True)
    print('STUDY_RENDERED='+name,flush=True)

def rail():
    setup('world-rail',(12,-20,13),(0,0,.2),18)
    earth(12,11)
    # Rails form a continuous route, rather than a decorative diagram.
    for x in [-1,1]:
        cube('Rail web',(x,.2,.22),(.1,10,.3),'steel',.025)
        cube('Rail head',(x,.2,.39),(.23,10,.11),'steel',.03)
        cube('Rail foot',(x,.2,.1),(.33,10,.09),'dark',.02)
    for y in [1.4,2.25,3.1,3.95,4.8]:cube('Sleeper',(0,y,.1),(3.5,.32,.2),'sand',.02)
    # The front cart has a comic load; the model is an illustration, not a force simulation.
    cart=cube('Cart deck',(0,-1.1,.92),(2.9,2.05,.3),'warm',.09);cart.rotation_euler[1]=-.07
    for x in [-1,1]:
        for y in [-1.65,-.6]:
            rod('Cart wheel',(x-.12,y,.57),(x+.12,y,.57),.37,'ink',24)
            rod('Wheel hub',(x-.14,y,.57),(x+.14,y,.57),.12,'steel',24)
    for k in range(4):cube('Overconfident stack of cargo',(0,-1.05,1.35+k*.62),(1.5-k*.07,1.35,.58),'yellow' if k%2 else 'cream',.08)
    character(-2.65,-1.95,s=1.05,pose='surprise',rotation=-.1)
    house(-3.6,3.6,.55)
    tree(3.7,3.2,.95);tree(-4.5,1.2,.65)
    for i in range(65):
        x=random.choice([-1,1])*random.uniform(2.2,5.7);y=random.uniform(-4.8,5)
        rod('Grass blade',(x,y,.06),(x+.03,y,.18+random.random()*.14),.012,'grasslight',5)
    cloud(-4,5,6.5,1.1);cloud(4,8,5.5,1.4)
    render('world-rail')

def section():
    setup('section-house',(8,-22,11),(0,-.3,.15),17.3)
    earth(11,8)
    house(1.15,1.1,.91,cutaway=True)
    tree(-3.9,2.5,.9);tree(4.2,2.6,.72)
    # Open half-cylinder exposes the route; colored beads are diagram notation.
    pts=[(-2.8,-3.93,1.5),(-2.8,-3.93,-1.3),(-2.65,-3.93,-1.55),(2.3,-3.93,-1.55),(2.55,-3.93,-1.3),(2.55,-3.93,.65)]
    path('Exposed pipe shell',pts,.23,'cream')
    path('Visible inner channel',[(x,y-.15,z) for x,y,z in pts],.14,'dark')
    for i in range(25):
        t=i/24;x=-2.58+t*4.8
        ball('Schematic airflow bead',(x,-4.32,-1.55),(.075,.06,.075),'warm' if t<.38 else 'water',12)
    for z in [-.95,-.45,.1,.65,1.2]:ball('Incoming air marker',(-2.8,-4.32,z),(.075,.06,.075),'warm',12)
    for z in [-1.03,-.5,0,.5]:ball('Outlet air marker',(2.55,-4.32,z),(.075,.06,.075),'water',12)
    path('Connection into the room',[(2.55,-3.93,.65),(2.55,-.15,.65),(2.1,-.15,.65)],.22,'cream')
    cube('Intake cap',(-2.8,-3.93,1.7),(.92,.7,.14),'teal',.05)
    rod('Intake post',(-2.8,-3.93,1.5),(-2.8,-3.93,1.72),.08,'steel')
    character(-1.9,-.8,s=.8,pose='confident',rotation=-.2)
    cloud(-4,5,6.5,1.3);cloud(4,7,5.4,1)
    render('section-house')

def comedy():
    setup('comedy-visitor',(9,-18,10),(0,-.2,.8),13.6)
    earth(9,7)
    house(1.25,1.25,.79,cutaway=True)
    tree(-3.2,2.1,.8)
    # A deliberately visible human setup and an absurd traveller payoff.
    cube('Deck chair seat',(-1.35,-1.5,.55),(1.2,1.3,.17),'cream',.09)
    back=cube('Deck chair back',(-1.35,-.92,1.12),(1.2,.15,1.1),'cream',.07);back.rotation_euler[0]=-.18
    for x in [-1.85,-.85]:
        rod('Chair leg',(x,-1.95,.02),(x,-.9,.72),.055,'trunk')
        rod('Chair leg',(x,-1,.02),(x,-1.9,.62),.055,'trunk')
    character(-1.45,-2.2,s=1.05,pose='surprise',rotation=-.12)
    # Mosquitoes are theatrical characters, not literal scale or biological diagrams.
    mosquito(1.15,-2.05,2.35,1.85)
    mosquito(2.7,-1.8,2.7,1.1)
    mosquito(3.1,-1.5,2, .7)
    cube('Welcome mat',(0,-.6,.13),(1.2,.6,.06),'yellow',.04)
    rod('Foreground pipe opening',(-3.05,-2.8,.12),(-3.05,-2.8,1.2),.25,'cream',24)
    cloud(-3.5,5,6.3,1);cloud(4.5,6,5.8,1.1)
    render('comedy-visitor')

def cast():
    setup('character-poses',(0,-20,7),(0,0,1),12.8,res=(1800,900))
    for i,(x,pose) in enumerate([(-4.1,'confident'),(-1.4,'celebrate'),(1.4,'surprise'),(4.1,'wait')]):
        cube('Pose plinth',(x,0,-.12),(2.25,2,.2),'cream',.12)
        character(x,0,s=1.23,pose=pose)
    render('character-poses')

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    funcs={'rail':rail,'section':section,'comedy':comedy,'cast':cast}
    for name in (args or list(funcs)):funcs[name]()
