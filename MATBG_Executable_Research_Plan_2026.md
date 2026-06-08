# MATBG Interband Pairing Superfluid Stiffness: Executable Research Plan

版本：0.1  
日期：2026-06-07  
来源母本：`MATBG_Interband_Pairing_Superfluid_Stiffness_PhD_Proposal_2026_V2.md`  
已有基础：`MATBG_superfluid_weight_PRB_v2.tex`

## 0. 执行定位

本文件不是新的开题报告，而是把 V2 方案转化为可执行研究工程的操作层。V2 已经给出研究意义、边界与四个模块；本文件负责回答：

1. 从今天开始先做哪几件事；
2. 每个工作包输入、输出、验收标准是什么；
3. 哪些数值检查必须通过，哪些结果才能进入论文主图；
4. interband pairing 如何定义才不会变成 band-basis 规范选择的伪影；
5. 如果主假设不成立，如何把结果转化为可发表的负结果或边界结论。

一句话主线：

> 在 BM-based finite-band BdG 框架中，用可复现实验友好 observable 检验 interband pairing 是否留下区别于 intraband pairing 的超流刚度指纹。

## 1. 当前研究状态判断

### 1.1 已经具备的基础

同仓库 TeX 稿已经完成了一个重要起点：

1. BM continuum model 下的 band-basis superfluid weight decomposition；
2. `D_s = D_s^{conv} + D_s^{geom} + D_s^{cross}` 的计算框架；
3. flat-band 与 extended band truncation 的初步对照；
4. uniform s-wave、sublattice s-wave、nematic d-wave 的基准结果；
5. k-mesh、gap magnitude、filling dependence 的基础图表逻辑。

这意味着新课题不应从“能否计算 superfluid stiffness”开始，而应从以下升级点开始：

1. 把 pairing ansatz 从 band-diagonal 扩展到可控 interband / mixed pairing；
2. 把主要输出从“geometric fraction 数值”转向“observable discrimination pattern”；
3. 加入 `Dxx`、`Dyy`、anisotropy、doping trend、interband mixing strength scan；
4. 建立严格的数值验收标准，避免 cutoff、gauge、mesh 或 pairing convention 造成假信号。

### 1.2 最小可发表问题

最小可发表单元不追求证明 MATBG 真实配对机制，而只回答：

> 在同一个 BM low-energy framework 和同一套 response calculation 中，加入规范一致的 interband pairing 后，total stiffness、stiffness anisotropy、doping trend 是否出现稳健且可区分的变化？

如果答案是肯定的，论文主结论是：

1. interband pairing 可以产生某类 stiffness signature；
2. 该 signature 在参数变化下稳定；
3. 一级 observable 可以作为未来实验和理论比较的判据。

如果答案是否定的，论文仍可转化为：

1. 在 BM finite-band mean-field 范围内，interband pairing 对可观测 stiffness 的影响受限；
2. 仅靠 phenomenological interband pairing 不足以解释异常刚度；
3. 需要 self-consistent interaction、correlated normal state 或 UV-complete lattice 模型。

## 2. 核心假设与判据

### 2.1 主假设

H1：相对于纯 intraband pairing，interband 或 mixed pairing 会改变至少一个一级 observable，且变化在合理参数区间内稳健。

一级 observable 包括：

1. `Dxx_total` 与 `Dyy_total` 的绝对大小；
2. anisotropy ratio `Dxx_total / Dyy_total`；
3. normalized anisotropy `(Dxx_total - Dyy_total) / (Dxx_total + Dyy_total)`；
4. filling 或 chemical-potential dependence；
5. pairing-mixing-strength dependence。

### 2.2 次级机制假设

H2：如果一级 observable 出现稳健差异，该差异可由 `Dconv`、`Dgeom`、`Dcross` 的相对变化解释。

注意：`Dgeom / Dtotal` 不是主结论，只是解释变量。主图优先展示实验可读量。

### 2.3 稳健 signature 的工作定义

一个 signature 暂定为稳健，需要满足全部条件：

1. 在至少两个 k-mesh 上结论不变，建议 `nk = 12, 14, 16` 中至少两个通过；
2. 对 finite-difference step 或 velocity evaluation 的合理变化不敏感；
3. 在 `Delta0 = 0.3, 0.5, 1.0 meV` 中至少两个值保持同一趋势；
4. 在小幅改变 band truncation 或 cutoff 时，一级 observable 的符号、峰位或排序不翻转；
5. 效应量超过数值误差，建议主结论使用大于 `10%` 的 relative change，边界结论可记录 `5%` 到 `10%`。

## 3. 范围锁定

