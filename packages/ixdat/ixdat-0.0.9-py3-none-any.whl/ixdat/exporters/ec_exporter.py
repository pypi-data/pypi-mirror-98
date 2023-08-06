from .csv_exporter import CSVExporter


class ECExporter(CSVExporter):
    """A CSVExporter that by default exports potential, current, and selector"""

    @property
    def default_v_list(self):
        """The default v_list for ECExporter is V_str, J_str, and sel_str"""
        v_list = [
            self.measurement.E_str,
            self.measurement.I_str,
            self.measurement.V_str,
            self.measurement.J_str,
            self.measurement.sel_str,
        ]
        return v_list
