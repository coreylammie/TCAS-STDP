# Efficient FPGA Implementations of Pair and Triplet-based STDP for Neuromorphic Architectures

![](https://img.shields.io/badge/license-GPL-blue.svg)
![DOI](https://img.shields.io/badge/DOI-10.1109%2FTCSI.2018.2881753-brightgreen.svg)

GitHub Repository Detailing the Software and HDL Source Code for *'Efficient FPGA Implementations of Pair and Triplet-based STDP for Neuromorphic Architectures'*, published in Transactions on Circuits and Systems I (TCAS-I).

## Abstract
Synaptic plasticity is envisioned to bring about learning and memory in the brain. Various plasticity rules have been proposed, among which Spike-Timing Dependent Plasticity (STDP) has gained the highest interest across various neural disciplines, including neuromorphic engineering. Here, we propose highly efficient digital implementations of pair-based STDP (PSTDP) and Triplet-based STDP (TSTDP) on Field Programmable Gate Arrays (FPGA) that do not require dedicated floating-point multipliers, hence need minimal hardware resources. The implementations are verified by using them to replicate a set of complex experimental data, including those from pair, triplet, quadruplet, frequency-dependent pairing, as well as Bienenstock-Cooper-Munro (BCM) experiments. We demonstrate that the proposed TSTDP design has a higher operating frequency that leads to 2.46 times faster weight adaptation (learning), and achieves 11.55 folds improvement in resource usage, compared to a recent implementation of a calcium-based plasticity rule capable of exhibiting similar learning performance. In addition, we show that the proposed PSTDP and TSTDP designs respectively consume 2.38 and 1.78 times less resources than the most efficient PSTDP implementation in the literature. As a direct result of the efficiency and powerful synaptic capabilities of the proposed learning modules, they could be integrated in large-scale digital neuromorphic architectures to enable high-performance STDP learning.

## Citation

To cite our work, kindly use the following BibTex entry:

```
@ARTICLE{8566143,
author={C. Lammie and T. J. Hamilton and A. van Schaik and M. Rahimi Azghadi},
journal={IEEE Transactions on Circuits and Systems I: Regular Papers},
title={Efficient FPGA Implementations of Pair and Triplet-Based STDP for Neuromorphic Architectures},
year={2018},
doi={10.1109/TCSI.2018.2881753},
ISSN={1549-8328},
}
```

## STDP Boundary Parameter Optimization
The STDP boundary parameters were optimized by minimizing the Normalized Mean Square Error (NMSE) using *scipy.optimize.fmin()* from the SciPy Python library. All source code detailing the parameter optimization process is available under the *'STDP Boundary Parameter Optimization'* directory.

## Digital STDP Implementation
All HDL code used for the Paired Based Spike Timing Dependent Plasticity (PSTDP), Full Triplet Based Spike Timing Dependent Plasticity (TSTDP), TSTDP Hippocampal (TMH), and Minimal TSTDP Visual Cortex (TMVC) implementations is available under the *'Digital STDP Implementation'* directory.

**Preface:** All HDL files provided are targeted for the DE1-SOC development board. All reported hardware utilization numbers for our current works have been obtained from re-synthesizing our original HDL designs using the Xilinx ISE Design Suite in order to provide a direct comparison to previous works. These public files are provided as is- reminants of Verilog logic used to interface with our UART communication scheme have yet to be removed.


## License
All code is licensed under the GNU General Public License v3.0. Details pertaining to this are available at: https://www.gnu.org/licenses/gpl-3.0.en.html
