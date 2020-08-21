import sys
sys.path.insert(0, "C:\\Users\\Marta\\source\\repos\\crunchy-taiyaki\\Speckle\\src\\modules")
import numpy as np
import matplotlib.pyplot as plt
from power_spectrum import *
import plot

load_path = 'D:\\Speckle_data\\hd52721\\04082019\\550\\hip96977\\result_ref\\ps1'
result_folder_path = 'D:\\Speckle_data\\hd52721\\04082019\\550\\hip96977\\result_ref\\ps1\\test_background'

#load dark, flat and stars spectra
mean_dark, mean_flat, mean_star_ps, mean_ref_ps = load_ps_from_folder(load_path)

mean_star_ps_rmbg = remove_background(mean_star_ps,460)
mean_ref_ps_rmbg = remove_background(mean_ref_ps,460)

plt.figure()
plt.plot(mean_ref_ps[:,256],label='ref')
plt.plot(mean_ref_ps_rmbg[:,256],label='rmbg ref')
plt.legend()
plt.yscale('log')
plt.ylim(1,1e10)
plt.xlim(0,512)
plt.title('ref x')
plt.savefig(result_folder_path + '\\ref_x.png')
plt.show()

plt.figure()
plt.plot(mean_ref_ps[256,:],label='ref')
plt.plot(mean_ref_ps_rmbg[256,:],label='rmbg ref')
plt.legend()
plt.yscale('log')
plt.ylim(1,1e10)
plt.xlim(0,512)
plt.title('ref y')
plt.savefig(result_folder_path + '\\ref_y.png')
plt.show()

plt.figure()
plt.plot(mean_star_ps[:,256],label='star')
plt.plot(mean_star_ps_rmbg[:,256],label='rmbg star')
plt.legend()
plt.yscale('log')
plt.ylim(1,1e10)
plt.xlim(1,512)
plt.title('obj x')
plt.savefig(result_folder_path + '\\obj_x.png')
plt.show()

plt.figure()
plt.plot(mean_star_ps[256,:],label='star')
plt.plot(mean_star_ps_rmbg[256,:],label='rmbg star')
plt.legend()
plt.yscale('log')
plt.ylim(1,1e10)
plt.xlim(0,512)
plt.title('obj y')
plt.savefig(result_folder_path + '\\obj_y.png')
plt.show()

ps=final_power_spectrum(mean_star_ps, mean_ref_ps)
ps_rmbg=final_power_spectrum(mean_star_ps_rmbg, mean_ref_ps_rmbg)

plt.figure()
plt.plot(ps[:,256],label='ps')
plt.plot(ps_rmbg[:,256],label='rmbg ps')
plt.legend()
plt.ylim(0,1.3)
plt.xlim(0,512)
plt.title('obj/ref x')
plt.savefig(result_folder_path + '\\ps_x.png')
plt.show()

plt.figure()
plt.plot(ps[256,:],label='ps')
plt.plot(ps_rmbg[256,:],label='rmbg ps')
plt.legend()
plt.ylim(0,1.3)
plt.xlim(0,512)
plt.title('obj/ref y')
plt.savefig(result_folder_path + '\\ps_y.png')
plt.show()