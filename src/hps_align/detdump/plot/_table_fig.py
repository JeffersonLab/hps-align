"""construct different kinds of figures with tables of subplots"""

def _local(data_items, output_file, title = None, **kwargs):
    """the local coordinate system is plotted in a 2x4 grid where
    the top row is translations, the bottom row is rotations, and
    the last entry in the bottom row is for structure constants"""

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(
        nrows = 2,
        ncols = 4,
        gridspec_kw = dict(
            wspace = 0.2,
            hspace = 0.3,
        )
    )
    fig.set_size_inches(17,8)

    for tr, i_tr in [('t',1),('r',2)]:
        for uvw, i_uvw in [('u',1),('v',2),('w',3)]:
            ax = axes[i_tr-1][i_uvw-1]
            for name, df in data_items:
                sl = (df.t_r == i_tr)&(df.u_v_w == i_uvw)
                ax.scatter(
                    df[sl].parameter.apply(str),
                    df[sl].value*1000,
                    label = name if (i_tr == 1 and i_uvw == 1) else '_no_legend'
                )
            ax.set_xticks(
                ax.get_xticks(),
                ax.get_xticklabels(),
                rotation=90,
                fontsize='xx-small'
            )
            ax.grid(axis='x', alpha=0.5)
            ax.axhline(0., color='gray')
            ax.set_title(f'{tr}{uvw}')
            if i_uvw == 1:
                if i_tr == 1:
                    ax.set_ylabel('$\mu m$')
                else:
                    ax.set_ylabel('mrad')

    axes[0][-1].axis('off')

    for name, df in data_items:
        axes[1][-1].scatter(
            df[~df.individual].parameter.apply(str),
            df[~df.individual].value*1000
            )
    axes[1][-1].axhline(0., color='gray')
    axes[1][-1].grid(axis='x', alpha='0.5')
    axes[1][-1].set_title('Structure Constants')

    fig.legend(
        title = title,
        loc = 'lower left',
        bbox_to_anchor = (0.75, 0.6)
    )
    fig.savefig(output_file)
    plt.clear()


def _global(data_items, output_file, title = None, which='hps', **kwargs):
    """the global coordinate system is plottined in a 3x2 grid
    where the first column is position and the second column is
    euler angles. The rows go through x, y, z."""

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(
        nrows = 3,
        ncols = 2,
        sharex = 'col'
    )
    fig.set_size_inches(17,8)

    for i_c, c in enumerate(['x','y','z']):
        for i_tr, tr in enumerate([which,'theta']):
            # go through coordinates down columns and
            # and position/rotation across rows
            ax = axes[i_c][i_tr]
            for name, data in data_items:
                ax.scatter(
                    data.sensor,
                    data[f'{tr}{c}']*1000,
                    label = name if i_c==0 and i_tr == 0 else '_no_legend'
                )
            if i_tr == 0:
                ax.set_ylabel(f'{c.upper()} [$\mu$m]')
            else:
                ax.set_ylabel(f'$\\theta_{c}$ [mrad]')
            ax.axhline(0.0, color='gray')
            ax.grid(axis='x')
            if c == 'x':
                if i_tr == 0:
                    if tr == 'hps':
                        ax.set_title('HPS Global Position')
                    else:
                        ax.set_title('SVT Global Position')
                else:
                    ax.set_title('Euler Angle\n$\\theta_x = atan(v_z, w_z)$, $\\theta_y = -asin(u_z)$, $\\theta_z = atan(u_y, u_x)$')
            if c == 'z':
                ax.set_xticks(
                    ax.get_xticks(),
                    ax.get_xticklabels(),
                    rotation=90
                )
    fig.legend(
        title = title,
        loc = 'lower center',
        bbox_to_anchor = (0.5, 0.9)
    )
    fig.savefig(output_file, bbox_inches='tight')
    plt.close()
