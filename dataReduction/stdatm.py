import numpy as np

def temp(To, z):
    # Determines expected temperature as function of altitude up to 47000 meters, within the range flown by the balloon.

    # Get temperature lapse rate for altitude
    if z <= 11000:
        zi = 0
        Li = -6.5*10**-3
        Ti = To
    elif z <= 20000:
        zi = 11000
        Li = 0
        Ti = temp(To, 11000)
    elif z <= 32000:
        zi = 20000
        Li = 1*10**-3
        Ti = temp(To, 20000)
    else:
        zi = 32000
        Li = 2.8*10**-3
        Ti = temp(To, 32000)

    # Determine temperature as function of altitude
    T = Ti+Li*(z-zi)
    return T

def pres(Po, To, z):

    go = 9.80665
    Wo = 28.9644
    R = 8314.32

    # Determines expected pressure as function of altitude up to 47000 meters, within the range flown by the balloon.
    T = temp(To, z)
    if z <= 11000:
        zi = 0
        Li = -6.5*10**-3
        Pi = Po
        Ti = To
    elif z <= 20000:
        zi = 11000
        Li = 0
        # print("Po: " + str(Po))
        # print("To: " + str(To))
        Pi = pres(Po, To, 11000)
        Ti = temp(To, 11000)
    elif z <= 32000:
        zi = 20000
        Li = 1*10**-3
        Pi = pres(Po, To, 20000)
        Ti = temp(To, 20000)
    else:
        zi = 32000
        Li = 2.8*10**-3
        Pi = pres(Po, To, 32000)
        Ti = temp(To, 32000)

    # Determine pressure as function of altitude
    if Li != 0:
        # print(go)
        # print(Wo)
        # print(z)
        # print(zi)
        # print(Pi)
        # P = Pi*(Ti/T)**(go*Wo/(R*Li))
        P = Pi*np.power(Ti/T,go*Wo/(R*Li))

        # print(Pi*(Ti/T))
        # print(go*Wo/(R*Li*10**3))

        # print(Li)
        # print("Pi: " + str(Pi))
        # print("Li: " + str(Li * 10 ** 3))
        # print("Ti: " + str(Ti))
        # print("T: " + str(T))
        # print("P: " + str(P))
    else:
        # print(go)
        # print(Wo)
        # print(z)
        # print(zi)
        # print(Pi)
        P = Pi*np.exp((-go*Wo*(z-zi))/(R*Ti))
        # print(P)
    return P

# alt = np.arange(0,35000,10)
# N = len(alt)
# T = np.zeros(N)
#
# # Using 1976 standard atmosphere where Ti = 288.15 K = 15 C
#
# for j in range(N):
#     z = alt[j]
#     T[j] = temp(15, z)
#
# plt.figure(0)
# plt.plot(alt,T)
# plt.show()