### 3.1 必做范围

1. BM continuum model，参数先沿用现有 TeX 稿；
2. `T = 0` mean-field BdG；
3. flat-band projection `n_keep = 2` 作为主线；
4. `n_keep = 4, 6` 作为 remote-band 趋势与 cutoff 风险检查；
5. pairing classes：
   - intraband uniform s-wave；
   - intraband nematic d-wave；
   - interband s-like pairing；
   - mixed intra plus interband pairing；
6. observables：
   - `Dxx_total`, `Dyy_total`；
   - `Dxx_conv`, `Dyy_conv`；
   - `Dxx_geom`, `Dyy_geom`；
   - `Dxx_cross`, `Dyy_cross`；
   - anisotropy measures；
   - filling dependence。

### 3.2 暂不做范围

1. 自洽 Hartree-Fock normal state；
2. self-consistent gap equation；
3. finite-T / BKT；
4. heterostrain；
5. full experimental fitting；
6. UV-complete atomistic lattice calculation。

这些内容只能作为 discussion 或 future work，不能进入主线依赖。

## 4. 关键技术风险：interband pairing 的规范协变性

V2 中把 interband pairing 定义为 normal-state band basis 里的 off-diagonal pairing matrix。这是正确的研究语言，但执行时必须小心：

> 任意指定 `Delta_nm(k)` 的非对角常数可能依赖 band eigenvector 的相位和 gauge choice，因此可能不是物理可观测 ansatz。

### 4.1 优先路线 A：orbital/sublattice basis 定义，再投影到 band basis

这是首选路线。

做法：

1. 在 orbital/sublattice/layer basis 中定义物理配对矩阵 `Delta_orb(k)`；
2. 用 normal-state eigenvectors 投影：

```text
Delta_band(k) = U^\dagger(k) Delta_orb(k) U^*(-k)
```

3. `Delta_band(k)` 中自然出现 diagonal 与 off-diagonal components；
4. 通过调节 orbital structure 或 mixing parameter 控制 interband weight；
5. 所有 observable 在 gauge transformation 下保持不变。

优点：

1. 物理解释更强；
2. 避免 arbitrary band-basis off-diagonal term；
3. 更容易回应审稿人关于 gauge dependence 的质疑。

### 4.2 备选路线 B：band basis phenomenology，但必须加 gauge fixing 和 gauge test

仅当路线 A 无法快速实现时使用。

最低要求：

1. 对 `U(k)` 使用连续 gauge fixing；
2. 明确给出 `Delta_nm(k)` 的 transformation rule；
3. 对 eigenvector 随机相位重定义进行测试，确认 `Dxx_total`、`Dyy_total` 不变；
4. 若结果随相位改变，则该 ansatz 不可作为主结果。

### 4.3 第一决策门

截止日期：2026-06-13

必须完成：

1. 明确采用路线 A 或路线 B；
2. 写出具体 `Delta(k)` 定义；
3. 完成 hermiticity、particle-hole symmetry、gauge-randomization 三项检查；
4. 若三项检查失败，本课题不得进入大规模参数扫描。

## 5. 工作包拆解

### WP0：仓库与可复现环境

目标：把当前论文仓库整理成可以运行、复现、归档的研究工程。

输入：

1. 当前 TeX 稿；
2. V2 proposal；
3. 后续 Python 代码与数据。

任务：

1. 创建标准目录结构；
2. 固定 Python 依赖；
3. 建立 config-driven run 方式；
4. 建立 research log；
5. 规定图表、数据、代码命名。

建议目录：

```text
MATBG/
  README.md
  MATBG_Interband_Pairing_Superfluid_Stiffness_PhD_Proposal_2026_V2.md
  MATBG_Executable_Research_Plan_2026.md
  papers/
  notes/
  src/
    matbg/
      bm_model.py
      band_basis.py
      pairing.py
      bdg.py
      stiffness.py
      scans.py
      plotting.py
  scripts/
    run_benchmark.py
    run_pairing_scan.py
    run_filling_scan.py
    make_figures.py
  configs/
    benchmark.yaml
    pairing_scan.yaml
    filling_scan.yaml
  data/
    raw/
    processed/
  figures/
  runs/
```

验收标准：

1. 一条命令可以跑出 benchmark；
2. 每次扫描保存 config、commit hash、参数、结果摘要；
3. 任何主图都能追溯到对应 run folder。

### WP1：文献收缩与论证表

目标：把文献综述从叙述性材料变成论文论证矩阵。

任务：

