__authors__ = """Dylan Marshall, Umut Eser"""

# native libs
import os, sys
# external libs
import numpy as np
import pandas as pd


################################################################################
################################################################################


def main(sc_N_states=[
    "N_wt",
    "N_ko_chd1",
    # "N_ko_ino80",
    "N_ko_isw1",
    "N_ko_isw2",
    "N_ko_rsc",
    "N_ko_spt6-1004",
    "N_ko_spt6-YW"
  ]):
  """ collate high throughput predictions to pandas dataframe format

  >>> python3.6 collate_outputs.py \
  < collated_dir > < outputs_dir >  < inp_mode > < run_mode >"""
  # input mode / run mode - collation parameters
  collated_dir = str(sys.argv[1])
  outputs_dir = str(sys.argv[2])
  inp_mode = str(sys.argv[3])
  run_mode = str(sys.argv[4])
  # input mode specific dataframes
  output_dfs = {
    x.split(".")[0]: pd.read_csv(collated_dir + x)
      for x in os.listdir(collated_dir)
        if (inp_mode in x) and ("output" in x)
  }
  # load predictions according to input mode and run mode
  preds = {
    x.split(".")[0]: np.load(outputs_dir + x)
      for x in os.listdir(outputs_dir)
        if (inp_mode in x) and (run_mode in x)
  }
  # combine K. lactis
  raw_outputs = {
    "_".join(["kl", inp_mode, run_mode]): np.concatenate([
      np.expand_dims(preds[y].item().get("kl").flatten(), 1)
        for y in preds.keys()
    ], 1)
  }
  # combine S. cerevisiae predictions
  raw_outputs.update({
    "_".join(["sc", state, inp_mode, run_mode]): np.concatenate(list({
      seqid: np.concatenate([np.expand_dims(
        preds[x].item().get("sc").get(state).flatten(), 1)
          for x in preds.keys() if x.split("_")[7] == seqid
      ], 1) for seqid in np.arange(1, 17).astype("str")
    }.values()), 0) for state in sc_N_states
  })
  # mean and variance of K. lactis predictions
  for species in ["kl"]:
    output_dfs["_".join([species, inp_mode, "output_df"])][
      "_".join([inp_mode, run_mode, "mean"])
    ] = np.average(raw_outputs["_".join([species, inp_mode, run_mode])], 1)
    output_dfs["_".join([species, inp_mode, "output_df"])][
      "_".join([inp_mode, run_mode, "variance"])
    ] = np.var(raw_outputs["_".join([species, inp_mode, run_mode])], 1)
  # mean and variance of S. cerevisiae predictions
  for state in sc_N_states:
    output_dfs["_".join(["sc", inp_mode, "output_df"])][
      "_".join([state, inp_mode, run_mode, "mean"])
    ] = np.average(raw_outputs["_".join(["sc", state, inp_mode, run_mode])], 1)
    output_dfs["_".join(["sc", inp_mode, "output_df"])][
      "_".join([state, inp_mode, run_mode, "variance"])
    ] = np.var(raw_outputs["_".join(["sc", state, inp_mode, run_mode])], 1)
  # save
  for df in output_dfs.keys():
    output_dfs[df].to_csv(collated_dir + df + ".csv")


if __name__=='__main__':
  main()


###############################################################################
###############################################################################
