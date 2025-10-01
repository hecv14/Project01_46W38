# %%
import math 

# %%
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
    # we check the wind speed range in an ascending way (starting from 0 m/s):
    if 0 <= wsp_input < wsp_cutin: # below wsp_cutin
        pow_out = 0

    elif wsp_cutin <= wsp_input < wsp_rated: # in interpolation range
        interp_method = interp_method.lower().strip() # clean the string
        if interp_method not in ["linear", "cubic"]:
            print(f'Interpolation method "{interp_method}" not recognized!')
            print('Using "linear" instead.')
            interp_method = "linear" # keep it running but warn user of change          
        match interp_method:
            case "linear":
                # g_fwsp is the weighting function pow_out / pow_rated as f(wsp)
                try:
                    g_fwsp = (wsp_input - wsp_cutin) / (wsp_rated - wsp_cutin)
                except ZeroDivisionError:
                    g_fwsp = float('nan') # keep it running but warn user
                    print("Zero Division Error: wsp_cutin cannot equal wsp_rated!")
            case "cubic":                
                try: g_fwsp = (wsp_input**3 )/(wsp_rated**3)
                except ZeroDivisionError:
                    g_fwsp = float('nan') # keep it running but warn user
                    print("Zero Division Error: wsp_rated cannot be 0!")
        # with the weighting factor find the power output
        pow_out = g_fwsp * pow_rated

    elif wsp_rated <= wsp_input < wsp_cutout: # operating at rated power
        pow_out = pow_rated

    elif wsp_input >= wsp_cutout: # WTG shut-down starting wsp_cutout
        pow_out = 0

    else: # unexpected wind speed e.g., negative
        pow_out = float('nan')
        print(f"unexpected wind speed {wsp_input}")

    return pow_out


# %%
if __name__ == '__main__':
    # Write the main script to use the function here:

# test the function with wind speeds from 0 to 1m/s above cut-out
    print('using linear interpolation.')
    for wsp in range(27):
        pow = simple_power(wsp) # linear
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

    print('using cubic interpolation.')
    for wsp in range(27):
        pow = simple_power(wsp, interp_method="cubic")
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

    print('using wrong arg. for interpolation.')
    for wsp in range(27):
        pow = simple_power(wsp, interp_method="typo") # test bad input
        print(f"{wsp}, {pow:,.2f}")
    print('\n')

    print('negative wind speed')
    simple_power(-2) # nan

# %%