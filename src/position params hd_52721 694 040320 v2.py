import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from power_spectrum import final_power_spectrum

#___________________ACF_____________________________________
def acf(star_ps):
    acf = np.abs(fft.ifft2(star_ps))
    acf = fft.fftshift(acf)
    return acf

#__________________HELP FUNCTIONS___________________________________
def ring_mask(img, r1, r2):
    H, W = img.shape
    x, y = np.meshgrid(np.arange(W), np.arange(H))
    d2 = (x - 256)**2 + (y - 256)**2
    mask = d2 < r1**2
    mask1 = d2 > r2**2
    img_masked_ring = np.copy(img)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask)
    img_masked_ring = np.ma.array(img_masked_ring, mask = mask1)
    return img_masked_ring

def slice_image(data,x1,y1,x2,y2):
    size = data.shape[0]
    projection = np.ones(size)*np.nan
    k = (y2-y1)/(x2-x1)
    for x in range(0, size):
        y = int(x*k-x2*k+y2)
        if y < 512 and y>0:
            projection[x] = data[x,y]
    return projection

def mask_freq(ar,freq_ar,freq1,freq2):
    mask = freq_ar >= freq2
    mask1 = freq_ar <= freq1
    masked_ar = copy(ar)
    masked_ar = ma.array(masked_ar, mask = mask)
    masked_ar = ma.array(masked_ar, mask = mask1)
    return masked_ar





#path = 'D:\\Speckle_data\\hd52721\\040320\\694\\result_ref\\'
#acff = acf(middle_star/middle_ref)
#x = np.array([263.972,266.114])
#y = np.array([326.112,329.668])
#plt.figure()
#plt.imshow(acff, cmap='gray', vmin=np.min(acff), vmax=np.max(acff)/200)
## plt.scatter(x,y)
#plt.savefig(path + 'acf.png')
#plt.show()

ps = final_power_spectrum()

size=512
U = np.arange(0,size)/size
V = np.arange(0,size)/size
xdata = np.meshgrid(U,V)
bandwidth = 2
f_ar = np.arange(5,190,bandwidth)
f_ar_lenght = len(f_ar)
u,v = xdata # u,v coordinate grid must be define before triple_spectrum_2d_min!
def triple_spectrum_2d_min(I1,DM21,DM31,x1,y1,x2,y2,x3,y3):
    DI2 = 10**(-0.4*DM21)
    DI3 = 10**(-0.4*DM31)
    result = I1**2*(1 + DI2**2 + DI3**2 + 2*DI2*np.cos(2*np.pi*((v-0.5)*(x1-x2) + (u-0.5)*(y1-y2))) +\
    2*DI3*np.cos(2*np.pi*((v-0.5)*(x1-x3) + (u-0.5)*(y1-y3))) +\
    2*DI2*DI3*np.cos(2*np.pi*((v-0.5)*(x2-x3) + (u-0.5)*(y2-y3))))
    return result

def res_fun(x):
    return sum((triple_spectrum_2d_min(*x) - ydata)**2)


dm21_ar = np.zeros(f_ar_lenght)
dm31_ar = np.zeros(f_ar_lenght)
r12_ar = np.zeros(f_ar_lenght)
r13_ar = np.zeros(f_ar_lenght)
psi2_ar = np.zeros(f_ar_lenght)
psi3_ar = np.zeros(f_ar_lenght)
I1_ar = np.zeros(f_ar_lenght)
x2_ar = np.zeros(f_ar_lenght)
y2_ar = np.zeros(f_ar_lenght)
x3_ar = np.zeros(f_ar_lenght)
y3_ar = np.zeros(f_ar_lenght)

#______________fiting_____________________________________
for i in range(f_ar_lenght):
    ydata = ring_mask(ps,f_ar[i],f_ar[i]+bandwidth)
    scale = np.sqrt(np.nanmean(ydata))
    I1 = scale

    DM21 = 2.1508108889915714
    DM31 = 2.2729956539732257
    y1 = 256; x1 = 256
    y2 = 263.972; x2 = 326.112
    y3= 266.114; x3 = 329.668
    ig = np.array([I1,DM21,DM31,x1,y1,x2,y2,x3,y3])
    print('freq:', f_ar[i])
    popt = minimize(res_fun, ig, method='L-BFGS-B',\
    tol=1e-8)

    I1 = popt.x[0]
    DM21 = popt.x[1]
    DM31 = popt.x[2]
    x1 = popt.x[3]
    y1 = popt.x[4]
    x2 = popt.x[5]
    y2 = popt.x[6]
    x3 = popt.x[7]
    y3 = popt.x[8]
    r12 = np.sqrt((x2-256)**2 + (y2-256)**2)
    r13 = np.sqrt((x3-256)**2 + (y3-256)**2)
    PSI2 = np.arctan2(y2-256,x2-256)*180/np.pi
    PSI3 = np.arctan2(y3-256,x3-256)*180/np.pi
    dm21_ar[i] = DM21
    dm31_ar[i] = DM31
    r12_ar[i] = r12
    r13_ar[i] = r13
    psi2_ar[i] = PSI2
    psi3_ar[i] = PSI3
    I1_ar[i] = I1
    x2_ar[i] = x2
    y2_ar[i] = y2
    x3_ar[i] = x3
    y3_ar[i] = y3

