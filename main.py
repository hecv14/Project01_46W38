# %%

def simple_power(wsp_input, pow_rated = 15, wsp_cutin = 3, wsp_rated = 11, wsp_cutout = 25, interp_method="linear"):
    """simple_power is used to roughly interpolate the power in the curve of a
    variable speed WTG. A linear and a cubic interpolation option are given.

    Args:
        wsp_input (float): wind speed for the power will be estimated.
        pow_rated (float, optional): rated power. Defaults to 15 MW.
        wsp_cutin (float, optional): cut-in wind speed. Defaults to 3 m/s.
        wsp_rated (float, optional): rated wind speed. Defaults to 11 m/s.
        wsp_cutout (float, optional): cut-out wind speed. Defaults to 25 m/s.
        interp_method (str, optional): interpolation method. Defaults to "linear".

    Returns:
        pow_out: interpolated power for the wsp_input
    """
    # no need to interpolate below wsp_cutin
    if wsp_input < wsp_cutin:
        pow_out = 0
    elif wsp_cutin <= wsp_input < wsp_rated:
        # using match case here to avoid too many ifs
        match interp_method:
            case "linear":
                g_fwsp = (wsp_input - wsp_cutin)/(wsp_rated - wsp_cutin)
            case "cubic":
                # g_fwsp is the weighting function pow_out / pow_rated as f(wsp)
                g_fwsp = (wsp_input**3 )/(wsp_rated**3)
            case _:
                print('WARNING interpolation method not recognized, will use "linear"')
                g_fwsp = (wsp_input - wsp_cutin)/(wsp_rated - wsp_cutin)
        pow_out = g_fwsp * pow_rated
    elif wsp_rated <= wsp_input < wsp_cutout:
        pow_out = pow_rated
    else: # wind speeds above cutout
        pow_out = 0
    return pow_out


# %%
