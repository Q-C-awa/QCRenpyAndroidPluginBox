init python:
    import pygame
    import math
    
    renpy.register_shader("white_round", 
        variables="""
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform float u_stroke_width;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
        """,
        vertex_100="""
            v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
            precision highp float;
            
            vec2 uv = v_tex_coord;
            vec2 center = vec2(0.5, 0.5);
            float dist = distance(uv, center);
            if(dist <= u_radius) {
                gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
            else if(dist <= u_radius + u_stroke_width) {
                gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
            }
            else {
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            }
        """)
    
    renpy.register_shader("color_round_picker", variables="""
        uniform vec2 u_model_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_100="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        precision highp float;
        vec2 uv = v_tex_coord;
        vec2 center = vec2(0.5, 0.5);
        float dist = distance(uv, center);
        float outer_radius = 0.49;
        float inner_radius = 0.38;
        
        if(dist >= inner_radius && dist <= outer_radius) {
            float angle = atan(center.y - uv.y , center.x - uv.x); 
            float hue = (angle + 3.141592653589793) / (2.0 * 3.141592653589793);
            float h = hue * 6.0;
            int i = int(floor(h));
            float f = h - float(i);
            float p = 0.0;
            float q = 1.0 - f;
            float t = f;
            
            if (i == 0) {
                gl_FragColor = vec4(1.0, t, p, 1.0);
            } else if (i == 1) {
                gl_FragColor = vec4(q, 1.0, p, 1.0);
            } else if (i == 2) {
                gl_FragColor = vec4(p, 1.0, t, 1.0);
            } else if (i == 3) {
                gl_FragColor = vec4(p, q, 1.0, 1.0);
            } else if (i == 4) {
                gl_FragColor = vec4(t, p, 1.0, 1.0);
            } else {
                gl_FragColor = vec4(1.0, p, q, 1.0);
            }
        } else {
            gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
        }
    """)
    class ColorPicker(renpy.Displayable):
        def __init__(self, width=800, height=800, xpos=0.5, ypos=0.5, color_picker_zoom=1.0, step=6, **kwargs):
            super(ColorPicker, self).__init__(**kwargs)
            self.color_picker_zoom = color_picker_zoom
            self.width = int(width * color_picker_zoom)
            self.height = int(height * color_picker_zoom)
            self.xpos = xpos
            self.ypos = ypos
            
            # 计算位置
            screen_width, screen_height = renpy.get_physical_size()
            self.actual_x = int(self.xpos * (screen_width - self.width))
            self.actual_y = int(self.ypos * (screen_height - self.height))
            
            # 圆环参数
            self.center_x = self.width // 2
            self.center_y = self.height // 2
            base_radius = min(width, height) // 2
            self.outer_radius = int(base_radius * 0.98 * color_picker_zoom)
            self.inner_radius = int(base_radius * 0.74 * color_picker_zoom)
            self.slider_radius = (self.inner_radius + self.outer_radius) // 2
            
            # 矩形参数
            self.rect_width = int(420 * color_picker_zoom)
            self.rect_height = int(420 * color_picker_zoom)
            self.rect_step = step
            self.rect_x = (self.width - self.rect_width) // 2
            self.rect_y = (self.height - self.rect_height) // 2
            
            # 状态变量
            self.angle = 0.0
            self.slider_rel_x = 0.5
            self.slider_rel_y = 0.5
            self.dragging_ring = False
            self.dragging_rect = False
            self.base_color = Color("#ff0000")
            self.final_color = Color("#ff0000")
            self.rect_colors_cache = None
            self.cache_base_color = None
            
        def get_hue_color(self, angle):
            """根据角度获取HSV颜色空间的颜色"""
            hue = angle / (2 * math.pi)
            return Color(hsv=(hue, 1.0, 1.0))
            
        def get_rect_color_at_position(self, x, y):
            """获取矩形中指定位置的颜色"""
            u = max(0.0, min(1.0, x / float(self.rect_width - 1) if self.rect_width > 1 else 0))
            v = max(0.0, min(1.0, y / float(self.rect_height - 1) if self.rect_height > 1 else 0))
            
            saturation = u
            brightness = 1.0 - v
            gray = Color(rgb=(brightness, brightness, brightness))
            pure_color = self.base_color.multiply_value(brightness)
            
            return gray.interpolate(pure_color, saturation)
            
        def precompute_rect_colors(self):
            """预计算"""
            if self.rect_colors_cache is not None and self.cache_base_color == self.base_color:
                return self.rect_colors_cache
                
            colors = {}
            for x in range(0, self.rect_width, self.rect_step):
                for y in range(0, self.rect_height, self.rect_step):
                    colors[(x, y)] = self.get_rect_color_at_position(x, y)
            
            self.rect_colors_cache = colors
            self.cache_base_color = self.base_color
            return colors
            
        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            # 更新基色
            self.base_color = self.get_hue_color(self.angle)
            # 渲染圆环
            ring_display = Transform(Solid("#ffffff"), 
                                shader="color_round_picker", 
                                mesh=True,
                                xsize=self.width, 
                                ysize=self.height)
            ring_render = renpy.render(ring_display, width, height, st, at)
            render.blit(ring_render, (self.actual_x, self.actual_y))
            # 渲染矩形
            rect_colors = self.precompute_rect_colors()
            for (x, y), color in rect_colors.items():
                rect_width = min(self.rect_step, self.rect_width - x)
                rect_height = min(self.rect_step, self.rect_height - y)
                color_rect = Solid(color, xsize=rect_width, ysize=rect_height)
                color_render = renpy.render(color_rect, width, height, st, at)
                render.blit(color_render, (self.actual_x + self.rect_x + x, self.actual_y + self.rect_y + y))
            # 最终颜色
            self.final_color = self.get_rect_color_at_position(
                self.slider_rel_x * self.rect_width,
                self.slider_rel_y * self.rect_height
            )
            # 渲染圆环滑块
            # 这里可以调圆快和圆环的相对位置
            ring_slider_x = self.actual_x + self.center_x + (self.slider_radius+5) * math.cos(self.angle)
            ring_slider_y = self.actual_y + self.center_y + (self.slider_radius) * math.sin(self.angle)
            self._render_ring_slider(render, ring_slider_x, ring_slider_y, 
                            int(min(self.width, self.height) * 0.15 * self.color_picker_zoom),
                            width, height, st, at)
            
            # 渲染矩形滑块
            rect_slider_x = self.actual_x + self.rect_x + (self.slider_rel_x * self.rect_width)
            rect_slider_y = self.actual_y + self.rect_y + (self.slider_rel_y * self.rect_height)
            self._render_slider(render, rect_slider_x, rect_slider_y,
                            int(min(self.width, self.height) * 0.05 * self.color_picker_zoom),
                            width, height, st, at)
            
            renpy.redraw(self, 0.05)
            return render
            
        def _render_ring_slider(self, render, x, y, size, width, height, st, at):
            """渲染圆环滑块"""
            slider_pos_x = x - size // 2
            slider_pos_y = y - size // 2
            
            # 使用白色圆形着色器
            slider_display = Transform(Solid("#ffffff"), 
                                    shader="white_round", 
                                    mesh=True,
                                    xsize=size, 
                                    ysize=size,
                                    u_radius=0.45,
                                    u_stroke_width=0.025)
            slider_render = renpy.render(slider_display, width, height, st, at)
            render.blit(slider_render, (slider_pos_x, slider_pos_y))
            
        def _render_slider(self, render, x, y, size, width, height, st, at):
            """渲染滑块"""
            slider_pos_x = x - size // 2
            slider_pos_y = y - size // 2
            
            # 黑色边框
            slider_border = Solid("#000000", xsize=size, ysize=size)
            slider_border_render = renpy.render(slider_border, width, height, st, at)
            render.blit(slider_border_render, (slider_pos_x, slider_pos_y))
            
            # 白色内部
            inner_size = size - 4
            inner_pos_x = slider_pos_x + 2
            inner_pos_y = slider_pos_y + 2
            slider_inner = Solid("#FFFFFF", xsize=inner_size, ysize=inner_size)
            slider_inner_render = renpy.render(slider_inner, width, height, st, at)
            render.blit(slider_inner_render, (inner_pos_x, inner_pos_y))
            
        def event(self, ev, x, y, st):
            # 更新实际位置
            screen_width, screen_height = renpy.get_physical_size()
            self.actual_x = int(self.xpos * (screen_width - self.width))
            self.actual_y = int(self.ypos * (screen_height - self.height))
            
            local_x = x - self.actual_x
            local_y = y - self.actual_y
            
            # 圆环拖动
            if self._is_in_ring(local_x, local_y):
                self._handle_ring_event(ev, local_x, local_y)
            
            # 矩形拖动
            if self._is_in_rect(x, y):
                self._handle_rect_event(ev, x, y)
                
            return None
            
        def _is_in_ring(self, x, y):
            """检查是否在圆环内"""
            dx = x - self.center_x
            dy = y - self.center_y
            distance = math.sqrt(dx*dx + dy*dy)
            return self.inner_radius <= distance <= self.outer_radius
            
        def _is_in_rect(self, x, y):
            """检查是否在矩形内"""
            rect_actual_x = self.actual_x + self.rect_x
            rect_actual_y = self.actual_y + self.rect_y
            return (rect_actual_x <= x <= rect_actual_x + self.rect_width and 
                    rect_actual_y <= y <= rect_actual_y + self.rect_height)
            
        def _handle_ring_event(self, ev, local_x, local_y):
            dx = local_x - self.center_x
            dy = local_y - self.center_y
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
                
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.angle = angle
                self.dragging_ring = True
                renpy.restart_interaction()
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.dragging_ring = False
            elif ev.type == pygame.MOUSEMOTION and self.dragging_ring:
                self.angle = angle
                renpy.restart_interaction()
                
        def _handle_rect_event(self, ev, x, y):
            rect_actual_x = self.actual_x + self.rect_x
            rect_actual_y = self.actual_y + self.rect_y
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                rel_x = (x - rect_actual_x) / self.rect_width
                rel_y = (y - rect_actual_y) / self.rect_height
                self.slider_rel_x = max(0.0, min(1.0, rel_x))
                self.slider_rel_y = max(0.0, min(1.0, rel_y))
                self.dragging_rect = True
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.dragging_rect = False
            elif ev.type == pygame.MOUSEMOTION and self.dragging_rect:
                rel_x = (x - rect_actual_x) / self.rect_width
                rel_y = (y - rect_actual_y) / self.rect_height
                self.slider_rel_x = max(0.0, min(1.0, rel_x))
                self.slider_rel_y = max(0.0, min(1.0, rel_y))
                renpy.restart_interaction()
            
        def visit(self):
            return []
            
        def get_final_color(self):
            return self.final_color.hexcode

default color_picker_width = 800  # 分辨率设置 一般情况不建议大于850
default color_picker_height = color_picker_width 
default color_picker_zoom = 0.8  # 大小设置
default color_picker_step = 5  # 精度控制，一般情况不建议小于5
ColorPicker(
        width=color_picker_width,
        height=color_picker_height,
        xpos=0.5, # 位置设置
        ypos=0.5,
        color_picker_zoom=color_picker_zoom,
        step=color_picker_step
    )