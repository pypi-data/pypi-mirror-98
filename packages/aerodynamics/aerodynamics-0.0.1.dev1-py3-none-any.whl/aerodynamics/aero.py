# aerodynamics 0.0.1

# @author: dilara ozev, ethem yilmaz


"""
    velocity : relative velocity of the fluid (m/s)
    d_vis : dynamic viscosity (Ns/m^2)
    k_vis: kinematic viscosity  (m^2/s)
    rho : density (kg / m^3)
    re: reynolds number
    mach: mach number
"""



def reNumber_kinematic(velocity, ch_length , k_vis):
    """
    Reynolds Number = (Velocity * Characteristic Length)/ Kinematic Viscosity

    Parameters
    ----------
    velocity : Relative Viscousity of the Fluid          m/s
    ch_length : Characteristic length of the solid       m
    k_vis : Kinematic Viscosity of the Fluid           (m^2/s)
        

    Returns
    -------
    re : Reynolds Number                                (dimensionless)
        

    """
    re = (velocity * ch_length ) /  k_vis
    return re

def reNumber_dynamic(velocity, ch_length, rho , d_vis): 
    """
    Reynolds Number = (Fluid_density * Velocity * Characteristic Length)/ Dynamic Viscosity

    Parameters
    ----------
    velocity : Relative Viscousity of the Fluid       m/s
    ch_length : Characteristic length of the solid    m
    rho: Density of the air                          (kg / m^3)
    d_vis : Dynamic Viscosity of the Fluid          (N*s/m^2)
        

    Returns
    -------
    re : Reynolds Number                            (dimensionless)
        

    """    
    re = (velocity * rho * ch_length) /  d_vis
    return re



def speed_of_sound_ideal(adiabatic_constant = 1.66, gas_constant = 287.05, molecular_mass_gas = 0.0289647, absolute_temperature = 298.15):
    """
    Speed of sound in ideal gases

    Formula
    ----------
    
    ((adiabatic_constant*gas_constant*absolute_temperature)/molecular_mass_gas)**(1/2)

    Parameters
    ----------
    R = the universal gas constant = 8.314 J/mol K,
    T = the absolute temperature in terms of Kelvin = 298.15K
    M = the molecular weight of the gas in kg/mol = 0.0289647
    γ = the adiabatic constant, characteristic of the specific ideal gas = 1.66

    Returns
    -------
    speed of sound

    """
    return ((adiabatic_constant*gas_constant*absolute_temperature)/molecular_mass_gas)**(1/2)
    
    
    
def speed_of_sound_air(Temperature_celsius=23.15):
    """
    Calculates speed of sound in the dry air
    
    Formula
    ----------
    
    v = 331 + 0.6*T_c

    Parameters
    ----------
    Temperature_celsius = Temperature in terms of celsius

    Returns
    -------
    speed of sound in the dry air

    """
    return (331+Temperature_celsius*0.6)
       
    
    
    
    
def mach_number(speed_of_vehicle ,s_sound=341):
    """
    

    Parameters
    ----------
    speed_of_vehicle: speed of vehicle in terms of m/s
    s_sound : Speed of sound. The default is 341 m/s.

    Returns
    -------
    mach = mach number

    """
    
    return speed_of_vehicle/s_sound















