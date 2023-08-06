import os
from pickle import load, dump
import dill
import math
import sympy as sp
import numpy as np
from numpy.linalg import norm

from scipy import optimize

ARCLINE_FILE = os.path.join(os.path.dirname(__file__), 'arcline.pkl')
ARCARC_FILE = os.path.join(os.path.dirname(__file__), 'arcarc.pkl')
ARCARC2_FILE = os.path.join(os.path.dirname(__file__), 'arcarc2.pkl')

def get_arc_arc_points2(x_0, y_0, x_1, y_1, x_prev, y_prev, r_0, end_angle, pts=10):

    tan_end_ang = math.tan(end_angle)
    start_angle = get_line_ori(x_0, y_0, x_prev, y_prev)
    x_ca_multi = [x_0 + r_0*np.cos(start_angle + s*np.pi/2) for s in [1, -1]]
    y_ca_multi = [y_0 + r_0*np.sin(start_angle + s*np.pi/2) for s in [1, -1]]

    # Get center with largest y coordinate
    i_center = y_ca_multi.index(max(y_ca_multi))
    x_ca = x_ca_multi[i_center]
    y_ca = y_ca_multi[i_center]
      
    x_cb_sym = sp.Symbol('x_cb_sym', real=True)
    y_cb_sym = sp.Symbol('y_cb_sym', real=True)
    x_2_sym = sp.Symbol('x_2_sym', real=True)
    y_2_sym = sp.Symbol('y_2_sym', real=True)
    r_b_sym = sp.Symbol('r_b_sym', real=True)

    # Numerically
    eq_pt2_on_A = sp.Eq((x_2_sym - x_ca)**2 + (y_2_sym - y_ca)**2, r_0**2)
    eq_pt2_on_B = sp.Eq((x_2_sym - x_cb_sym)**2 + (y_2_sym - y_cb_sym)**2, r_b_sym**2)
    eq_pt3_on_B = sp.Eq((x_1 - x_cb_sym)**2 + (y_1 - y_cb_sym)**2, r_b_sym**2)
    eq_tangent_at_2 = sp.Eq((y_ca-y_2_sym) / (x_ca-x_2_sym), (y_2_sym-y_cb_sym) / (x_2_sym-x_cb_sym))
    eq_slope_at_3 = sp.Eq((x_1-x_cb_sym) / (y_1-y_cb_sym), tan_end_ang)

    init = (float(np.mean([x_0, x_1])), float(np.mean([y_0, y_1])), x_1, float(np.mean([y_0, y_1])), r_0)
    sols = sp.nsolve((eq_pt2_on_A, eq_pt2_on_B, eq_pt3_on_B, eq_tangent_at_2, eq_slope_at_3), (x_2_sym, y_2_sym, x_cb_sym, y_cb_sym, r_b_sym), init, verify=False)

    best_sol = _get_best_sol3(x_0, y_0, x_1, y_1, x_ca, y_ca, x_prev, y_prev, r_0, tan_end_ang, sols)
    x_tan, y_tan, x_cb, y_cb, r_1 = map(float, best_sol)
    
    # Figure out how many points in the two arcs (scale by length)
    arc1_length = r_0 * get_0_to_180(get_3point_ang((x_0, y_0), (x_ca, y_ca), (x_tan, y_tan)))
    arc2_length = r_1 * get_0_to_180(get_3point_ang((x_tan, y_tan), (x_cb, y_cb), (x_1, y_1)))
    arc_2_pts = round(pts/(arc1_length/arc2_length + 1))
    arc_1_pts = pts - arc_2_pts if arc_2_pts < pts else 1

    # Generate the points
    x_arc_1, y_arc_1 = get_arc_points(x_0, y_0, x_tan, y_tan, x_ca, y_ca, x_prev,      y_prev,      arc_1_pts, direction='cw')
    x_arc_2, y_arc_2 = get_arc_points(x_tan, y_tan, x_1, y_1, x_cb, y_cb, x_arc_1[-2], y_arc_1[-2], arc_2_pts, direction='ccw')

    return list(x_arc_1) + list(x_arc_2), list(y_arc_1) + list(y_arc_2), x_ca, y_ca, x_tan, y_tan, start_angle, i_center, x_cb, y_cb, r_1