1. 建立 `notes/literature_matrix.md`；
2. 对每篇核心文献记录：
   - 模型；
   - 是否含 interband pairing；
   - 是否计算 total stiffness；
   - 是否分解 conventional/geometric；
   - 是否给出 experimental observable；
   - 本文可借用和需避开的表述；
3. 将文献分为四组：
   - flat-band quantum geometry；
   - MATBG topology and geometry；
   - interband pairing / multiband BdG；
   - stiffness / kinetic inductance experiments。

验收标准：

1. 至少 15 篇核心文献进入矩阵；
2. 每篇文献最多 5 行高密度摘要；
3. 形成一个 gap statement：

```text
Existing work establishes geometric contribution, but does not provide an observable-driven comparison of intra- and interband pairing signatures in a unified BM BdG response framework.
```

### WP2：BM normal-state benchmark

目标：确认 normal-state baseline 与已有 TeX 稿一致。

固定参数：

```text
theta = 1.05 deg
vF = 2.135 eV Angstrom
w0 = 87.2 meV
w1 = 109.0 meV
w0 / w1 = 0.80
N_shell = 3
nk benchmark = 12, 14, 16
n_keep = 2, 4, 6
```

任务：

1. 复现 BM flat-band bandwidth；
2. 输出 band structure；
3. 输出 density/filling versus chemical potential map；
4. 检查 eigenvector phase handling；
5. 保存 `U(k)`、`epsilon(k)` 的数据接口。

验收标准：

1. flat-band bandwidth 接近现有 TeX 稿的 `W = 11.2 meV`；
2. band ordering 在扫描网格上无明显跳带错误；
3. `nu(mu)` 单调且可用于 filling scan；
4. `n_keep = 2` 子空间在目标 chemical potential 范围内稳定。

### WP3：BdG 与 stiffness response engine

目标：形成可复用的 stiffness 计算核心。

任务：

1. 构造 BdG Hamiltonian；
2. 实现 current operator；
3. 实现 `D_mu_nu_total`；
4. 实现 `conv / geom / cross` decomposition；
5. 支持 `mu`、`Delta0`、`eta_inter`、`pairing_type` 扫描；
6. 同时输出 `xx` 与 `yy` 分量。

核心公式接口：

```text
normal bands:
  H(k) U(k) = U(k) epsilon(k)

BdG:
  H_BdG(k) = [[epsilon(k) - mu, Delta_band(k)],
              [Delta_band^\dagger(k), -epsilon^T(-k) + mu]]

response:
  D_mu_nu = K_mu_nu + paramagnetic_response_mu_nu
```

BM continuum 主线里 diamagnetic term 可为零，但文中必须明确这是 continuum cutoff 的限制。`n_keep > 2` 结果只作为 trend，不作为模型无关定量结论。

验收标准：

1. BdG spectrum 满足 particle-hole symmetry；
2. `Dxx_total` 与现有 TeX benchmark 在 intraband s-wave 下相符；
3. symmetric pairing 下 `Dcross` 接近零的旧结果能复现；
4. `Dxx` 与 `Dyy` 在 C3-symmetric baseline 下不应出现无物理来源的大各向异性；
5. 数值误差随 `nk` 增加收敛。

### WP4：pairing ansatz 实现

目标：把 V2 里的四类 pairing 写成可测试、可解释、可审稿的数学对象。

#### WP4.1 intraband uniform s-wave

用途：baseline。

```text
Delta_nm(k) = Delta0 delta_nm
```

验收：

1. 复现旧稿 table；
2. `Dcross / Dtotal` 接近旧稿水平。

#### WP4.2 intraband nematic d-wave

用途：产生 pairing-driven anisotropy baseline。

```text
Delta_nm(k) = Delta0 f_d(k) delta_nm
f_d(k) = cos(k dot a1) - cos(k dot a2)
```

验收：

1. `Dconv` 相比 uniform s-wave 下降；
2. anisotropy 的方向与 nematic axis 一致；
3. 换 nematic orientation 时 anisotropy 旋转而不是数值崩溃。

#### WP4.3 interband s-like pairing

用途：核心新机制。

优先用 orbital-defined pairing 投影得到：

```text
Delta_orb(k; eta) = Delta0 [M_intra + eta M_inter_like]
Delta_band(k; eta) = U^\dagger(k) Delta_orb(k) U^*(-k)
```

其中 `eta` 是 interband mixing strength。初始扫描：

```text
eta = 0.00, 0.10, 0.25, 0.50, 0.75, 1.00
```

验收：

1. `eta = 0` 回到 intraband 或已知 orbital baseline；
2. `eta` 增大时 off-diagonal pairing weight 单调或可解释；
3. gauge-randomization 后 total observables 不变；
4. gap matrix 满足 spin-singlet even-parity 的对称要求。

