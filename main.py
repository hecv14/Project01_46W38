# %%
import warnings

def simple_power(wsp_input: float | int,
                pow_rated: float | int = 15,
                wsp_cutin: float | int = 3,
                wsp_rated: float | int = 11,
                wsp_cutout: float | int = 25,
                interp_method: str ="linear"
                ) -> float | int:
    """simple_power is used to roughly interpolate the power in the curve of a
    variable speed WTG. A linear and a cubic interpolation option are given.

    Args:
        wsp_input (float): wind speed for the power will be estimated.
        pow_rated (float, optional): rated power. Defaults to 15 MW.
        wsp_cutin (float, optional): cut-in wind speed. Defaults to 3 m/s.
        wsp_rated (float, optional): rated wind speed. Defaults to 11 m/s.
        wsp_cutout (float, optional): cut-out wind speed. Defaults to 25 m/s.
        interp_method (str, optional): interpolation used. Defaults to "linear".

    Returns:
        pow_out: interpolated power for the wsp_input, same units as pow_rated.
    """
    # weighting if the interpolation is linear
    g_lin = lambda wsp_input, wsp_cutin, wsp_rated: \
    (wsp_input - wsp_cutin) / (wsp_rated - wsp_cutin) \
    if wsp_rated != wsp_cutin else float('inf')

    # if it is cubic
    g_cub = lambda wsp_input, wsp_rated: \
    (wsp_input**3 )/(wsp_rated**3) \
    if wsp_rated != 0 else float('inf')

    # no need to interpolate below wsp_cutin
    if 0 <= wsp_input < wsp_cutin:
        pow_out = 0
    elif wsp_cutin <= wsp_input < wsp_rated:
        interp_method = interp_method.lower().strip() # clean the string a bit
        # using match case here to avoid too many ifs
        match interp_method:
            case "linear":
                # g_fwsp is the weighting function pow_out / pow_rated as f(wsp)
                g_fwsp = g_lin(wsp_input, wsp_cutin, wsp_rated)
            case "cubic":                
                g_fwsp = g_cub(wsp_input, wsp_rated)
            case _:
                warnings.warn("Interpolation method unrecognized, using linear")
                g_fwsp = g_lin(wsp_input, wsp_cutin, wsp_rated)
        # with the weighting factor find the power output
        pow_out = g_fwsp * pow_rated
    elif wsp_rated <= wsp_input < wsp_cutout:
        pow_out = pow_rated
    elif wsp_input >= wsp_cutout: # wind speeds above cutout
        pow_out = 0
    return pow_out


# %%
if __name__ == '__main__':
    # Write the main script to use the function here:
    # test the function with wind speeds from 0 to 1m/s above cut-out
    print('using linear interpolation.')
    for wsp in range(26):
        pow = simple_power(wsp) # linear
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

    print('using cubic interpolation.')
    for wsp in range(26):
        pow = simple_power(wsp, interp_method="cubic")
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

    print('using wrong arg. for interpolation.')
    for wsp in range(26):
        pow = simple_power(wsp, interp_method="typo") # test bad input
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

# %%