##___________saving_data_______________________________________
#path = 'D:\\Speckle_data\\hd52721\\040320\\694\\result_ref\\'
#np.save(path + 'f_ar.npy',f_ar)
#np.save(path + 'I1_ar.npy',I1_ar)
#np.save(path + 'dm21_ar.npy',dm21_ar)
#np.save(path + 'dm31_ar.npy',dm31_ar)
#np.save(path + 'r12_ar.npy',r12_ar)
#np.save(path + 'r13_ar.npy',r13_ar)
#np.save(path + 'psi2_ar.npy',psi2_ar)

##___________________loading_data_from_folder_path_______________
#path = 'D:\\Speckle_data\\hd52721\\040320\\694\\result_ref\\'
#f_ar = np.load(path + 'f_ar.npy')
#I1_ar = np.load(path + 'I1_ar.npy')
#dm21_ar = np.load(path + 'dm21_ar.npy')
#dm31_ar = np.load(path + 'dm31_ar.npy')
#r12_ar = np.load(path + 'r12_ar.npy')
#r13_ar = np.load(path + 'r13_ar.npy')
#psi2_ar = np.load(path + 'psi2_ar.npy')
#psi3_ar = np.load(path + 'psi3_ar.npy')
#x2_ar = np.load(path + 'x2_ar.npy')
#y2_ar = np.load(path + 'y2_ar.npy')
#x3_ar = np.load(path + 'x3_ar.npy')
#y3_ar = np.load(path + 'y3_ar.npy')

#______________plot_fiting_results_depend_on_freq______________
freq1 = 30; freq2 = 160
freq_ar = f_ar
dm_mask21 = mask_freq(dm21_ar,freq_ar,freq1,freq2)
dm_mask31 = mask_freq(dm31_ar,freq_ar,freq1,freq2)
psi2_mask = mask_freq(psi2_ar,freq_ar,freq1,freq2)
psi3_mask = mask_freq(psi3_ar,freq_ar,freq1,freq2)
r12_mask = mask_freq(r12_ar,freq_ar,freq1,freq2)
r13_mask = mask_freq(r13_ar,freq_ar,freq1,freq2)
I1_mask = mask_freq(I1_ar,freq_ar,freq1,freq2)
x2_mask = mask_freq(x2_ar,freq_ar,freq1,freq2)
y2_mask = mask_freq(y2_ar,freq_ar,freq1,freq2)
x3_mask = mask_freq(x3_ar,freq_ar,freq1,freq2)
y3_mask = mask_freq(y3_ar,freq_ar,freq1,freq2)

plt.figure(figsize=(10,6))
plt.subplot(2,2,1)
plt.scatter(freq_ar, dm_mask21)
plt.title('dm2 vs upper bound freq')
plt.subplot(2,2,2)
plt.scatter(freq_ar, dm_mask31)
plt.title('dm3 vs upper bound freq')
plt.figure()
plt.scatter(freq_ar, I1_mask)
plt.title('I1 vs upper bound freq')
plt.figure(figsize=(10,6))
plt.scatter(freq_ar, r12_mask)
plt.title('RHO2 vs upper bound freq')
plt.figure()
plt.scatter(freq_ar, r13_mask)
plt.title('RHO3 vs upper bound freq')
plt.figure()
plt.scatter(freq_ar, psi2_mask)
plt.title('PSI2 vs upper bound freq')
plt.figure()
plt.scatter(freq_ar, psi3_mask)
plt.title('PSI3 vs upper bound freq')
plt.show()

#________________errors_estimating____________________________________________
I1 = np.min(I1_mask)
std_I1 = np.std(I1_mask)
x1 = 256
std_x1 = 1e-9
y1 = 256
std_y1 = 1e-9
x2 = np.mean(x2_mask)
std_x2 = np.std(x2_mask)
y2 = np.mean(y2_mask)
std_y2 = np.std(y2_mask)
x3 = np.mean(x3_mask)
std_x3 = np.std(x3_mask)
y3 = np.mean(y3_mask)
std_y3 = np.std(y3_mask)
dm21 = np.nanmean(dm_mask21)
er_dm21 = np.nanstd(dm_mask21)
dm31 = np.nanmean(dm_mask31)
er_dm31 = np.nanstd(dm_mask31)

