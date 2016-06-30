import math
import libtcodpy as libtcod

kComponentTypeNone = 0
kComponentTypeBody = 1
kComponentTypeWing = 2
kComponentTypeMainEngine = 3
kComponentTypeSideEngine = 4
kComponentTypeSideWeapon = 5
kComponentTypeSpinalWeapon = 6

body_segments = [10, 178, 179, 186, 193, 194, 197, 202, 203, 206, 207, 208, 209, 210, 215, 216, 219, 220, 223, 240]
body_single_bottom = [179, 194, 197, 209, 216]
body_double_bottom = [186, 203, 206, 210, 215]
body_single_top = [179, 193, 197, 207, 216]
body_double_top = [186, 202, 206, 208, 215]

body_hardpoints_single = [193, 194, 197, 208, 210, 215, 240]
body_hardpoints_double = [202, 203, 206, 207, 209, 216]
body_hardpoints_flat = [10, 178, 219]

wing_segments = {}
wing_segments['a'] = ((221, (0, 'a')), (62, (0, 'a'))) + ((92, (1, 'a'), (0, 'b'), (1, 'a'), (0, 'b'), (0, 'c')), ) * 5
wing_segments['b'] = ((93, (0, 'a'), (1, 'a'), (0, 'b'), (1, 'b'), (0, 'c')), (124, (0, 'a'), (1, 'a'), (0, 'b'), (1, 'b'), (0, 'c')), (222, (0, 'a'), (1, 'a'), (0, 'b'), (1, 'b'), (0, 'c')), (186, (0, 'a'), (1, 'a'), (0, 'b'), (1, 'b'), (0, 'c')))
wing_segments['c'] = ((47, (0, 'a'), (-1, 'c')), )

wing_reflections = {221: 222, 62: 60, 92: 47, 93: 91, 124: 124, 222: 221, 186: 186, 47: 92, 0: 0}

wing_backs_single = [193, 194, 196, 197, 208, 210, 215, 219, 220, 223]
wing_backs_double = [202, 203, 205, 206, 207, 209, 216, 219, 220, 223]

for back in wing_backs_single + wing_backs_double: wing_reflections[back] = back # Wing backs are symmetric.

engine_mounts_double = body_double_bottom
engine_mounts_single = body_single_bottom

side_weapons_single = (25, 180, 190, 217)
side_weapons_double = (157, 182, 185, 188, 189)
# weapons_missile = (23, 24)
front_weapons_single = (25, 179)
front_weapons_double = (157, 186, 215)
projectiles_single = (46, 58, 124, 249, 250)
projectiles_double = (7, 22, 34, 42, 94, 240, 247)

shot_colors = [libtcod.red, libtcod.flame, libtcod.azure, libtcod.green]

weapon_reflections = {180: 195, 190: 212, 217: 192, 182: 199, 185: 204, 188: 200, 189: 211}
for weapon in side_weapons_single + side_weapons_double + front_weapons_single + front_weapons_double:
	if weapon not in weapon_reflections:
		weapon_reflections[weapon] = weapon

color_schemes = ((libtcod.light_orange, libtcod.dark_orange), (libtcod.dark_grey, libtcod.silver), (libtcod.darker_green, libtcod.gold), (libtcod.lighter_azure, libtcod.light_azure), (libtcod.silver, libtcod.desaturated_blue), (libtcod.dark_violet, libtcod.darker_violet), (libtcod.light_sepia, libtcod.sepia))

r = libtcod.random_new()

class Component(object):
	def __init__(self, shape):
		self.shape = shape
		self.type = kComponentTypeNone
	
	def draw(self, con, x_origin = 0, y_origin = 0):
		for y, row in enumerate(self.shape):
			for x, cell in enumerate(row):
				libtcod.console_put_char(con, x + x_origin, y + y_origin, cell)