def get_arc_arc_points(x_0, y_0, x_1, y_1, x_prev, y_prev, r_0, r_1, pts=10, sym_funcs=None, numerical=False):
    
    start_angle = get_line_ori(x_0, y_0, x_prev, y_prev)
    
    x_ca_multi = [x_0 + r_0*np.cos(start_angle + s*np.pi/2) for s in [1, -1]]
    y_ca_multi = [y_0 + r_0*np.sin(start_angle + s*np.pi/2) for s in [1, -1]]

    x_ca = None
    y_ca = None
    i_center = None

    # Get the center point closest to pt 1
    for i_ca, (x, y) in enumerate(zip(x_ca_multi, y_ca_multi)):
        if x_ca is None or norm([x_1-x, y_1-y]) < norm([x_1-x_ca, y_1-y_ca]):
            x_ca = x
            y_ca = y
            i_center = i_ca
    
    x_ca_sym = sp.Symbol('x_ca_sym', real=True)
    y_ca_sym = sp.Symbol('y_ca_sym', real=True)    
    x_cb_sym = sp.Symbol('x_cb_sym', real=True)
    y_cb_sym = sp.Symbol('y_cb_sym', real=True)
    x_1_sym = sp.Symbol('x_1_sym', real=True)
    y_1_sym = sp.Symbol('y_1_sym', real=True)
    x_2_sym = sp.Symbol('x_2_sym', real=True)
    y_2_sym = sp.Symbol('y_2_sym', real=True)
    x_3_sym = sp.Symbol('x_3_sym', real=True)
    y_3_sym = sp.Symbol('y_3_sym', real=True)
    r_a_sym = sp.Symbol('r_a_sym', real=True)
    r_b_sym = sp.Symbol('r_b_sym', real=True)

    if numerical is False:
        if sym_funcs is None and os.path.exists(ARCARC_FILE) is False:
            eq_pt2_on_A = sp.Eq((x_2_sym - x_ca_sym)**2 + (y_2_sym - y_ca_sym)**2, r_a_sym**2)
            eq_pt2_on_B = sp.Eq((x_2_sym - x_cb_sym)**2 + (y_2_sym - y_cb_sym)**2, r_b_sym**2)
            eq_pt3_on_B = sp.Eq((x_3_sym - x_cb_sym)**2 + (y_3_sym - y_cb_sym)**2, r_b_sym**2)
            eq_tangent_at_2 = sp.Eq((x_ca_sym - x_cb_sym)**2 + (y_ca_sym - y_cb_sym)**2, (r_b_sym - r_a_sym)**2)
            
            partial_sols_1 = sp.solve([eq_pt2_on_A, eq_pt2_on_B], x_2_sym, y_2_sym)
            partial_sols_2 = sp.solve([eq_pt3_on_B, eq_tangent_at_2], x_cb_sym, y_cb_sym)

            sym_sols = [[partial_sols_1[idx_sol][idx_var].subs([(x_cb_sym, partial_sols_2[idx_sol][0]), (y_cb_sym, partial_sols_2[idx_sol][1])]) for idx_var in range(2)] + list(partial_sols_2[idx_sol]) for idx_sol in range(2)]

            with open(ARCARC_FILE, 'wb') as fid:
                # dump(sym_sols, fid)
                sym_funcs = lambdify_and_dump(sym_sols, [x_ca_sym, y_ca_sym, x_1_sym, y_1_sym, x_3_sym, y_3_sym, r_a_sym, r_b_sym], fid)

        elif os.path.exists(ARCARC_FILE) is True:
            with open(ARCARC_FILE, 'rb') as fid:
                # sym_sols = load(fid)
                sym_funcs = load(fid)

        # Substitute for symbols in the symbolic solution
        sols = [tuple([f(x_ca, y_ca, x_0, y_0, x_1, y_1, r_0, r_1) for f in sym_func]) for sym_func in sym_funcs]
        
    else:
        eq_pt2_on_A = sp.Eq((x_2_sym - x_ca)**2 + (y_2_sym - y_ca)**2, r_0**2)
        eq_pt2_on_B = sp.Eq((x_2_sym - x_cb_sym)**2 + (y_2_sym - y_cb_sym)**2, r_1**2)
        eq_pt3_on_B = sp.Eq((x_1 - x_cb_sym)**2 + (y_1 - y_cb_sym)**2, r_1**2)
        eq_tangent_at_2 = sp.Eq((x_ca - x_cb_sym)**2 + (y_ca - y_cb_sym)**2, (r_1 - r_0)**2)

        init = (float(np.mean([x_0, x_1])), float(np.mean([y_0, y_1])), x_1, float(np.mean([y_0, y_1])))
        sols = sp.nsolve((eq_pt2_on_A, eq_pt2_on_B, eq_pt3_on_B, eq_tangent_at_2), (x_2_sym, y_2_sym, x_cb_sym, y_cb_sym), init, verify=False)
        sols = [[sols[row, col] for row in range(sols.rows)] for col in range(sols.cols)]

    # Get the best solution  
    best_sol = _get_best_sol2(x_0, y_0, x_1, y_1, x_ca, y_ca, x_prev, y_prev, r_0, r_1, sols)    
    x_tan, y_tan, x_cb, y_cb = map(float, best_sol)
    
    # Figure out how many points in the two arcs (scale by length)
    arc1_length = r_0 * get_0_to_180(get_3point_ang((x_0, y_0), (x_ca, y_ca), (x_tan, y_tan)))
    arc2_length = r_1 * get_0_to_180(get_3point_ang((x_tan, y_tan), (x_cb, y_cb), (x_1, y_1)))
    arc_2_pts = round(pts/(arc1_length/arc2_length + 1))
    arc_1_pts = pts - arc_2_pts if arc_2_pts < pts else 1

    # Generate the points
    x_arc_1, y_arc_1 = get_arc_points(x_0, y_0, x_tan, y_tan, x_ca, y_ca, x_prev,      y_prev,      arc_1_pts, direction='cw')
    x_arc_2, y_arc_2 = get_arc_points(x_tan, y_tan, x_1, y_1, x_cb, y_cb, x_arc_1[-2], y_arc_1[-2], arc_2_pts, direction='cw')

    return list(x_arc_1) + list(x_arc_2), list(y_arc_1) + list(y_arc_2), x_ca, y_ca, x_tan, y_tan, sym_funcs, start_angle, i_center, x_cb, y_cb