#___________________________first_way___________________________________
rho2 = np.sqrt((x2-256)**2 + (y2-256)**2)
er_rho2 = np.sqrt(((x2-256)*std_x2/rho2)**2 + ((y2-256)*std_y2/rho2)**2)
rho3 = np.sqrt((x3-256)**2 + (y3-256)**2)
er_rho3 = np.sqrt(((x3-256)*std_x3/rho3)**2 + ((y3-256)*std_y3/rho3)**2)
psi2 = np.arctan2(y2-256,x2-256)*180/np.pi
er_psi2 = np.sqrt((x2*std_y2/rho2**2)**2 + (y2*std_x2/rho2**2)**2)
psi3 = np.arctan2(y3-256,x3-256)*180/np.pi
er_psi3 = np.sqrt((x3*std_y3/rho3**2)**2 + (y3*std_x3/rho3**2)**2)

#_______________________printing_dm_rho_psi_results_______________________________
print('from', freq1, 'to', freq2, 'with step', bandwidth)
print('dm21: ', dm21, '+-', er_dm21)
print('dm31: ', dm31, '+-', er_dm31)
print('rho2: ', rho2, '+-', er_rho2)
print('rho3: ', rho3, '+-', er_rho3)
print('psi2: ', psi2,'or',psi2+180, '+-', er_psi2)
print('psi3: ', psi3,'or',psi3+180, '+-', er_psi3)

#_______________________comparing_data_and_model___________________________
model = triple_spectrum_2d_min(I1,dm21,dm31,x1,y1,x2,y2,x3,y3) # draw THIS!
fig = plt.figure()
plt.plot(slice_image(ring_mask(ps,freq1,freq2),256,256,x2,y2))
plt.plot(slice_image(ring_mask(model,freq1,freq2),256,256,x2,y2))
plt.title('Slice')
plt.show()

#_______________________parallactic_angle__________________________
pi = np.pi
fi = 43.6467 # BTA latitude in degr
firad = fi * pi / 180. # BTA latitude in radians
rah = 7
ram = 2
ras = (45.08+45.15)/2
sth = 7
stm = (40.6+43.5)/2
sts = 0
ded = -11
dem = 20
des = (05.0+05.0)/2
s = sth + stm / 60. + sts / (60. * 60)
r = rah + ram / 60. + ras / (60. * 60)
if ded >=0:
    d = (ded+dem/60. + des/(60.*60)) * pi / 180.
else:
    d = -1 * (abs(ded) + dem/60. + des/(60.*60)) * pi/180.
t = ((s - r) * 15.) * pi / 180.
parallactic_angle = (np.arctan(np.sin(t) / (np.tan(firad) * np.cos(d) - np.sin(d) * np.cos(t)))) * 180./pi
print('parallactic_angle: ', parallactic_angle, '[deg]')

#_______________nonhorizontality_and_scale___________________________________________________
nonhorizontality = 1.5
d_nonhorizontality = 0.01
scale = 0.00885267819 #(arcsec/px)
er_scale = 5.16421857e-05

#___________________calculating_theta_from_psi_______________________________________________
theta2 = parallactic_angle + nonhorizontality + psi2
theta3 = parallactic_angle + nonhorizontality + psi3
er_theta2 = np.sqrt((er_psi2)**2 + (d_nonhorizontality)**2)
er_theta3 = np.sqrt((er_psi3)**2 + (d_nonhorizontality)**2)

#_______________________rho_scaling___________________________________________________________
rho2_arcsec = rho2*scale
rho3_arcsec = rho3*scale
er_rho2_arcsec = rho2_arcsec*np.sqrt((er_rho2/rho2)**2 + (er_scale/scale)**2)
er_rho3_arcsec = rho3_arcsec*np.sqrt((er_rho3/rho3)**2 + (er_scale/scale)**2)

#_________________________printing_theta_rho_arcsec_dm_results
print('theta2: ', theta2,(theta2+180), '+-', er_theta2, '[deg]')
print('theta3: ', theta3,(theta3+180), '+-', er_theta3, '[deg]')
print('rho12: ', rho2_arcsec, '+-', er_rho2_arcsec, '[arcsec/px]')
print('rho13: ', rho3_arcsec, '+-', er_rho3_arcsec, '[arcsec/px]')
print('dm21: ', dm21, '+-', er_dm21)
print('dm31: ', dm31, '+-', er_dm31)