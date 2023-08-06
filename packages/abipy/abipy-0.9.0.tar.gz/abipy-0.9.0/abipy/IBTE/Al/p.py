#!/usr/bin/env python

from abipy.abilab import RtaRobot

self = RtaRobot.from_dir(".")
print(self)

new_labels = ["k = q = " + str(abifile.ebands.kpoints.ksampling.mpdivs) for abifile in self.abifiles]
print(new_labels)

self.change_labels(new_labels)

import matplotlib.pyplot as plt
#self.plot_ibte_vs_rta_rho()
fig = self.plot_ibte_mrta_serta_conv(title="Al")
fig.suptitle("Al")
plt.show()