def lambdify_and_dump(sols, vbs, fid):
    pk = [[sp.lambdify(vbs, eq, 'numpy') for eq in sol] for sol in sols]
    dill.settings['recurse'] = True
    dill.dump(pk, fid)
    return pk

def subs_lambdify(eq, vbs):
    f = sp.lambdify([vb[0] for vb in vbs], eq, 'numpy')
    ans = f(*[vb[1] for vb in vbs])
    return ans

def drop_zero_imag(sol):
    for i, eq in enumerate(sol):
        if eq.is_Add is True:
            sol[i] = eq.as_real_imag()[0]

    return sol

def get_0_to_180(ang):
    if abs(ang) > np.pi:
        ang = 2*np.pi-abs(ang)
    
    return ang

def get_0_to_360(ang):
    if ang < 0:
        ang = 2*np.pi + ang
    return ang

def get_3point_ang(a, b, c):
    ang = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])

    if ang < 0:
        ang += 2*np.pi
    
    if ang > np.pi:
        ang = 2*np.pi - ang

    return ang

def get_arc_line_points(x_0, y_0, x_1, y_1, x_prev, y_prev, r_curve, pts=10, sym_sols=None, numerical=False):
    
    start_angle = get_line_ori(x_0, y_0, x_prev, y_prev)
    
    x_c_multi = [x_0 + r_curve*np.cos(start_angle + s*np.pi/2) for s in [1, -1]]
    y_c_multi = [y_0 + r_curve*np.sin(start_angle + s*np.pi/2) for s in [1, -1]]

    x_c = None
    y_c = None
    i_center = None

    # Get the center point closest to pt 1
    for i_c, (x, y) in enumerate(zip(x_c_multi, y_c_multi)):
        if x_c is None or norm([x_1-x, y_1-y]) < norm([x_1-x_c, y_1-y_c]):
            x_c = x
            y_c = y
            i_center = i_c
    
    x = sp.Symbol('x', real=True)
    y = sp.Symbol('y', real=True)
    x_c_sym = sp.Symbol('x_c_sym', real=True)
    y_c_sym = sp.Symbol('y_c_sym', real=True)
    x_1_sym = sp.Symbol('x_1_sym', real=True)
    y_1_sym = sp.Symbol('y_1_sym', real=True)
    r_curve_sym = sp.Symbol('r_curve_sym', real=True)

    if numerical is False:
        if sym_sols is None and os.path.exists(ARCLINE_FILE) is False:
            eq_circle = sp.Eq((x - x_c_sym)**2 + (y - y_c_sym)**2, r_curve_sym**2)
            eq_perp = sp.Eq((y - y_c_sym)/(x - x_c_sym), -(x - x_1_sym)/(y - y_1_sym))
            sym_sols = sp.solve([eq_circle, eq_perp], x, y)
            
            with open(ARCLINE_FILE, 'wb') as fid:
                dump(sym_sols, fid)

        elif os.path.exists(ARCLINE_FILE) is True:
            with open(ARCLINE_FILE, 'rb') as fid:
                sym_sols = load(fid)

        # Substitute for symbols in the symbolic solution
        sols = [tuple([eq.subs([(x_c_sym, x_c), (y_c_sym, y_c), (x_1_sym, x_1), (y_1_sym, y_1), (r_curve_sym, r_curve)]) for eq in sym_sol]) for sym_sol in sym_sols]

    else:
        
        eq_circle = sp.Eq((x - x_c)**2 + (y - y_c)**2, r_curve**2)
        eq_perp = sp.Eq((y - y_c)/(x - x_c), -(x - x_1)/(y - y_1))

        init = (50, 150)
        sols = sp.nsolve((eq_circle, eq_perp), (x, y), init, verify=False)
        sols = [[sols[row, col] for row in range(sols.rows)] for col in range(sols.cols)]

    # Get the best solution  
    best_sol = _get_best_sol4(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, r_curve, sols)

    x_tan = float(sp.re(best_sol[0]))
    y_tan = float(sp.re(best_sol[1]))
    
    # Figure out how many points in the arc and line (scale by length)
    arc_length = r_curve * get_3point_ang((x_0, y_0), (x_c, y_c), (x_tan, y_tan))
    line_length = norm([x_1 - x_tan, y_1 - y_tan])
    line_pts = round(pts/(arc_length/line_length + 1))
    arc_pts = pts - line_pts if line_pts < pts else 1

    # Generate the points
    x_arc, y_arc = get_arc_points(x_0, y_0, x_tan, y_tan, x_c, y_c, x_prev, y_prev, arc_pts, direction='ccw')
    x_line, y_line = get_line_points(x_tan, y_tan, x_1, y_1, line_pts)

    return list(x_arc) + list(x_line), list(y_arc) + list(y_line), x_c, y_c, x_tan, y_tan, sym_sols, start_angle, i_center


