import numpy as np
import matplotlib.pyplot as plt
from power_spectrum import *

result_folder_path1 = 'D:\\Speckle_data\\hd52721\\04082019\\550\\hip96977\\result_ref\\ps1'
result_folder_path2 = 'D:\\Speckle_data\\hd52721\\04082019\\550\\hip96977\\result_ref\\ps2'


#load dark, flat and stars spectra
mean_dark1, mean_flat1, mean_star_ps1, mean_ref_ps1 = load_ps_from_folder(result_folder_path1)
mean_dark2, mean_flat2, mean_star_ps2, mean_ref_ps2 = load_ps_from_folder(result_folder_path2)

#
ps1=final_power_spectrum(mean_star_ps1, mean_ref_ps1)
ps2 = final_power_spectrum(mean_star_ps2, mean_ref_ps2)

#plot spectra for finding bound freq
plt.figure()
plt.plot(mean_dark1[:,256],label='middle')
plt.plot(mean_dark2[:,256],label='median')
plt.legend()
plt.title('dark x')
plt.show()

plt.figure()
plt.plot(mean_dark1[256,:],label='middle')
plt.plot(mean_dark2[256,:],label='median')
plt.legend()
plt.title('dark y')
plt.show()

plt.figure()
plt.plot(mean_flat1[:,256],label='middle')
plt.plot(mean_flat2[:,256],label='median')
plt.legend()
plt.title('flat x')
plt.show()

plt.figure()
plt.plot(mean_flat1[256,:],label='middle')
plt.plot(mean_flat2[256,:],label='median')
plt.legend()
plt.title('flat y')
plt.show()

plt.figure()
plt.plot(mean_ref_ps1[:,256],label='middle')
plt.plot(mean_ref_ps2[:,256],label='median')
plt.legend()
plt.yscale('log')
plt.title('ref x')
plt.show()

plt.figure()
plt.plot(mean_ref_ps1[256,:],label='middle')
plt.plot(mean_ref_ps2[256,:],label='median')
plt.legend()
plt.yscale('log')
plt.title('ref y')
plt.show()

plt.figure()
plt.plot(mean_star_ps1[:,256],label='middle')
plt.plot(mean_star_ps2[:,256],label='median')
plt.legend()
plt.yscale('log')
plt.title('obj x')
plt.show()

plt.figure()
plt.plot(mean_star_ps1[256,:],label='middle')
plt.plot(mean_star_ps2[256,:],label='median')
plt.legend()
plt.yscale('log')
plt.title('obj y')
plt.show()

plt.figure()
plt.plot(ps1[:,256],label='middle')
plt.plot(ps2[:,256],label='median')
plt.legend()
plt.xlim(40,470)
plt.ylim(0,1.3)
plt.title('obj/ref x')
plt.show()

plt.figure()
plt.plot(ps1[256,:],label='middle')
plt.plot(ps2[256,:],label='median')
plt.legend()
plt.xlim(40,470)
plt.ylim(0,1.3)
plt.title('obj/ref y')
plt.show()
