import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.use("Agg")


def lindemann_vs_frames(indices: np.ndarray) -> str:
    plt.figure(1)
    plt.title("Lindemann index per frame")
    plt.xlabel("Frames")
    plt.ylabel("Lindemann index")
    plt.plot(np.arange(0, len(indices)), indices, "+")
    plt.tight_layout()
    # plt.show()
    plt.savefig("lindemann_per_frame.pdf")
    return "lindemann_per_frame.pdf"