def _get_best_sol3(x_0, y_0, x_1, y_1, x_ca, y_ca, x_prev, y_prev, r_a, tan_end_ang, sols, i_center=1):
    return [sols[row, 0] for row in range(sols.rows)]
    
def _get_best_sol2(x_0, y_0, x_1, y_1, x_ca, y_ca, x_prev, y_prev, r_a, r_b, sols, i_center=1):
    """Gets the solution with the the solution with the shortest arclength
    
    """
    arc_lengths = []
    for i, sol in enumerate(sols):

        # Look for NaNs in tan point and center point
        if any([math.isnan(v) for v in sol[:2]]) and not any([math.isnan(v) for v in sol[2:]]):
            # If NaNs found in tangent point but not in center b, find tangent point from center b            
            x_cb, y_cb = map(float, sol[2:])
            sol = (*get_two_circ_tan_point((x_ca, y_ca), r_a, (x_cb, y_cb), r_b), x_cb, y_cb)
            sols[i] = sol
        
        elif any([math.isnan(v) for v in sol[2:]]):
            # If NaNs found in center point, skip this solution
            arc_lengths.append(np.inf)
            continue
        
        # try:
        x_tan, y_tan, x_cb, y_cb = map(float, sol)
        # except TypeError:
        #     continue

        x_arc_a, y_arc_a = get_arc_points(x_0, y_0, x_tan, y_tan, x_ca, y_ca, x_prev, y_prev)
        x_arc_b, y_arc_b = get_arc_points(x_tan, y_tan, x_1, y_1, x_cb, y_cb, x_arc_a[-2], y_arc_a[-2])

        arc_length_a = sum([norm([x1-x0, y1-y0]) for (x0, x1, y0, y1) in zip(x_arc_a[:-1], x_arc_a[1:], y_arc_a[:-1], y_arc_a[1:])])
        arc_length_b = sum([norm([x1-x0, y1-y0]) for (x0, x1, y0, y1) in zip(x_arc_b[:-1], x_arc_b[1:], y_arc_b[:-1], y_arc_b[1:])])

        arc_lengths.append(sum([arc_length_a, arc_length_b]))
        
    return sols[arc_lengths.index(min(arc_lengths))]