class BodyComponent(Component):
	def __init__(self, shape):
		super(BodyComponent, self).__init__(shape)
		self.type = kComponentTypeBody
		self.engine_double = (self.shape[-1][0] in engine_mounts_double)
		self.engine_single = (self.shape[-1][0] in engine_mounts_single)
	
	def draw(self, con, x_origin = 0, y_origin = 0):
		super(BodyComponent, self).draw(con, x_origin, y_origin)
		if self.engine_single:
			for y in range(7):
				libtcod.console_put_char(con, x_origin, len(self.shape) + y + y_origin, 179)
				libtcod.console_set_char_foreground(con, x_origin, len(self.shape) + y + y_origin, libtcod.red * (1.0 / (y+1)))
		elif self.engine_double:
			for y in range(7):
				libtcod.console_put_char(con, x_origin, len(self.shape) + y + y_origin, 186)
				libtcod.console_set_char_foreground(con, x_origin, len(self.shape) + y + y_origin, libtcod.red * (1.0 / (y+1)))

class WingComponent(Component):
	def __init__(self, shape, engines_single, engines_double, weapons):
		super(WingComponent, self).__init__(shape)
		self.type = kComponentTypeWing
		self.engines_single = engines_single
		self.engines_double = engines_double
		self.weapons = weapons
	def reversed(self):
		return WingComponent([[wing_reflections[cell] for cell in reversed(row)] for row in self.shape], [len(self.shape[0]) - x - 1 for x in self.engines_single], [len(self.shape[0]) - x - 1 for x in self.engines_double], [(w[0].reversed(), len(self.shape[0]) - w[1] - 1, w[2]) for w in self.weapons])
	
	def draw(self, con, x_origin = 0, y_origin = 0):
		super(WingComponent, self).draw(con, x_origin, y_origin)
		for engine in self.engines_single:
			for y in range(5):
				libtcod.console_put_char(con, engine + x_origin, len(self.shape) + y + y_origin, 179)
				libtcod.console_set_char_foreground(con, engine + x_origin, len(self.shape) + y + y_origin, libtcod.red * (1.0 / (y+1)))
		for engine in self.engines_double:
			for y in range(5):
				libtcod.console_put_char(con, engine + x_origin, len(self.shape) + y + y_origin, 186)
				libtcod.console_set_char_foreground(con, engine + x_origin, len(self.shape) + y + y_origin, libtcod.red * (1.0 / (y+1)))
		for weapon in self.weapons:
			weapon[0].draw(con, x_origin + weapon[1], y_origin + weapon[2])

class WeaponComponent(Component):
	def __init__(self, shape, projectile, projectile_color):
		super(WeaponComponent, self).__init__(shape)
		self.type = kComponentTypeSideWeapon
		self.projectile = projectile
		self.projectile_color = projectile_color
	def reversed(self):
		return WeaponComponent([[weapon_reflections[cell] for cell in reversed(row)] for row in self.shape], self.projectile, self.projectile_color)
	def draw(self, con, x_origin = 0, y_origin = 0):
		super(WeaponComponent, self).draw(con, x_origin, y_origin)
		for y in range(1, 5):
			libtcod.console_put_char(con, x_origin, - y + y_origin, self.projectile)
			libtcod.console_set_char_foreground(con, x_origin, - y + y_origin, self.projectile_color)

def generate_body():
	next_single = False
	next_double = False
	body_shape = []
	for i in range(libtcod.random_get_int(r, 3, 7)):
		idx = libtcod.random_get_int(r, 0, len(body_segments) - 1)
		while (next_single and body_segments[idx] in body_double_top) or (next_double and body_segments[idx] in body_single_top):
			idx = libtcod.random_get_int(r, 0, len(body_segments) - 1)
		body_shape.append([body_segments[idx]])
		next_single = (body_segments[idx] in body_single_bottom)
		next_double = (body_segments[idx] in body_double_bottom)
	return BodyComponent(body_shape)

