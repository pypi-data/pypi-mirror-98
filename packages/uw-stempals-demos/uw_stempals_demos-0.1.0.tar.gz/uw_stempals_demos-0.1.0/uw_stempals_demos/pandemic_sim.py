import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

# set animation backends
rc("animation", html="jshtml")
rc("animation", embed_limit=60)


def pandemicSim(
    N: int = 50,
    Nsick: int = 1,
    pVacc: float = 0.0,
    pMask: float = 50.0,
    qMask: float = 75.0,
    c: float = 1.0,
    v: float = 1.0,
    L: float = 1.0,
    tRecover: int = 200,
    tTotal: int = 550,
    seed: int = 0,
) -> animation.FuncAnimation:
    """
    Parameters
    ----------
    N : int, default=50
        Total number of people in the simulation. Must be a positive integer.
    Nsick : int, default=1
        Number of people sick at the beginning. Must be a positive integer < N.
    pVacc : float, default=0
        Percent of people vaccinated at the beginning. Must be a float between 0 and 100.
    pMask : float, default=50
        Percent of people wearing masks. Must be a float between 0 and 100.
    qMask : float, default=75
        Quality of the masks in percent reduction of contagiousness. Must be a float
        between 0 and 100.
    c : float, default=1
        The contagiousness of the disease. Must be a positive float.
    v : float, default=1
        Speed of the people. Must be a positive float
    L : float, default=1
        Side length of the box the people move in. Must be a positive float.
        Note that technically they are moving on the surface of a 2-torus that cannot
        be embedded in R^3. This is the torus circumference in both directions.
    tRecover : int, default=200
        The time to recover from the disease. Must be a positive integer.
    tTotal : int, default=550
        The total time of the simulation. Must be a positive integer.
    seed : int, default=0
        The random seed that determines the initial conditions and the paths walked
        by the people during the simulation.

    Returns
    -------
    anim : matplotlib.animation.FuncAnimation
    """

    # --------------------------
    # validate parameter values
    # --------------------------
    assert isinstance(N, int) & (N > 0), "N must be a positive integer."
    assert isinstance(Nsick, int) & (
        Nsick >= 0
    ), "Nsick must be a non-negative integer."
    assert (pVacc >= 0) & (pVacc <= 100), "pVacc must be between 0 and 100."
    assert (pMask >= 0) & (pMask <= 100), "pMask must be between 0 and 100."
    assert (qMask >= 0) & (qMask <= 100), "qMask must be between 0 and 100."
    assert c >= 0, "c must be non-negative."
    assert v >= 0, "v must be non-negative."
    assert L > 0, "L must be positive."
    assert isinstance(tRecover, int) & (
        tRecover >= 0
    ), "tRecover must be a non-negative integer."
    assert isinstance(tTotal, int) & (tTotal > 0), "tTotal must be a positive integer."
    assert isinstance(seed, int) & (seed >= 0), "seed must be non-negative."

    # -----------------------
    # set initial conditions
    # -----------------------
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, L, size=(N, 2))  # initial positions
    phi = rng.uniform(0, 2 * np.pi, size=N)  # initial directions
    Nvacc = int(pVacc / 100 * N)  # number of vaccinated people
    Nnormal = N - Nsick - Nvacc  # number of normal people
    Nmasked = int(pMask / 100 * N)  # number of masked people
    status = Nnormal * ["normal"] + Nsick * ["sick"] + Nvacc * ["vaccinated"]
    status = rng.permutation(np.array(status, dtype="<U10"))  # initial statuses
    masked, unmasked = np.split(rng.permutation(np.arange(N)), [Nmasked])
    recover_counter = np.zeros(N)
    recover_counter[status == "sick"] = 1  # days since infected for each person

    # -----------------
    # setup the figure
    # -----------------
    fig_inches = 8
    wpad, hpad, mpad = 0.1, 0.15, 0.1
    wsubplot = (1 - 2 * wpad - mpad) / 2
    hsubplot = 1 - 2 * hpad
    fig = plt.figure(figsize=(fig_inches, fig_inches / 2), dpi=150)
    ax1 = fig.add_axes(
        [wpad, hpad, wsubplot, hsubplot], xlim=(0, L), ylim=(0, L), xticks=[], yticks=[]
    )
    ax2 = fig.add_axes(
        [wpad + wsubplot + mpad, hpad, wsubplot, hsubplot],
        xlim=(0, tTotal),
        ylim=(0, N),
    )
    ax2.set(xlabel="Time", ylabel="Number of sick people")

    # bubble colors for each status
    colors = {
        "normal": "cornflowerblue",
        "sick": "tomato",
        "vaccinated": "orange",
        "recovered": "mediumseagreen",
    }

    # set sizes of plotting elements
    r_bbl = 0.04 * np.sqrt(c) * np.ones(N)  # radius of the unmasked bubbles
    r_bbl[masked] *= np.sqrt(1 - qMask / 100)  # radius of masked bubbles
    s_bbl = (72 * 2 * r_bbl * fig_inches * wsubplot / L) ** 2 * np.ones(N)
    s_unmasked_ppl = 3 / L ** 2
    s_masked_ppl = 10 / L ** 2

    # bubbles around people
    bbl = ax1.scatter(
        x[:, 0], x[:, 1], c=np.vectorize(colors.get)(status), s=s_bbl, alpha=0.5
    )
    # markers for people
    unmasked_ppl = ax1.scatter(x[unmasked, 0], x[unmasked, 1], c="k", s=s_unmasked_ppl)
    masked_ppl = ax1.scatter(
        x[masked, 0], x[masked, 1], c="k", s=s_masked_ppl, marker="x"
    )
    # track number of sick people
    N_currently_sick, N_total_sick = [Nsick], [Nsick]
    (currently_sick_ppl,) = ax2.plot(N_currently_sick, label="Currently")
    (total_sick_ppl,) = ax2.plot(N_total_sick, label="Total")
    ax2.legend()

    plt.close()

    # ------------------------------------------------------
    # define a function to perform a step of the simulation
    # ------------------------------------------------------
    def step(n):
        # step forward
        nonlocal x, phi
        phi = rng.vonmises(phi, 10)
        V = v / 100 * np.vstack([np.cos(phi), np.sin(phi)])
        x = (x + V.T) % L

        # new infections
        if "normal" in status:
            normal = np.where(status == "normal")[0]
            sick = np.where(status == "sick")[0]

            # calculate square distances of sick people to normal people
            d2 = np.sum((x[sick, None] - x[normal]) ** 2, axis=-1)

            # infect!
            too_close = (
                ((d2 > 0) & (d2 < r_bbl[sick, None] ** 2))
                .squeeze()
                .astype(int)
                .reshape(-1, len(normal))
            )
            if too_close.ndim > 1:
                too_close = too_close.sum(axis=0)
            new_cases = normal[too_close > 0]
            status[new_cases] = "sick"

        # record the number of sick people
        N_currently_sick.append(np.where(status == "sick")[0].size)
        N_total_sick.append(
            np.where((status == "sick") | (status == "recovered"))[0].size
        )

        # update the plots
        bbl.set_offsets(x)
        bbl.set_color(np.vectorize(colors.get)(status))
        unmasked_ppl.set_offsets(x[unmasked])
        masked_ppl.set_offsets(x[masked])
        currently_sick_ppl.set_data(np.arange(len(N_currently_sick)), N_currently_sick)
        total_sick_ppl.set_data(np.arange(len(N_total_sick)), N_total_sick)

        # recovery
        status[recover_counter > tRecover] = "recovered"
        recover_counter[status == "sick"] += 1

        return bbl, unmasked_ppl, masked_ppl, currently_sick_ppl, total_sick_ppl

    # ---------------------
    # create the animation
    # ---------------------
    anim = animation.FuncAnimation(fig, step, frames=tTotal, interval=20, blit=True)

    return anim