def _get_best_sol(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, r_curve, sols, i_center=1):
    """Gets the solution with the the solution with maximum or minimum subtended angle.
    
    """
    angs = []
    for sol in sols:
        
        # Look for NaNs
        if any([math.isnan(v) for v in sol]):
            # If NaNs found, skip this solution
            angs.append(np.inf if i_center==1 else -np.inf)
            continue

        # try:
        x_tan = float(sol[0])
        y_tan = float(sol[1])
        # except TypeError:
        #     continue

        x_arc, y_arc = get_arc_points(x_0, y_0, x_tan, y_tan, x_c, y_c, x_prev, y_prev, 100)

        start_ang = abs(get_3point_ang((x_prev, y_prev), (x_0, y_0), (x_arc[1], y_arc[1])))
        end_ang = abs(get_3point_ang((x_arc[-2], y_arc[-2]), (x_tan, y_tan), (x_1, y_1)))

        angs.append(min([start_ang, end_ang]))
        
    return sols[angs.index(min(angs))] if i_center == 1 else sols[angs.index(max(angs))]

def _get_best_sol4(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, r_curve, sols, i_center=1):
    """Gets the solution with the the solution with maximum or minimum subtended angle.
    
    """
    arc_lengths = []
    for sol in sols:
        
        # Look for NaNs
        if any([math.isnan(sp.re(v)) for v in sol]):
            # If NaNs found, skip this solution
            arc_lengths.append(np.inf)
            continue

        x_tan = float(sp.re(sol[0]))
        y_tan = float(sp.re(sol[1]))

        # arc_length = r_curve * get_3point_ang((x_0, y_0), (x_c, y_c), (x_tan, y_tan))
        arc_length = r_curve * get_0_to_360(get_angle_two_vecs(x_0-x_c, y_0-y_c, x_tan-x_c, y_tan-y_c))
        line_length = norm([x_1 - x_tan, y_1 - y_tan])

        arc_lengths.append(arc_length + line_length)
        
    return sols[arc_lengths.index(min(arc_lengths))]

