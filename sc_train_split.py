__authors__ = """Dylan Marshall, Umut Eser"""

# native libs
import os, sys
# external libs
import numpy as np
import pandas as pd


################################################################################
################################################################################


def _np_5_to_3_sc(gene, data, width=1024):
  """orient extracted data in 5' --> 3' direction"""
  # get genomic and sequencing data at gene location
  seqid, strand = gene["seqid"], gene["strand"]
  start, end = gene["AUG_start"], gene["AUG_end"]
  # random boundaries for AUG - phasing
  start, end = _np_random_start_end(start, end, strand, width)
  locus = _np_get_locus_sc(seqid, start, end, strand, data)
  # ancillary information at gene location
  ancillary_df = pd.DataFrame({
    "strand": np.repeat(gene["strand"], width),
    "ID": np.repeat(gene["ID"], width),
    "seqid": np.repeat(gene["seqid"], width)
  })
  # return 5' --> 3' orientation genomic and sequencing data
  if gene["strand"] is "+":
    df = pd.concat(
      objs=(ancillary_df, locus.rename(columns={
        "NS_wt_pos": "NS_wt_sense",
        "NS_wt_neg": "NS_wt_antisense"
      })), axis=1)
  else: # gene["strand"] is "-"
    # reverse negative strand data
    for col in [
      "DS_A", "DS_T", "DS_G", "DS_C",
      "NS_wt_pos", "NS_wt_neg",
      "MS_wt_1"
    ]: locus[col] = locus[col].values[::-1]
    # flip negative strand data
    df = pd.concat(
      objs=(ancillary_df, locus.rename(columns={
        "DS_A": "DS_T",
        "DS_T": "DS_A",
        "DS_G": "DS_C",
        "DS_C": "DS_G",
        "NS_wt_pos": "NS_wt_antisense",
        "NS_wt_neg": "NS_wt_sense"
      })), axis=1)
  return df[[
    "ID", "strand", "seqid", "position",
    "DS_A", "DS_C", "DS_G", "DS_T",
    "NS_wt_sense", "NS_wt_antisense",
    "MS_wt_1"
  ]]


def _np_get_locus_sc(seqid, start, end, strand, data,
  cols=[
    "position", "seqid",
    "DS_A", "DS_C", "DS_G", "DS_T",
    "NS_wt_pos", "NS_wt_neg",
    "MS_wt_1"
  ]):
  """extract DNA sequence, NET-seq and MNase-seq data at given locus"""
  return data[
    (data["seqid"] == seqid) &
    (data["position"] >= start) &
    (data["position"] < end)
  ][cols].reset_index(drop=True) if strand is "+" else data[
      (data["seqid"] == seqid) &
      (data["position"] > start) &
      (data["position"] <= end)
    ][cols].reset_index(drop=True)


def _np_get_sc_data(columns, seqid, data):
  """get column-specific sequencing data according to seqid"""
  return np.rot90(
    data[data["seqid"] == seqid][
      columns
    ].values.reshape((-1, 1024, len(columns))), axes=(1, 2))


def _np_random_start_end(start, end, strand, width):
  """define random <width> region within AUG boundaries"""
  if strand == "+":
    start = np.random.randint(start, start + width)
    return start, start + width
  else: # strand == "-"
    end = np.random.randint(end - width, end)
    return end - width, end


def main(head_dir="/n/groups/churchman/dmm57/COLAB/", training_regions=16):
  """ TODO: modulate 'head_dir' variable
    head_dir := FIDDLE head directory
    training_regions := number of randomly sampled regions per gene"""
  # ancillary
  run = str(sys.argv[1])
  collated_dir = head_dir + "/DATA/COLLATED/"
  model_inputs_dir = head_dir + "/MODELS/INPUTS/"
  # load dataframes
  data_sc = {
    "meta_sc": pd.read_csv(collated_dir + "meta_sc.csv"),
    "gen_seq_sc": pd.read_csv(collated_dir + "gen_seq_sc.csv")
  }
  # remove unnecessary columns
  nuisance = "Unnamed: 0"
  for df in list(data_sc.keys()):
    if nuisance in data_sc[df].columns.values:
      data_sc[df].drop(nuisance, axis=1, inplace=True)
  # collate train dataframe
  sc_train_df = pd.concat([
    pd.concat([
      _np_5_to_3_sc(gene[1], data_sc["gen_seq_sc"])
        for gene in data_sc["meta_sc"].iterrows()
      ], ignore_index=True)
        for _ in range(training_regions)
    ], ignore_index=True)
  # drop extra seqid columns
  sc_train_df["SEQID"] = sc_train_df["seqid"].values[:, 0]
  sc_train_df.drop("seqid", axis=1, inplace=True)
  sc_train_df["seqid"] = sc_train_df["SEQID"].values
  sc_train_df = sc_train_df[[
    "ID", "strand", "seqid", "position",
    "DS_A", "DS_C", "DS_G", "DS_T",
    "NS_wt_sense", "NS_wt_antisense",
    "MS_wt_1"
  ]]
  # save
  sc_train_df.to_csv(collated_dir + "sc_train_df_" + run + ".csv")
  # extract train set arrays to dictionary
  sc_train_dict = {
    seqid: {
      "sc_train_ds": np.expand_dims(
        a=_np_get_sc_data(
          columns=["DS_A", "DS_C", "DS_G", "DS_T"],
          seqid=seqid, data=sc_train_df),
        axis=3),
      "sc_train_ns": np.expand_dims(
        a=_np_get_sc_data(
          columns=["NS_wt_antisense", "NS_wt_sense"],
          seqid=seqid, data=sc_train_df),
        axis=3),
      "sc_train_ms": np.expand_dims(
        a=_np_get_sc_data(
          columns=["MS_wt_1"],
          seqid=seqid, data=sc_train_df),
        axis=3),
    } for seqid in np.unique(sc_train_df["seqid"].values)
  }
  # save
  np.save(model_inputs_dir + "sc_train_dict_" + run, sc_train_dict)


if __name__=='__main__':
  main()


###############################################################################
###############################################################################
