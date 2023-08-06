import logging
from astropy import units as u

# Assumed source evolution is highly negative
eta = -2


def tde_evolution_sun_15(z):
    """TDE redshift evolution from Sun et. al. 2015 (https://arxiv.org/abs/1509.01592)

    :param z: Redshift
    :return: f(z)
    """
    evolution = ((1 + z)**(0.2 * eta) + ((1 + z)/1.43)**(-3.2 * eta) +
                 ((1 + z)/2.66)**(-7 * eta)
                 )**(1./eta)
    return evolution


def biehl_jetted_evolution(z, m=-3.):
    """Evolution of TDEs assumed by Biehl et al. 2018 is 0.1 per Gpc per year
    (10^-10 per Mpc per year). The source evolution is assumed to be
    negative, with an index m=3, though the paper also considers indexes up
    to m=0 (flat). More details found under https://arxiv.org/abs/1711.03555

    :param z: Redshift
    :param m: Index of evolution
    :return: Jetted TDE rate
    """
    rate = (1 + z)**m
    return rate


tde_evolutions = {
    "sun_15": (tde_evolution_sun_15, "https://arxiv.org/abs/1509.01592"),
    "biehl_18_jetted": (biehl_jetted_evolution, "https://arxiv.org/abs/1711.03555")
}


def get_tde_evolution(evolution_name=None, **kwargs):
    """Returns a TDE evolution as a function of redshift

    :param evolution_name: Name of chosen evolution
    :return: Normalised evolution, equal to 1 at z=0
    """

    if evolution_name is None:
        logging.info("No evolution specified. Assuming default evolution.")
        evolution_name = "sun_15"

    if evolution_name not in tde_evolutions.keys():
        raise Exception(f"Evolution name '{evolution_name}' not recognised. "
                        f"The following source evolutions are available: {tde_evolutions.keys()}")
    else:
        evolution, ref = tde_evolutions[evolution_name]
        logging.info(f"Loaded evolution '{evolution_name}' ({ref})")

    normed_evolution = lambda x: evolution(x, **kwargs)/evolution(0.0, **kwargs)
    return normed_evolution

local_tde_rates = {
    "sun_15_jetted": (3 * 10 **-11 / (u.Mpc**3 * u.yr), "https://arxiv.org/abs/1706.00391"),
    "van_velzen_18": (8 * 10**-7 / (u.Mpc**3 * u.yr), "https://arxiv.org/abs/1707.03458"),
    "biehl_18_jetted": (10**-10 / (u.Mpc**3 * u.yr), "https://arxiv.org/abs/1711.03555"),
    "kochanek_16": (1.5 * 10**-6 / (u.Mpc**3 * u.yr), "https://arxiv.org/abs/1601.06787")
}

def get_local_tde_rate(rate_name=None):
    """Returns local TDE rate

    :param rate_name: Name of chosen evolution
    :return: Normalised evolution, equal to 1 at z=0
    """

    if rate_name is None:
        logging.info("No rate specified. Assuming default rate.")
        rate_name = "van_velzen_18"

    if rate_name not in local_tde_rates.keys():
        raise Exception(f"Rate name '{rate_name}' not recognised. "
                        f"The following source evolutions are available: {local_tde_rates.keys()}")
    else:
        local_rate, ref = local_tde_rates[rate_name]
        logging.info(f"Loaded rate '{rate_name}' ({ref})")

    return local_rate.to("Mpc-3 yr-1")

def get_tde_rate(evolution_name=None, rate_name=None, **kwargs):
    """Load a TDE rate as a function of redshift. This is a product of
    a TDE evolution and a TDE local rate.

    :param evolution_name: Name of TDE evolution to use
    :param rate_name: Name of TDE local rate to use
    :return: TDE Rate function
    """
    normed_evolution = get_tde_evolution(evolution_name, **kwargs)
    local_rate = get_local_tde_rate(rate_name)
    return lambda z: local_rate*normed_evolution(z)