def get_line_points(x_0, y_0, x_1, y_1, pts=10):
    return np.linspace(x_0, x_1, pts), np.linspace(y_0, y_1, pts)

def arc_center(x_0, y_0, x_1, y_1, m_0):
    """Returns the x and y coordinates of the center of curvature of an arc given the start and end coordinates, and the slope at the start.

    Parameters
    ----------
    x_0 : float
        Starting X coordinate
    y_0 : float
        Starting Y coordinate
    x_1 : float
        Ending X coordinate
    y_1 : float
        Ending Y coordinate
    m_0 : float
        Starting slop

    Returns
    -------
    list, list
        x and y coordinates of center of curvature

    """
    a = -m_0
    b = 1

    x = sp.Symbol('x', real=True)
    y = sp.Symbol('y', real=True)

    eq1 = sp.Eq(b*x -a*y - (b*x_0-a*y_0), 0)
    eq2 = sp.Eq((x_0 - x_1)*x + (y_0 - y_1)*y  -  .5*(x_0**2 + y_0**2 - x_1**2 - y_1**2), 0)

    sol = sp.solve([eq1, eq2], x, y)        
    
    x_c = [v for v in sol.values()][0]
    y_c = [v for v in sol.values()][1]

    return x_c, y_c

# def get_arc_points2(x_0, y_0, radius, x_prev, y_prev, delta_angle, pts=10, flip=1, direction=None):

#     entry_angle = get_line_ori(x_0, y_0, x_prev, y_prev)
#     ang_to_center = entry_angle + np.pi/2*flip

#     x_c = x_0 + radius*np.cos(ang_to_center)
#     y_c = y_0 + radius*np.sin(ang_to_center)

#     ang_from_prev = get_line_ori(x_c, y_c, x_0, y_0)  - get_line_ori(x_c, y_c, x_prev, y_prev) 
    
#     delta_angle_1 = delta_angle
#     delta_angle_2 = -np.sign(delta_angle)*(2*np.pi-abs(delta_angle))
    
#     if direction is None:
#         delta_angle = delta_angle_1 if np.sign(delta_angle_1) == np.sign(ang_from_prev) else delta_angle_2
#     elif direction == 'ccw':
#         delta_angle = delta_angle_1 if delta_angle_1 > 0 else delta_angle_2
#     elif direction == 'cw':
#         delta_angle = delta_angle_1 if delta_angle_1 < 0 else delta_angle_2

#     end_angle = start_angle + delta_angle
    
#     angles = np.linspace(start_angle, end_angle, pts)   

#     x = list([x_c + radius*np.cos(angle) for angle in angles])
#     y = list([y_c + radius*np.sin(angle) for angle in angles])

#     return x, y

