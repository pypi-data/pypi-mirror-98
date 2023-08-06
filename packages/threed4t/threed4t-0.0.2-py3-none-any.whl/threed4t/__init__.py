
from ursina import *
from ursina.shaders import lit_with_shadows_shader, normals_shader

from . import common
from .engine import Engine3D
from .mouse4t import Mouse4T
from .sequence4t import 動畫組合
from .audio4t import 載入聲音


模擬3D引擎 = Engine3D

__all__ = [ 
            '模擬3D引擎', 'Entity', 'EditorCamera', '載入聲音',
            '模擬進行中','模擬主迴圈', 'color','Vec3','Vec4','Vec2',
            '按住的鍵', '滑鼠','天空', '新增立方體', '新增6面貼圖方塊',
            '新增內面貼圖球體','新增球體', '新增物體', '新增平面',
            '預約執行', '新增文字', '新增立方體線框', '新增4面體線框',
            '動畫組合', '動作', '光影著色器', '法線著色器',
            ]


Text.default_font = common.msjh_font_path
print('字形設定: ', Text.default_font)

# shader
光影著色器 = lit_with_shadows_shader
法線著色器 = normals_shader

#動畫組合 = Sequence
動作 = Func


按住的鍵 = held_keys
滑鼠 = Mouse4T()
天空 = Sky
######## top level function
# import __main__
# __main__.按住的鍵 = held_keys


def simulate():
    if not common.is_engine_created:
        Engine3D()

    common.stage.simulate()


模擬主迴圈 = simulate
模擬進行中 = simulate

######## top level function

def add_cube(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cube(*args, **kwargs)
新增立方體 = add_cube

def add_cube_line(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cube_line(*args, **kwargs)
新增立方體線框 = add_cube_line

def add_tetrahedron_line(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_tetrahedron_line(*args, **kwargs)
新增4面體線框 = add_tetrahedron_line


def add_entity(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_entity(*args, **kwargs)
新增物體 = add_entity

def add_sphere(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_sphere(*args, **kwargs)
新增球體 = add_sphere

def add_quad(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_quad(*args, **kwargs)
新增平面 = add_quad


def add_cubic6(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_cubic6(*args, **kwargs)
新增6面貼圖方塊 = add_cubic6

def add_sphere_inward(*args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    return common.stage.add_sphere_inward(*args, **kwargs)
新增內面貼圖球體 = add_sphere_inward

def add_text(文字, *args, **kwargs):
    if not common.is_engine_created:
        Engine3D()
    kwargs['text'] = 文字
    return common.stage.add_text(*args, **kwargs)
新增文字 = add_text



def 預約執行(函式, *args, 時間=1, **kwargs):
    kwargs['delay'] = 時間
    invoke(函式, *args, **kwargs)



if __name__ == '__main__' :
    pass
    