#### WP4.4 mixed intra plus interband pairing

用途：建立 discrimination map。

任务：

1. 扫描 `Delta_intra` 与 `Delta_inter`；
2. 固定 total gap norm 的扫描和固定 `Delta_intra` 的扫描都做一版；
3. 区分“总 gap 变大导致 stiffness 增强”和“interband structure 导致 stiffness 改变”。

验收：

1. 至少有一个 normalized comparison，其中 gap norm 固定；
2. 主结论不能只来自 `Delta` 总幅度变化；
3. discrimination map 中每一块区域都有对应参数定义。

### WP5：observable-first 参数扫描

目标：先得到实验友好结果，再解释内部组成。

优先扫描顺序：

1. `eta_inter` scan at CNP；
2. `mu` 或 filling scan for selected eta；
3. `Delta0` scan；
4. `n_keep` robustness check；
5. optional nematic orientation scan。

建议初始网格：

```text
mu = -8, -6, -4, -2, 0, 2, 4, 6, 8 meV
Delta0 = 0.3, 0.5, 1.0 meV
eta_inter = 0.00, 0.10, 0.25, 0.50, 0.75, 1.00
nk = 12, 14
n_keep = 2
```

通过后再扩展：

```text
nk = 16
n_keep = 4, 6
mu grid dense near signature peak
```

主输出表：

```text
pairing_type
eta_inter
mu_meV
filling_nu
Delta0_meV
nk
n_keep
Dxx_total
Dyy_total
Dxx_conv
Dyy_conv
Dxx_geom
Dyy_geom
Dxx_cross
Dyy_cross
anisotropy_ratio
anisotropy_norm
geom_fraction_xx
geom_fraction_yy
run_id
```

验收标准：

1. 至少生成 intraband 与 interband 的同参数对照；
2. 每一个 claimed signature 都有 error/robustness 检查；
3. 所有图都能从结果表自动重画。

### WP6：判别图谱与论文写作

目标：把扫描结果转化为论文叙事。

判别图谱的形式：

1. 横轴：filling 或 `mu`；
2. 纵轴：`eta_inter` 或 pairing class；
3. 颜色：`Dtotal` enhancement、anisotropy、或 `Dgeom / Dtotal`；
4. overlay：稳健区间和不稳健区间。

论文主图候选：

1. Fig. 1：research pipeline schematic，BM bands 到 BdG 到 stiffness observable；
2. Fig. 2：baseline reproduction，intraband s-wave decomposition；
3. Fig. 3：`eta_inter` scan of `Dxx_total`, `Dyy_total`, anisotropy；
4. Fig. 4：filling dependence for intra vs inter vs mixed；
5. Fig. 5：decomposition explaining selected signatures；
6. Fig. 6：pairing discrimination map；
7. Appendix：k-mesh、gauge test、band truncation、gap-norm normalization。

验收标准：

1. 主文只放一级 observable 和少量解释图；
2. `Dconv / Dgeom / Dcross` 主要用于解释，不喧宾夺主；
3. 每个结论都标明 BM-based、finite-band、phenomenological pairing 的边界。

## 6. 前两周执行冲刺

### Sprint 1：2026-06-07 到 2026-06-13

目标：把 interband pairing 定义和数值工程地基锁死。

任务清单：

1. 建立 repo structure；
2. 创建 `README.md` 与 `notes/literature_matrix.md`；
3. 从旧 TeX 稿抽取 BM 参数和旧 benchmark 表；
4. 明确采用 route A 还是 route B 定义 interband pairing；
5. 写出 `Delta_orb(k)` 或 `Delta_band(k)` 的精确定义；
6. 制定 gauge-randomization test；
7. 跑通 intraband s-wave benchmark 或整理旧结果为机器可读表。

本周验收物：

1. `configs/benchmark.yaml`；
2. `notes/interband_pairing_definition.md`；
3. `notes/literature_matrix.md` 初版；
4. benchmark result table；
5. go/no-go note：interband ansatz 是否进入扫描。

### Sprint 2：2026-06-14 到 2026-06-20

目标：完成最小 interband scan。

任务清单：

1. 实现或整理 stiffness engine 的 `Dxx`、`Dyy` 输出；
2. 跑 `eta_inter = 0, 0.25, 0.5, 1.0` at `mu = 0`；
3. 跑 `mu = -4, 0, 4 meV` 的小扫描；
4. 检查 `Delta0 = 0.5, 1.0 meV` 的趋势是否一致；
5. 画第一版 comparison figure；
6. 写一页 result memo。

