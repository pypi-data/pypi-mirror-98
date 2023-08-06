"""Panels to interact with the SIGEPH file."""
import param
import panel as pn
import panel.widgets as pnw
import bokeh.models.widgets as bkw

from .core import PanelWithElectronBands #, PanelWithEbandsRobot


class SigEPhFilePanel(PanelWithElectronBands):
    """
    Panel with widgets to interact with a |SigEphFile|.
    """

    plot_plot_qpsolution_btn = pnw.Button(name="Plot Sigma_nk", button_type='primary')

    def __init__(self, sigeph, **params):
        super().__init__(**params)
        self.sigeph = sigeph

        self.sigma_spin_select = pn.widgets.Select(name="Spin index", options=list(range(sigeph.nsppol)))
        self.sigma_kpoint_select = pn.widgets.Select(name="Kpoint in Sigma_nk",
                options={"[%d]: %s" % (ik, repr(k)): ik for ik, k in enumerate(sigeph.sigma_kpoints)})

        #sigma_band_select  = param.ObjectSelector(default=0, objects=[0], doc="Band index in sigma_nk")

    @property
    def ebands(self):
        """|ElectronBands|."""
        return self.sigeph.ebands

    def plot_lws(self):
        # Insert results in grid.
        gspec = pn.GridSpec(sizing_mode='scale_width')
        for i, rta_type in enumerate(("serta", "mrta")):
            fig = self.sigeph.plot_lws_vs_e0(rta_type=rta_type, **self.fig_kwargs)
            gspec[i, 0] = fig
            fig = self.sigeph.plot_tau_vtau(rta_type=rta_type, **self.fig_kwargs)
            gspec[i, 1] = fig

        return gspec

    def plot_qpgaps(self):
        # Insert results in grid.
        gspec = pn.GridSpec(sizing_mode='scale_width')

        for i, qp_kpt in enumerate(self.sigeph.sigma_kpoints):
            fig = self.sigeph.plot_qpgaps_t(qp_kpoints=qp_kpt, qp_type="qpz0", **self.fig_kwargs)
            gspec[i, 0] = fig
            fig = self.sigeph.plot_qpgaps_t(qp_kpoints=qp_kpt, qp_type="otms", **self.fig_kwargs)
            gspec[i, 1] = fig

        return gspec

    def plot_qps_vs_e0(self):
        return self._mp(self.sigeph.plot_qps_vs_e0(**self.fig_kwargs))

    @param.depends('plot_plot_qpsolution_btn.clicks')
    def plot_qpsolution_sk(self):
        if self.plot_plot_qpsolution_btn.clicks == 0: return
        fig = self.sigeph.plot_qpsolution_sk(self.sigma_spin_select.value, self.sigma_kpoint_select.value,
                                             itemp=0, with_int_aw=True,
                                             ax_list=None, xlims=None, fontsize=8, **self.fig_kwargs)
        return self._mp(fig)

    def get_panel(self):
        """Return tabs with widgets to interact with the DDB file."""
        tabs = pn.Tabs(); app = tabs.append
        app(("Summary", pn.Row(bkw.PreText(text=self.sigeph.to_string(verbose=self.verbose),
                               sizing_mode="scale_both"))))
        #app(("e-Bands", pn.Row(self.get_plot_ebands_widgets(), self.on_plot_ebands_btn)))

        # Build different tabs depending on the calculation type.
        if self.sigeph.imag_only:
            app(("LWS", self.plot_lws))

        else:
            app(("QP-gaps", self.plot_qpgaps))
            app(("QP_vs_e0", self.plot_qps_vs_e0))
            app(("QPSolution", pn.Row(
                pn.Column("# Quasiparticle solution",
                          self.sigma_spin_select,
                          self.sigma_kpoint_select,
                          self.plot_plot_qpsolution_btn),
                self.plot_qpsolution_sk)
            ))

        return tabs
