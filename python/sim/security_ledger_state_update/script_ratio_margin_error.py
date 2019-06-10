import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 0.1
mpl.rcParams['hatch.linewidth'] = 0.1


type = 2
if type == 1:

    # Graph 1
    r = 0.7
    low_bin = 50
    max_bin = 2000
    x = np.arange(low_bin, max_bin + low_bin, 10)
    y = np.empty(len(x))
    y.fill(r)
    d = y*(1-y)/x

    error = np.empty(len(x))
    y2 = np.empty(len(x))
    ind_d = 0
    V_match = 0
    match_found = False

    for i in range(len(d)):
        error[i] = 4.22 * math.sqrt(d[i])
        y2[i] = 0.5 + error[i]
        if y[i]-error[i] >= 0.5 and match_found is False:
            V_match = x[i]
            match_found = True
            print(V_match)
    tick_bin = int((round(max_bin, -3) - round(low_bin, -2)) / 10)
    plt.xticks(np.arange(round(low_bin, -2), round(max_bin, -3), tick_bin))
    plt.ylim(0.2, 1)
    plt.xlim(low_bin, max_bin)
    plt.xlabel('P (producers)', fontsize = 12)
    plt.ylabel('$r_1$ $\pm$ $\Delta r_1$', fontsize=15)
    plt.axhline(y=.5)
    plt.plot(x, y, 'k-', color='maroon', linestyle='--', label='_nolegend_')

    plt.plot(x, y2, 'k-', color='forestgreen', linestyle=':', label='50% + $\Delta r_1$')
    plt.fill_between(x, y-error, y+error, edgecolor='black', linewidth=0.2, hatch='///', facecolor='azure')
    props = dict(boxstyle='round', facecolor='lavenderblush', alpha=0.5)
    plt.text(0.74*x[-1], 0.4, ' $r_1$ = ' + str(int(r*100)) + '\n at 99.999% CL', verticalalignment='top', bbox=props)

    plt.legend(loc='lower right')
    plt.savefig('graph_rDeltaR_over_P_at_99.999_at_r_{}.png'.format(r))

else:


    # Graph 2
    p_full = 2000
    p_small = 200
    r = 0.6
    low_bin2 = 0
    max_bin2 = 2
    x = np.linspace(0, 1, 2)
    y = np.empty(len(x))
    y.fill(r)
    d = 4.22 * math.sqrt(r * (1-r) / p_full)
    d2 = 4.22 * math.sqrt(r * (1-r) / p_small)
    print(d)
    error = np.empty(len(x))
    error.fill(d)
    error_b = np.empty(len(x))
    error_b.fill(d2)

    x2 = np.linspace(1, 2, 2)
    y2 = np.empty(len(x2))
    y2.fill(1-r)
    error2 = np.empty(len(x2))
    error2.fill(d)
    error_b2 = np.empty(len(x2))
    error_b2.fill(d2)

    tick_bin2 = 1
    plt.xticks(np.arange(-1, 3, step=10))
    plt.ylim(0, 1)
    plt.xlim(low_bin2, max_bin2)
    # plt.xlabel('#[h($\delta_L$)] bins',fontsize=12)
    plt.ylabel('$r_{1,2} \pm \Delta r_{1,2}$',fontsize=15)
    # (99.999% confidence level)')
    plt.axhline(y=.5)
    plt.plot(x, y, color='maroon', linestyle='--', label='_nolegend_')
    plt.plot(x2, y2, color='maroon', linestyle='--', label='_nolegend_')
    plt.fill_between(x, y - error_b, y + error_b, edgecolor='black', linewidth=0.2, hatch='\\\\', facecolor='seashell', label='P={}'.format(p_small))
    plt.fill_between(x2, y2 - error_b2, y2 + error_b2, edgecolor='black', linewidth=0.2, hatch='\\\\', facecolor='seashell', label='_nolegend_')
    plt.fill_between(x, y - error, y + error, edgecolor='black', linewidth=0.2, hatch='///', facecolor='azure', label='P={}'.format(p_full))
    plt.fill_between(x2, y2-error2, y2+error2,edgecolor='black',linewidth=0.2, hatch='///', facecolor='azure',label='_nolegend_')
    #props = dict(alpha=1)
    plt.text(0.5, -0.02, '$r_1$', verticalalignment='top', fontsize=15)
    plt.text(1.5, -0.02, '$r_2$', verticalalignment='top', fontsize=15)

    plt.legend(title=' $r_1$={}% \n $\Delta r_1(P)$ (99.999% CL):'.format(int(r*100)), loc='upper right')
    #plt.show()
    plt.savefig('bar_graph_rDeltaR_at_99.999_at_r_{}.png'.format(r))


