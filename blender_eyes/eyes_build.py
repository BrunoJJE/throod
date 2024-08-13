import bpy
import random

print("\ntestClean current scene")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

print("Start scene creation")
print("Add an empty cube to attach interactive python script handling to it")
bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))


print("Create materials")

material_01 = bpy.data.materials.new(name="my_material_01")
material_01.use_nodes = True

material_02 = bpy.data.materials.new(name="my_material_02")
material_02.use_nodes = True

material_03 = bpy.data.materials.new(name="my_material_03")
material_03.use_nodes = True

principled_bsdf_node = material_01.node_tree.nodes["Principled BSDF"]
principled_bsdf_node.inputs["Base Color"].default_value = (0.9, 0.2, 0, 1)
principled_bsdf_node.inputs["Metallic"].default_value = 1.0
principled_bsdf_node.inputs["Roughness"].default_value = 0.5

principled_bsdf_node = material_02.node_tree.nodes["Principled BSDF"]
principled_bsdf_node.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
principled_bsdf_node.inputs["Metallic"].default_value = 1.0
principled_bsdf_node.inputs["Roughness"].default_value = 0.1

principled_bsdf_node = material_03.node_tree.nodes["Principled BSDF"]
principled_bsdf_node.inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1)
principled_bsdf_node.inputs["Metallic"].default_value = 1.0
principled_bsdf_node.inputs["Roughness"].default_value = 0.9


print("Build scene")

spacing = 2.2
for x in range(10):
    for y in range(10):
        h = random.random() * 4
        location = (x * spacing, y * spacing, h)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, h))
        active = bpy.context.active_object
        rc = random.random()
        if rc < 0.1:
            active.data.materials.append(material_03)
        elif rc < 0.6:
            active.data.materials.append(material_01)
        else:
            active.data.materials.append(material_02)

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-45, -23, 20), rotation=(1.3, 0, -1), scale=(1, 1, 1))

