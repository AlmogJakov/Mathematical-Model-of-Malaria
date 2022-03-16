import numpy as np


def arnon_model(init_vals, params, m_params, t):
    Eh_0, Ih_0, Em_0, Im_0 = init_vals
    Eh = [Eh_0]
    Ih = [Ih_0]
    Em = [Em_0]
    Im = [Im_0]

    d, eta_m, eta_p, n_m, s, c_s, mos, hum = m_params
    c_total = s * c_s
    k = np.zeros((eta_p,), dtype=int)
    k[0] = n_m
    f = []
    eggs_total = 0

    a, b, c, r, mu1_year, mu2, tau_m, tau_h = params
    mu1_day = mu1_year / 365
    e1 = np.e ** (- (r + mu1_day) * tau_h)
    e2 = np.e ** (- mu2 * tau_m)

    for time_now in range(t):
        next_g = k[(time_now % eta_p)] * mos * (1 - d)
        g = f.copy()
        g.append(next_g)
        eggs_total += next_g
        eggs_total = eggs_total - g[time_now - eta_m - 1] if time_now - eta_m - 1 > 0 else eggs_total
        p = eggs_total - c_total
        f.append(next_g)
        if p > 0:
            eggs_total = c_total
            for i in range(eta_m):
                f[t - i] = g[t - i] - (g[t - i] * p) / eggs_total
        mos = mos * (1 - d) + f[t - eta_m]
        m = mos / hum

        tm = time_now - tau_m
        th = time_now - tau_h

        Eh_th = Ih_th = Im_th = Ih_tm = Em_tm = Im_tm = 0

        if th >= 0:
            Eh_th = Eh[th]
            Ih_th = Ih[th]
            Im_th = Im[th]

        if tm >= 0:
            Ih_tm = Ih[tm]
            Em_tm = Em[tm]
            Im_tm = Im[tm]

        next_Eh = Eh[-1] + (a * b * m * Im[-1] * (1 - Eh[-1] - Ih[-1])
                            - a * b * m * Im_th * (1 - Eh_th - Ih_th) * e1
                            - r * Eh[-1] - mu1_day * Eh[-1])
        next_Ih = Ih[-1] + (a * b * m * Im_th * (1 - Eh_th - Ih_th) * e1
                            - r * Ih[-1] - mu1_day * Ih[-1])

        next_Em = Em[-1] + (a * c * Ih[-1] * (1 - Em[-1] - Im[-1])
                            - a * c * Ih_tm * (1 - Em_tm - Im_tm) * e2 - mu2 * Em[-1])

        next_Im = Im[-1] + (a * c * Ih_tm * (1 - Em_tm - Im_tm) * e2 - mu2 * Im[-1])

        Eh.append(next_Eh)
        Ih.append(next_Ih)
        Em.append(next_Em)
        Im.append(next_Im)
    return np.stack([Em, Ih, Em, Im]).T


def anderson_and_may_reproductive_number(params):
    a, b, c, m, r, mu1_year, mu2, tau_m, tau_h = params
    mu1_day = mu1_year / 365
    e1 = np.e ** (-mu2 * tau_m)
    e2 = np.e ** (-mu1_day * tau_h)
    R0 = (m * (a ** 2) * b * c * e1 * e2) / (r * mu2)
    return R0


# def get_m(params, f, t):
#     next_g = k[(time_now % eta_p)] * mos * (1 - d)
#     g = f.copy()
#     g.append(next_g)
#     eggs_total += next_g
#     eggs_total = eggs_total - g[time_now - eta_m - 1] if time_now - eta_m - 1 > 0 else eggs_total
#     p = eggs_total - c_total
#     f.append(next_g)
#     if p > 0:
#         eggs_total = c_total
#         for i in range(eta_m):
#             f[t - i] = g[t - i] - (g[t - i] * p) / eggs_total
#     mos = mos * (1 - d) + f[t - eta_m]
#     return mos / hum
