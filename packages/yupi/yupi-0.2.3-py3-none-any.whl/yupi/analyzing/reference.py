import numpy as np
from yupi.affine_estimator import affine_matrix

def add_dynamic_reference(trajectory, reference, start_in_origin=True):
    """ 
    This functions fuse the information of a trajectory with an 
    external reference of the motion of the System of Reference
    (SoR).

    It allows to remap the information gathered in local SoRs
    to a more general SoR.
    """
    def affine2camera(theta, tx, ty):
        x_cl, y_cl, theta_cl = np.zeros((3, theta.size + 1))
        theta_cl[1:] = np.cumsum(theta)

        for i in range(theta.size):
            A = affine_matrix(theta_cl[i + 1], x_cl[i], y_cl[i], R_inv=True)
            x_cl[i + 1], y_cl[i + 1] = A @ [-tx[i], -ty[i], 1]

        x_cl, y_cl, theta_cl = x_cl[1:], y_cl[1:], theta_cl[1:]
        return x_cl, y_cl, theta_cl


    def camera2obj(x_ac, y_ac, x_cl, y_cl, theta_cl):
        x_al, y_al = np.empty((2, x_ac.size))

        for i in range(x_ac.size):
            A = affine_matrix(theta_cl[i], x_cl[i], y_cl[i], R_inv=True)
            x_al[i], y_al[i] = A @ [x_ac[i], y_ac[i], 1]

        return x_al, y_al


    def affine2obj(theta, tx, ty, x_ac, y_ac):
        x_cl, y_cl, theta_cl = affine2camera(theta, tx, ty)
        x_al, y_al = camera2obj(x_ac, y_ac, x_cl, y_cl, theta_cl)
        return x_al, y_al

    theta, tx, ty = reference

    x_al, y_al = affine2obj(theta, tx, ty, trajectory.x_arr, trajectory.y_arr)
    
    if start_in_origin:
        x_al = x_al - x_al[0]
        y_al = y_al - y_al[0]

    trajectory.x_arr = x_al
    trajectory.y_arr = y_al

    return trajectory