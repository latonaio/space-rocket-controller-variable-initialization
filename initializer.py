# TO-DO: Containerize to microservice
import json
import sys
import numpy as np
# State controller implemented only for debug purposes
from state_controller import StateController

def main(input_file_name):
  f = open(input_file_name)
  input_file = json.load(f)
  f.close()
  metadata_distributor = StateController()
  human_readable_to_variable = {
    'ground_speed': 'v_g_0', 'flight_path_angle': 'gamma_0', 'launch_azimuth': 'xi_0',
    'ground_angular_velocity_1': 'p_g_0', 'ground_angular_velocity_2': 'q_g_0', 'ground_angular_velocity_3': 'r_g_0',
    'longtitude': 'lamb_0', 'latitude': 'eta_0', 'altitude': 'h_0',
    'euler_angle_1': 'phi_0', 'euler_angle_2': 'theta_0', 'euler_angle_3': 'sai_0',
    'start_time': 't_0',
    'centroid': 'xyz_cg',
    'characteristic_length': 'char_l',
    'flightbody_width': 'flightbody_w', 'flightbody_length': 'flightbody_l', 'flightbody_surface_area': 'flightbody_sa',
    'flightbody_mass': 'flightbody_m','flightbody_moment_of_inertia': 'flightbody_I' #matrix of moments of inertia,
  }
  vars = {}
  for k in human_readable_to_variable.keys():
    try:
      vars[human_readable_to_variable[k]] = float(input_file[k])
    except:
      print(f'WARNING: Error reading {k}')
  # Initialize direction cosines
  t_se = np.zeros([3,3])
  t_se[0][0] = np.cos(metadata_distributor.constants['OMEGA']*vars['t_0'] + vars['lamb_0'])
  t_se[0][1] = np.sin(metadata_distributor.constants['OMEGA']*vars['t_0'] + vars['lamb_0'])
  t_se[1][0] = -1*t_se[0][1]
  t_se[1][1] = t_se[0][0]
  t_se[2][2] = 1.0

  t_eh = np.zeros([3,3])
  t_eh[0][0] = np.cos(-vars['eta_0'] - metadata_distributor.constants['PI']/2)
  t_eh[0][2] = -1*np.sin(-vars['eta_0'] - metadata_distributor.constants['PI']/2)
  t_eh[2][0] = -1*t_eh[0][2]
  t_eh[2][2] = t_eh[0][0]
  t_eh[1][1] = 1.0

  t_hb = np.zeros([3,3])
  t_hb[0][0] = np.cos(vars['theta_0'])*np.cos(vars['sai_0'])
  t_hb[0][1] = np.cos(vars['theta_0'])*np.sin(vars['sai_0'])
  t_hb[0][2] = -np.sin(vars['theta_0'])
  t_hb[1][0] = np.sin(vars['phi_0'])*np.sin(vars['theta_0'])*np.cos(vars['sai_0']) \
              - np.cos(vars['phi_0'])*np.sin(vars['sai_0'])
  t_hb[1][1] = np.sin(vars['phi_0'])*np.sin(vars['theta_0'])*np.sin(vars['sai_0']) \
              + np.cos(vars['phi_0'])*np.cos(vars['sai_0'])
  t_hb[1][2] = np.sin(vars['phi_0'])*np.cos(vars['theta_0'])
  t_hb[2][0] = np.cos(vars['phi_0'])*np.sin(vars['theta_0'])*np.cos(vars['sai_0']) \
              + np.sin(vars['phi_0'])*np.sin(vars['sai_0'])
  t_hb[2][1] = np.cos(vars['phi_0'])*np.sin(vars['theta_0'])*np.sin(vars['sai_0'])\
              - np.sin(vars['phi_0'])*np.cos(vars['sai_0'])
  t_hb[2][2] = np.cos(vars['phi_0'])*np.cos(vars['theta_0'])

  t_sb = t_hb*t_eh*t_se

  # initialize prime vertical
  r_n_0 = metadata_distributor.constants['A']/ \
        (1-metadata_distributor.constants['E']**2*np.sin(vars['eta_0'])**2)

  # initialize quaternions
  q = np.zeros(4)
  q[0] = np.sign(t_sb[1][2]-t_sb[2][1])/2*(1+t_sb[0][0]-t_sb[1][1]-t_sb[2][2])**0.5
  q[1] = np.sign(t_sb[2][0]-t_sb[0][2])/2*(1-t_sb[0][0]+t_sb[1][1]-t_sb[2][2])**0.5
  q[2] = np.sign(t_sb[0][1]-t_sb[1][0])/2*(1-t_sb[0][0]-t_sb[1][1]+t_sb[2][2])**0.5
  q[3] = .5*(1+t_sb[0][0]+t_sb[1][1]+t_sb[2][2])**0.5

  # initialize center of gravity of flight body in ECI coordinates
  xyz_s = np.zeros(3)
  xyz_s[0] = (r_n_0+vars['h_0'])*np.cos(vars['eta_0']) \
              *np.cos(metadata_distributor.constants['OMEGA']*vars['t_0']+vars['lamb_0'])
  xyz_s[1] = (r_n_0+vars['h_0'])*np.cos(vars['eta_0']) \
              *np.sin(metadata_distributor.constants['OMEGA']*vars['t_0']+vars['lamb_0'])
  xyz_s[2] = ((1-metadata_distributor.constants['E']**2)*r_n_0+vars['h_0'])*np.sin(vars['eta_0'])

  # initialize angular velocity of flight body (flight body inertial coordinates)
  pqr = np.zeros(3)
  pqr[0] = vars['p_g_0']
  pqr[1] = vars['q_g_0']
  pqr[2] = vars['r_g_0']
  pqr = pqr + np.matmul(pqr, np.array([0,0,metadata_distributor.constants['OMEGA']]))

  # intialize velocities of flight body (flight body inertial coordinates)
  uvw = np.zeros(3)
  uvw[0] = vars['v_g_0']*np.cos(vars['gamma_0'])*np.cos(vars['xi_0'])
  uvw[1] = vars['v_g_0']*np.cos(vars['gamma_0'])*np.sin(vars['xi_0']) \
            + (xyz_s[0]**2+xyz_s[1]**2)**0.5*metadata_distributor.constants['OMEGA']
  uvw[2] = -vars['v_g_0']*np.sin(vars['eta_0'])
  uvw = np.matmul(t_hb, uvw)

  metadata_distributor.set({'t_se': t_se, 't_eh': t_eh, 't_hb': t_hb, 't_sb': t_sb})
  metadata_distributor.set({'q': q, 'xyz_s': xyz_s, 'pqr': pqr, 'uvw': uvw})
  # TO-DO create test file to ensure computation accuracy
  return metadata_distributor

if __name__ == '__main__':
  if len(sys.argv) > 1:
    # TO-DO: improve input file reading with keyword
    main(sys.argv[1])