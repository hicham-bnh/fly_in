import os, sys
import panda3d

dir = os.path.dirname(panda3d.__file__)
del panda3d

if sys.platform in ('win32', 'cygwin'):
    path_var = 'PATH'
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(dir)
elif sys.platform == 'darwin':
    path_var = 'DYLD_LIBRARY_PATH'
else:
    path_var = 'LD_LIBRARY_PATH'

if not os.environ.get(path_var):
    os.environ[path_var] = dir
else:
    os.environ[path_var] = dir + os.pathsep + os.environ[path_var]

del os, sys, path_var, dir


def _exec_tool(tool):
    import os, sys
    from subprocess import Popen
    tools_dir = os.path.dirname(__file__)
    handle = Popen(sys.argv, executable=os.path.join(tools_dir, tool))
    try:
        try:
            return handle.wait()
        except KeyboardInterrupt:
            # Give the program a chance to handle the signal gracefully.
            return handle.wait()
    except:
        handle.kill()
        handle.wait()
        raise

# Register all the executables in this directory as global functions.
obj2egg = lambda: _exec_tool('obj2egg')
apply_patch = lambda: _exec_tool('apply_patch')
check_adler = lambda: _exec_tool('check_adler')
egg_optchar = lambda: _exec_tool('egg-optchar')
egg_texture_cards = lambda: _exec_tool('egg-texture-cards')
deploy_stub = lambda: _exec_tool('deploy-stub')
egg2c = lambda: _exec_tool('egg2c')
check_crc = lambda: _exec_tool('check_crc')
text_stats = lambda: _exec_tool('text-stats')
pstats = lambda: _exec_tool('pstats')
dae2egg = lambda: _exec_tool('dae2egg')
interrogate = lambda: _exec_tool('interrogate')
check_md5 = lambda: _exec_tool('check_md5')
fltcopy = lambda: _exec_tool('fltcopy')
egg_qtess = lambda: _exec_tool('egg-qtess')
egg_palettize = lambda: _exec_tool('egg-palettize')
pfm_bba = lambda: _exec_tool('pfm-bba')
interrogate_module = lambda: _exec_tool('interrogate_module')
dxf_points = lambda: _exec_tool('dxf-points')
punzip = lambda: _exec_tool('punzip')
egg_crop = lambda: _exec_tool('egg-crop')
lwo2egg = lambda: _exec_tool('lwo2egg')
multify = lambda: _exec_tool('multify')
egg2dxf = lambda: _exec_tool('egg2dxf')
pfm_trans = lambda: _exec_tool('pfm-trans')
pview = lambda: _exec_tool('pview')
egg2flt = lambda: _exec_tool('egg2flt')
build_patch = lambda: _exec_tool('build_patch')
flt_info = lambda: _exec_tool('flt-info')
egg_topstrip = lambda: _exec_tool('egg-topstrip')
egg_rename = lambda: _exec_tool('egg-rename')
egg2bam = lambda: _exec_tool('egg2bam')
parse_file = lambda: _exec_tool('parse_file')
test_interrogate = lambda: _exec_tool('test_interrogate')
x_trans = lambda: _exec_tool('x-trans')
x2egg = lambda: _exec_tool('x2egg')
egg_retarget_anim = lambda: _exec_tool('egg-retarget-anim')
image_info = lambda: _exec_tool('image-info')
egg_mkfont = lambda: _exec_tool('egg-mkfont')
bam2egg = lambda: _exec_tool('bam2egg')
pzip = lambda: _exec_tool('pzip')
vrml_trans = lambda: _exec_tool('vrml-trans')
egg_list_textures = lambda: _exec_tool('egg-list-textures')
pencrypt = lambda: _exec_tool('pencrypt')
flt2egg = lambda: _exec_tool('flt2egg')
vrml2egg = lambda: _exec_tool('vrml2egg')
egg_make_tube = lambda: _exec_tool('egg-make-tube')
dxf2egg = lambda: _exec_tool('dxf2egg')
pdecrypt = lambda: _exec_tool('pdecrypt')
egg2obj = lambda: _exec_tool('egg2obj')
egg_trans = lambda: _exec_tool('egg-trans')
show_ddb = lambda: _exec_tool('show_ddb')
p3dcparse = lambda: _exec_tool('p3dcparse')
make_prc_key = lambda: _exec_tool('make-prc-key')
lwo_scan = lambda: _exec_tool('lwo-scan')
bam_info = lambda: _exec_tool('bam-info')
egg2x = lambda: _exec_tool('egg2x')
flt_trans = lambda: _exec_tool('flt-trans')
image_resize = lambda: _exec_tool('image-resize')
image_trans = lambda: _exec_tool('image-trans')

