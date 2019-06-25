# FIDDLE

### Flexible Integration of Data with Deep LEarning
a novel deep neural network approach for the integration and inference of functional genomic data

### [FIDDLE notebook 🎻](https://colab.research.google.com/github/churchmanlab/FIDDLE/blob/master/fiddle.ipynb)

```bash
directory architecture

├── < head_dir >
│   ├── logs/
│   ├── DATA/
│   │   ├── RAW/
│   │   │   ├── annotations
│   │   │   ├── bedgraphs
│   │   │   ├── txt
│   │   ├── COLLATED/
│   ├── MODELS/
│   │   ├── FIGURES_STATS/
│   │   ├── INPUTS/
│   │   ├── OUTPUTS/
│   │   ├── TRAINED/
│   │   ├── SCRIPTS/
│   │   │   ├── sc_train_split.py
│   │   │   ├── fiddle.py
│   │   │   ├── collate_outputs.py
```

![alt text](https://github.com/churchmanlab/FIDDLE/blob/master/architecture.png)

**_note_**: an HPC cluster with GPUs is recommended

[coding environment instructions](https://github.com/churchmanlab/FIDDLE/blob/master/HPC_instructions.md)
