# SETUP.md - reproducing the CFD environment on a second PC (Task B3, work order 2026-09-26)

Everything below is what was actually used on the CFD machine (2026-09-17 to 2026-09-26). Exact package lists: `env/apt_packages.txt`, `env/python_packages_system_python3.10.txt`, `env/vmtk_env_packages.txt`.

## 1. Machine and OS (reference, not a requirement)
AMD Ryzen Threadripper PRO 3955WX (16 cores / 32 threads, SMT on), 27 GB RAM visible to the guest, Windows host with **WSL2 Ubuntu 22.04.5 LTS** (kernel 6.6.87.2-microsoft-standard-WSL2), root disk 295 GB. `nproc` reports 32; **plan against 16 physical cores** (logical CPUs 2k and 2k+1 are the two threads of core k). A native Ubuntu 22.04 machine needs nothing else. The smoke test needs 8 cores and about 3 GB RAM.

## 2. Software installed (versions)
| component | version | how it was installed |
|---|---|---|
| **OpenFOAM ESI v2406** | 2406.260127-2 (`openfoam2406`, `-default`, `-dev`, `-common`) | apt repository `deb [arch=amd64] https://dl.openfoam.com/repos/deb jammy main` (add the OpenFOAM.com key first), then `sudo apt install openfoam2406-default openfoam2406-dev`; environment: `source /usr/lib/openfoam/openfoam2406/etc/bashrc` (`WM_PROJECT_VERSION=v2406`) |
| **cfMesh** (`cartesianMesh`) | the one shipped with ESI v2406 (`/usr/lib/openfoam/openfoam2406/platforms/linux64GccDPInt32Opt/bin/cartesianMesh`) | nothing to install separately |
| Open MPI | 4.1.2-2ubuntu1 (`openmpi-bin`, `libopenmpi-dev`) | pulled in by the OpenFOAM packages / `apt install openmpi-bin libopenmpi-dev` |
| g++ / gcc | 11.4.0 (`build-essential`) | needed at run time: the coded resistance boundary condition (`codedFixedValue`) is compiled with `wmake` on first use (`openfoam2406-dev` provides the headers) |
| Python | 3.10.12 (system) | `python3`; pip: numpy 2.2.6, scipy 1.15.3, pandas 2.2.3, pyvista 0.47.3 (off-screen), matplotlib 3.10.9, nibabel 5.4.2, scikit-image 0.25.2, pymeshfix 0.18.1, vtk 9.6.1, trimesh 5.1.0, networkx 3.4.2, scikit-learn 1.7.2 |
| **VMTK** | 1.5.0 (conda-forge build `py39h0c35f22_14`, Python 3.9.22) | only for the real-lumen geometry pipeline (Taubin smoothing `vmtksurfacesmoothing -iterations 30 -passband 0.1`), **not needed for the smoke test**: `micromamba create -n vmtk -c vmtk -c conda-forge vmtk python=3.9 -y` (micromamba binary from micro.mamba.pm); the scripts point at the env through a `VMTK_ENV` constant |
| Blender 3.0.1 (Workbench engine) | Debian package | figures only |

Other OpenFOAM versions are installed on the CFD machine (2512, Foundation 11) and were **not** used for any returned result. Only ESI v2406 (`foamVersion` prints v2406) is validated.

## 3. Path conventions
The scripts embed the CFD machine's scratch paths (`/tmp/claude-1000/.../scratchpad/...`, `/mnt/e/Paper6-T6/...`) as constants near the top (`P`, `BASE`, `SRC`, `VMTK_ENV`, `DEFAULT_CSV`): edit them; scripts import each other by module name, so put the `.py` files of `analysis/`, `pipeline/`, `launch/`, `task1_u3d/`, `task3_scan14/` on one PYTHONPATH (see README.md). `code/zerod_ffr.py` (0D twin) lives in the project `code/` folder and is only imported by the scan-837 / Item 1 tooling, never by the scan-14 tooling (blinding).

## 4. Smoke test (about 10 minutes on 8 cores; the limit asked for is 30 minutes)
`smoke_test/` reproduces one returned result: the **Stage A sten70 vessel, A5 coarse mesh (198,252 cells), steady laminar `simpleFoam`, coded resistance outlet (R = 6.974826e9 Pa s/m3, relax 0.2), 2000 iterations**. The returned outlet flow is **1.17392231e-06 m3/s** (`returns/.../stageA_A5_ladders.csv`, A5 sten70 coarse).
```
cd code_from_cfd/smoke_test
./run_smoke_test.sh 8            # NPROC (default 8); work directory ./smoke_work (must not exist)
```
Steps: (1) `stageA/make_stageA_geometry.py --ds 70` writes `sten70.stl` (numpy only; sha256 must be `47178798e1052ddb7d23d8b318a934baaf42d93d5555b9568eddcabdf9ef8ef2`), (2) `cartesianMesh` (cfMesh, 4 boundary layers of ratio 1.2, maxCellSize 1.95e-4), (3) `checkMesh`, (4) `decomposePar` (scotch), (5) `mpirun -np NPROC simpleFoam -parallel`, (6) `compare_smoke.py` prints **SMOKE TEST PASS** iff the run finished and the outlet flow is within **0.1 %** of `reference_result.json` (a fresh run of the same script on the CFD machine) **and** of the returned value above.
Expected on the reference machine: see `smoke_test/reference_result.json` (cells, outlet flow, FFR at x = 56.5 mm, wall clock). If the cell count of your mesh differs from the reference the flow criterion is not meaningful (cfMesh output can depend on the thread count: `export OMP_NUM_THREADS=8`, the reference run states the value used); report the cell count and the flow.
Failure hints: `wmake`/g++ missing -> the coded BC does not compile (install `openfoam2406-dev`, `build-essential`); `mpirun` refuses NPROC larger than the cores (pass a smaller NPROC); `cartesianMesh` writes the inlet and outlet patches with type `wall`, the script rewrites them to `patch`.

## 5. Rules that affect throughput on any machine
Total MPI ranks across concurrent jobs <= physical cores (16 here); bind ranks to cores (`mpirun --bind-to core --map-by core`; OpenMPI 4.1.2 ignores a `taskset` applied to `mpirun` and `--cpu-set` did not work on this host: the B2 runs pin each rank with a per-rank `taskset` wrapper, `task_0926/b2/b2_rank.sh`); the launcher `launch/run_set_generic.sh` refuses to start below 10 GB free on `/`; scan-14 real-lumen steady solves cost 2.1-2.3 h and about 6 GB per 3.5-3.9 M cells at 16 ranks for 3000 iterations (see `returns/2026-09-26/settle_iterations.csv` for the settle iterations: about 1000-1250 in resistance mode).
