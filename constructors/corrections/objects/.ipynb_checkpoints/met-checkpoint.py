import correctionlib
import numpy as np
import awkward as ak
from typing import Tuple


def apply_met_phi_corrections(
    events: ak.Array,
    year: str,
    cset
) -> Tuple[ak.Array, ak.Array]:
    run_ranges = {
        "2022": [355094, 359017],
        "2022EE": [359045, 362760],
    }
    if year in run_ranges:
        
        events["PuppiMET", "pt_raw"] = (
            ak.ones_like(events.PuppiMET.pt) * events.PuppiMET.pt
        )
        events["PuppiMET", "phi_raw"] = (
            ak.ones_like(events.PuppiMET.phi) * events.PuppiMET.phi
        )

        # make sure to not cross the maximum allowed value for uncorrected met
        met_pt = events.PuppiMET.pt_raw
        met_pt = np.clip(met_pt, 0.0, 6499.0)
        met_phi = events.PuppiMET.phi_raw
        met_phi = np.clip(met_phi, -3.5, 3.5)

        data_kind = "mc" if "genWeight" in events.fields else "data"
        if data_kind == "mc":
            run = np.random.randint(
                run_ranges[year][0], run_ranges[year][1], size=len(met_pt)
            )
        else:
            run = events.run
        try:
            pt_corr_file = f"pt_metphicorr_puppimet_{data_kind}"
            phi_corr_file = f"phi_metphicorr_puppimet_{data_kind}"
            
            events["PuppiMET", "pt"] = cset[pt_corr_file].evaluate(
                met_pt.to_numpy(),
                met_phi.to_numpy(),
                events.PV.npvsGood.to_numpy(),
                run,
            )
            
            events["PuppiMET", "phi"] = cset[phi_corr_file].evaluate(
                met_pt.to_numpy(),
                met_phi.to_numpy(),
                events.PV.npvsGood.to_numpy(),
                run,
            )
            
        except:
            pass


def corrected_polar_met(
    met_pt,
    met_phi,
    other_phi,
    other_pt_old,
    other_pt_new,
    positive=None,
    dx=None,
    dy=None,
) -> tuple:
    """
    helper function to compute new MET polar components after some other object pT correction.

    https://github.com/CoffeaTeam/coffea/blob/master/src/coffea/jetmet_tools/CorrectedMETFactory.py#L6
    """
    sin, cos = np.sin(other_phi), np.cos(other_phi)
    met_px = met_pt * np.cos(met_phi) - ak.sum(
        (other_pt_new - other_pt_old) * cos, axis=1
    )
    met_py = met_pt * np.sin(met_phi) - ak.sum(
        (other_pt_new - other_pt_old) * sin, axis=1
    )
    if positive is not None and dx is not None and dy is not None:
        met_px = met_px + dx if positive else x - dx
        met_py = met_py + dy if positive else y - dy

    corrected_met_pt = np.hypot(met_px, met_py)
    corrected_met_phi = np.arctan2(met_py, met_px)
    return corrected_met_pt, corrected_met_phi