def generate_wing(body):
	height = len(body.shape)
	wing_shape = [[0 for x in range(height)] for y in range(height)]
	x = 0
	next = 'a'
	hardpoints = []
	for y in range(height):
		idx = libtcod.random_get_int(r, 0, len(wing_segments[next]) - 1)
		wing_shape[y][x] = wing_segments[next][idx][0]
		idx_next = libtcod.random_get_int(r, 1, len(wing_segments[next][idx]) - 1)
		print wing_segments[next][idx]
		last_x = x
		dx = wing_segments[next][idx][idx_next][0]
		x += dx
		next = wing_segments[next][idx][idx_next][1]
		if dx == 1 and y + 1 < height:
			valid = True
			for y_check in range(y):
				if wing_shape[y_check][x] != 0:
					valid = False
			if valid:
				hardpoints.append((x, y))
		if x == -1:
			x = 0
			next = 'a'
	if not hardpoints:
		weapons = [(generate_weapon_front(), 0, -1)]
	else:
		weapons = [(generate_weapon_side(), hp[0], hp[1]) for hp in hardpoints]
	idx = libtcod.random_get_int(r, 0, 1)
	if idx:
		backs = wing_backs_single
	else:
		backs = wing_backs_double
	if body.shape[-1][0] in body_hardpoints_single:
		backs = wing_backs_single
	elif body.shape[-1][0] in body_hardpoints_double:
		backs = wing_backs_double
	engines_single = []
	engines_double = []
	for x_back in range(last_x):
		wing_shape[-1][x_back] = backs[libtcod.random_get_int(r, 0, len(backs) - 1)]
		if wing_shape[-1][x_back] in body_single_bottom:
			engines_single.append(x_back)
		elif wing_shape[-1][x_back] in body_double_bottom:
			engines_double.append(x_back)
	return WingComponent(wing_shape, engines_single, engines_double, weapons)

def generate_weapon_side():
	if libtcod.random_get_int(r, 0, 1) == 1:
		return WeaponComponent([[side_weapons_single[libtcod.random_get_int(r, 0, len(side_weapons_single) - 1)]]], projectiles_single[libtcod.random_get_int(r, 0, len(projectiles_single) - 1)], shot_colors[libtcod.random_get_int(r, 0, len(shot_colors) - 1)])
	else:
		return WeaponComponent([[side_weapons_double[libtcod.random_get_int(r, 0, len(side_weapons_double) - 1)]]], projectiles_double[libtcod.random_get_int(r, 0, len(projectiles_double) - 1)], shot_colors[libtcod.random_get_int(r, 0, len(shot_colors) - 1)])

def generate_weapon_front():
	if libtcod.random_get_int(r, 0, 1) == 1:
		return WeaponComponent([[front_weapons_single[libtcod.random_get_int(r, 0, len(front_weapons_single) - 1)]]], projectiles_single[libtcod.random_get_int(r, 0, len(projectiles_single) - 1)], shot_colors[libtcod.random_get_int(r, 0, len(shot_colors) - 1)])
	else:
		return WeaponComponent([[front_weapons_double[libtcod.random_get_int(r, 0, len(front_weapons_double) - 1)]]], projectiles_double[libtcod.random_get_int(r, 0, len(projectiles_double) - 1)], shot_colors[libtcod.random_get_int(r, 0, len(shot_colors) - 1)])

for i in range(20):
	con = libtcod.console_new(30, 30)
	libtcod.console_set_custom_font('cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
	libtcod.console_init_root(30, 30, 'Spaceship Generator', False)
	body = generate_body()
	h = len(body.shape)
	wing = generate_wing(body)
	if len(wing.engines_single) + len(wing.engines_double) == 0 and not body.engine_single and not body.engine_double:
		body.shape.append([206])
		body.engine_double = True
	colors = color_schemes[libtcod.random_get_int(r, 0, len(color_schemes) - 1)]
	libtcod.console_set_default_foreground(con, colors[0])
	wing.reversed().draw(con, 0, 8)
	wing.draw(con, h + 1, 8)
	libtcod.console_set_default_foreground(con, colors[1])
	body.draw(con, h, 8)
	libtcod.console_blit(con, 0, 0, 30, 30, 0, 0, 0)
	libtcod.console_flush()
	libtcod.sys_save_screenshot(None)
	libtcod.console_wait_for_keypress(True)