def get_arc_points(x_0, y_0, x_1, y_1, x_c, y_c, x_prev, y_prev, pts=10, direction=None):
    """Returns points on an arc given the start and end points, center of curvature, and a third point through which the start tangent passes.

    Parameters
    ----------
    x_0 : float
        Starting X coordinate
    y_0 : float
        Starting Y coordinate
    x_1 : float
        Ending X coordinate
    y_1 : float
        Ending Y coordinate
    x_c : float
        X coordinate of center of curvature
    y_c : float
        Y coordinate of center of curvature
    x_prev : float
        X coordinate of point through which the start tangent passes
    y_prev : float
        Y coordinate point through which the start tangent passes
    pts : int, optional
        Number of points to return, by default 10

    Returns
    -------
    list, list
        x and y coordinate of points on the arc

    """
    start_angle = get_line_ori(x_c, y_c, x_0, y_0)

    ang_from_prev = get_line_ori(x_c, y_c, x_0, y_0)  - get_line_ori(x_c, y_c, x_prev, y_prev) 

    # ang_from_prev = get_3point_ang((x_0, y_0), (x_c, y_c), (x_1, y_1))
    
    # delta_angle_1 = get_3point_ang((x_0, y_0), (x_c, y_c), (x_1, y_1))    
    delta_angle_1 = get_line_ori(x_c, y_c, x_1, y_1)  - get_line_ori(x_c, y_c, x_0, y_0) 
    delta_angle_2 = -np.sign(delta_angle_1)*(2*np.pi-abs(delta_angle_1))
    
    if direction is None:
        delta_angle = delta_angle_1 if np.sign(delta_angle_1) == np.sign(ang_from_prev) else delta_angle_2
    elif direction == 'ccw':
        delta_angle = delta_angle_1 if delta_angle_1 > 0 else delta_angle_2
    elif direction == 'cw':
        delta_angle = delta_angle_1 if delta_angle_1 < 0 else delta_angle_2

    end_angle = start_angle + delta_angle
    
    angles = np.linspace(start_angle, end_angle, pts)   
    radius = norm(np.array([x_0-x_c, y_0-y_c]).astype(np.float64))

    x = list([x_c + radius*np.cos(angle) for angle in angles])
    y = list([y_c + radius*np.sin(angle) for angle in angles])

    return x, y

def get_two_circ_tan_point(loc_ca, r_a, loc_cb, r_b):
    def error(loc):
        err_a = abs(norm([loc[0] - loc_ca[0], loc[1] - loc_ca[1]]) - r_a)
        err_b = abs(norm([loc[0] - loc_cb[0], loc[1] - loc_cb[1]]) - r_b)
        return max([err_a, err_b])
    
    res = optimize.minimize(error, [-10, 10], method='Nelder-Mead')
    return tuple(res.x)

def get_line_ori(x_0, y_0, x_1, y_1):
    """Returns the orientation of a vector defined by two points in 2D space.

    Parameters
    ----------
    x_0 : float
        X coordinate of first point
    y_0 : float
        Y coordinate of first point
    x_1 : float
        X coordinate of second point
    y_1 : float
        Y coordinate of second point

    Returns
    -------
    float
        Orientation of the vector (radians)

    """
    
    return math.atan2(y_1-y_0, x_1-x_0)

def get_angle_two_vecs(x_0, y_0, x_1, y_1):
    """Returns the orientation between the two vectors defined from the origin to the two given points in 2D space.

    Parameters
    ----------
    x_0 : float
        X coordinate of first point
    y_0 : float
        Y coordinate of first point
    x_1 : float
        X coordinate of second point
    y_1 : float
        Y coordinate of second point

    Returns
    -------
    float
        Angle between the two vectors (radians)

    """
    ang_0 = get_line_ori(0, 0, x_0, y_0)
    ang_1 = get_line_ori(0, 0, x_1, y_1)
    ang = ang_1 - ang_0

    return ang


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    x_0 = -66.411
    y_0 = 57.325
    x_1 = -59.795
    y_1 = 117.916
    r_0 = 27
    r_1 = 60
    x_prev = -53.044
    y_prev = 55.998

    x_arc, y_arc, x_ca, y_ca, x_tan, y_tan, sym_sols, start_angle, i_center, x_cb, y_cb = get_arc_arc_points(x_0, y_0, x_1, y_1, x_prev, y_prev, r_0, r_1, pts=10)

    (fig, ax) = plt.subplots()
    ax.scatter(x_arc, y_arc)
    ax.scatter([x_0, x_1], [y_0, y_1], c='r')
    ax.scatter([x_cb, x_ca], [y_cb, y_ca], c='g')
    ax.grid()
    ax.axis('square')

    plt.show()