本周验收物：

1. `runs/2026-06-14_minimal_interband_scan/`；
2. first-pass figure；
3. `notes/result_memo_2026-06-20.md`；
4. 是否值得扩大扫描的判断。

## 7. Go/No-Go 决策门

### Gate 1：interband ansatz 是否物理可用

时间：2026-06-13

Go 条件：

1. gap matrix 对称性正确；
2. gauge test 通过；
3. `eta = 0` 可回到 baseline；
4. off-diagonal pairing weight 可定义、可量化。

No-Go 后处理：

1. 放弃 arbitrary band-basis ansatz；
2. 只保留 orbital-defined projected pairing；
3. 把“band-basis interband pairing 的规范依赖风险”写入方法学说明。

### Gate 2：最小 scan 是否出现可观测差异

时间：2026-06-20

Go 条件：

1. 至少一个一级 observable 出现大于 `10%` 的变化；
2. 趋势在两个 `Delta0` 下同向；
3. 数值误差小于效应量。

No-Go 后处理：

1. 改为边界论文：interband pairing in this framework does not strongly alter observable stiffness；
2. 扩大到 nematic/mixed pairing 看是否只有 symmetry-breaking ansatz 有信号；
3. 明确指出需要 self-consistent interaction 或 correlated normal state。

### Gate 3：主图是否足够支撑 PRB 级论文

时间：2026-08-31

Go 条件：

1. 已有 4 张以上主结果图；
2. 每张主图有对应 robustness appendix；
3. discrimination map 有清晰物理解释；
4. introduction 和 limitations 能诚实限定模型边界。

No-Go 后处理：

1. 缩成短论文或方法论文；
2. 聚焦 gauge-covariant interband pairing construction；
3. 把大规模实验对照移到后续工作。

## 8. 数值检查清单

每次主扫描前后都要检查：

1. Normal-state Hamiltonian hermiticity；
2. BdG Hamiltonian hermiticity；
3. BdG particle-hole symmetry；
4. Band sorting continuity；
5. `U(k)` phase/gauge handling；
6. current operator decomposition correctness；
7. finite-difference velocity convergence；
8. k-mesh convergence；
9. `Dxx` and `Dyy` symmetry sanity check；
10. `Dtotal = Dconv + Dgeom + Dcross` numerical closure；
11. gap-norm normalization；
12. sensitivity to `n_keep` and cutoff。

任何主图如果缺少 8.1 到 8.12 中相关检查，不能进入论文主文。

## 9. 研究日志规范

建议建立 `RESEARCH_LOG.md`，每次运行后写 5 行：

```text
Date:
Question:
Config / run_id:
Result:
Decision:
```

每周五或周日做一次 weekly synthesis：

1. 本周得到什么；
2. 哪个假设增强，哪个假设减弱；
3. 下周唯一最重要任务；
4. 哪些图可以保留；
5. 哪些结果需要重跑。

## 10. 论文叙事骨架

### 10.1 Introduction 的中心张力

MATBG 的平带和量子几何可以增强超流刚度，但“几何增强存在”不等于“能区分配对机制”。本文将问题推进到可观测判别：

> Can interband pairing leave robust observable signatures in the superfluid stiffness tensor of MATBG?

### 10.2 Methods 的核心防线

1. BM model；
2. finite-band BdG；
3. gauge-covariant construction of pairing；
4. band-basis current decomposition；
5. observable-first scan；
6. cutoff and mesh limitations。

### 10.3 Results 的优先顺序

1. baseline reproduction；
2. interband mixing changes total stiffness or anisotropy；
3. filling dependence gives observable signature；
4. decomposition explains the signature；
5. robustness and negative regions。

### 10.4 Discussion 的诚实边界

必须明确：

1. 这不是 microscopic proof of real pairing；
2. BM continuum extended-band results 有 cutoff sensitivity；
3. phenomenological pairing 只能给 mechanism test；
4. experimental comparison 是 qualitative 或 semi-quantitative；
5. full explanation of large experimental stiffness may need interactions, vertex corrections, strong coupling, or lattice regularization。

## 11. 立即下一步

下一步不应该继续扩写开题语言，而应进入执行材料：

1. 创建 repo structure；
2. 写 `notes/interband_pairing_definition.md`；
3. 把现有 TeX 的 benchmark 数值整理成 `data/processed/baseline_benchmarks.csv`；
4. 写最小 `configs/benchmark.yaml`；
5. 决定并验证 interband pairing 的 gauge-covariant construction。

如果只做一件事，先做第 2 项。因为 interband pairing 的定义一旦不稳，后面所有扫描都会失去物理意义。
