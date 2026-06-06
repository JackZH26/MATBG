# 博士论文研究方案 V2

## 题目

**魔角双层石墨烯中带间配对与量子几何超流刚度的可观测指纹研究**

英文题目：
**Observable Signatures of Interband Pairing and Quantum-Geometric Superfluid Stiffness in Magic-Angle Twisted Bilayer Graphene**

## 一、研究背景与意义

魔角双层石墨烯（magic-angle twisted bilayer graphene, MATBG）自 2018 年被发现具有关联绝缘态与超导态以来，已成为强关联电子体系、莫尔材料和非常规超导研究的重要平台。MATBG 的关键特征在于近乎平坦的低能能带。平带一方面抑制由带速度主导的常规 Drude 型超流响应，另一方面又因非平庸的波函数结构、Berry connection 与 quantum metric，为几何增强的超流刚度（superfluid stiffness / superfluid weight）提供了可能。

量子几何对超流权重的贡献已在一般平带超导理论中得到系统发展。Peotta 与 Törmä 证明平带体系中的超流权重可由 quantum metric 提供下界；Hu 等、Julku 等将该框架推广到多带体系。对于 MATBG，Xie、Song、Lian 与 Bernevig 等工作指出，受保护的波函数拓扑结构使几何超流刚度在理论上不可忽略。实验上，对 MATBG 的 superfluid stiffness、kinetic inductance 以及 gap anisotropy 的测量，也表明简单的常规 BCS 图像难以完整解释其超导响应。

但当前研究仍存在三个缺口：

1. 多数工作仍停留在“量子几何有贡献”的定性层面，对不同配对机制如何塑造可观测超流刚度缺少系统比较。
2. 对 band-diagonal pairing 的研究相对较多，而对 band-off-diagonal 或 interband pairing 如何影响超流刚度张量、各向异性与掺杂依赖，研究仍不充分。
3. 理论与实验之间缺少“observable-driven discrimination”框架，即缺少从实验可测 stiffness pattern 反推可能配对机制的系统路线。

因此，本课题拟围绕“带间配对 + 量子几何 + 可观测超流刚度指纹”构建一个更收敛、更可执行的理论研究框架。与其追求给出某个模型无关的定量“几何占比”，本课题更关注在一个明确的低能理论范围内，哪些相对稳健的 stiffness signatures 可以用于区分不同配对机制。

## 二、国内外研究现状

### 2.1 量子几何与超流权重

Peotta 与 Törmä 的工作表明，平带超导中的超流权重可由 quantum metric 控制，这为“平带也能支持有限超流响应”提供了理论基础。Hu 等与 Julku 等进一步将这一框架推广到多带超导，指出 interband processes 在超流响应中可能扮演关键角色。

### 2.2 MATBG 中的几何超导问题

基于 Bistritzer-MacDonald（BM）continuum model 的研究表明，MATBG 平带的非平庸量子几何可显著增强超流权重。Xie 等进一步指出，MATBG 的拓扑波函数结构为几何超流刚度提供了受保护下界。然而，已有结果多强调下界、趋势或定性机制，而较少建立与实验 observable 直接对话的判别框架。

### 2.3 配对对称性与带间配对

MATBG 的配对对称性仍未定论。文献中已讨论过 s-wave、nematic d-wave、chiral d+id、valley-structured pairing 等候选机制。近年的 twisted graphene 理论工作提示，band-off-diagonal 或 interband pairing 不仅可能存在，而且会显著影响超流刚度、低温热力学行为与相变特征。这说明若只考虑 intraband pairing，可能无法完整捕捉真实体系的超导响应。

### 2.4 实验约束

最新实验已经测量 MATBG 的 superfluid stiffness、kinetic inductance 以及与 gap anisotropy 相关的信号。这意味着理论工作不应只汇报某个内部理论量的数值，而应优先回答：不同配对机制是否产生不同的实验友好 observable，例如总刚度大小、各向异性比、掺杂趋势与低温行为。

### 2.5 现有研究的不足

当前仍缺少一项同时满足以下条件的系统工作：

1. 在统一 BdG 线性响应框架中比较 intraband 与 interband pairing；
2. 同时分析总超流刚度与其理论内部组成（conventional / geometric / cross）；
3. 以实验可见 observable 为主、以理论分解为辅，建立 pairing discrimination 图谱。

本课题的工作定位即是填补这一缺口。

## 三、Interband Pairing 的定义、物理动机与本文范围

这是本方案 V2 新增的关键限定部分。

### 3.1 本文中 interband pairing 的定义

本文所说的 interband pairing，特指在 normal-state band basis 中，配对矩阵存在显著的非对角元：

- intraband pairing：Δ_nm(k) 仅在 n = m 时非零；
- interband pairing：Δ_nm(k) 在 n ≠ m 时也存在非零分量。

这里的“band”首先指低能有效模型中经对角化得到的 normal-state bands，而不是简单的 sublattice basis 或 orbital basis。

### 3.2 研究 interband pairing 的物理动机

本课题并不预设 interband pairing 已被 MATBG 实验证实，而是将其视为一个待检验的候选机制。研究其必要性来自以下几点：

1. MATBG 属于多带、强混合波函数结构体系，band basis 中的配对不必天然严格对角。
2. 近年的 twisted graphene 理论工作提示，band-off-diagonal pairing 可能显著影响 superfluid stiffness 与低温热力学行为。
3. 若 interband pairing 能产生区别于纯 intraband pairing 的稳健 stiffness signatures，则它有望成为解释实验异常刚度与各向异性的有效候选机制。

### 3.3 本文的范围与边界

本文中的 interband pairing 主要作为 **mechanism hypothesis** 与 **effective phenomenological ansatz** 来研究，而不是从某个显式 many-body interaction 出发自洽推导其唯一形式。本文目标是回答：

**在 BM-based low-energy effective framework 中，interband pairing 是否产生稳健且可区分的超流刚度指纹？**

因此，本文不声称：

1. 已唯一确定 MATBG 的真实配对机制；
2. 已给出模型无关的定量实验拟合；
3. 已证明所有 interband pairing 形式都物理可实现。

## 四、研究目标

本课题的总体目标是：

**在 BM-based 多带 BdG 框架下，系统检验 interband pairing 是否产生区别于 intraband pairing 的稳健超流刚度指纹，并建立以实验友好 observable 为主、以几何分解为解释的理论判别框架。**

为避免问题过宽，本课题将目标分为一个主目标与两个次目标。

### 4.1 主目标

回答以下核心问题：

**在 MATBG 的低能有效模型中，interband pairing 是否导致稳健、可与 intraband pairing 区分的 superfluid stiffness signatures？**

### 4.2 次目标一

建立统一理论框架，同时计算：

1. 总超流刚度张量 Dxx、Dyy；
2. 理论内部组成 Dconv、Dgeom、Dcross；
3. 它们随掺杂与 pairing parameters 的变化。

### 4.3 次目标二

提炼哪些实验友好 observable 最有判别力，用于区分不同 pairing mechanisms，尤其识别 interband pairing 是否为解释异常刚度与各向异性的必要成分。

## 五、核心科学问题

围绕上述目标，本课题聚焦三个收紧后的科学问题。

### 5.1 核心问题一

interband pairing 是否能够在合理参数区间内显著改变总超流刚度，且这种改变区别于纯 intraband pairing？

### 5.2 核心问题二

interband pairing 是否产生稳健的 stiffness tensor 指纹，例如：

1. Dxx/Dyy 各向异性比的系统改变；
2. 掺杂依赖峰值位置或不对称性的改变；
3. 总刚度增强但不必要求几何占比单调提升。

### 5.3 核心问题三

在多配对机制比较中，哪些 observable 最适合作为“一级判据”，哪些理论分解量适合作为“二级解释量”？

这里明确区分：

- **一级 observable（实验友好）**：总刚度大小、刚度各向异性、掺杂趋势、低温趋势；
- **二级解释量（理论内部）**：Dconv、Dgeom、Dcross 及其相对变化。

## 六、研究内容

本课题拟分为四个模块，但主线只要求完成前 1–3 模块；模块 4 为理论解释与对照总结。

### 6.1 模块一：统一理论框架

在 BM continuum model 的基础上，在 normal-state band basis 中构造统一 BdG Hamiltonian，显式比较以下四类配对：

1. intraband isotropic s-wave；
2. intraband nematic d-wave；
3. interband s-like pairing；
4. mixed intra+interband pairing。

同时建立 current operator 与 superfluid stiffness tensor 的统一 Kubo 线性响应表达式。

### 6.2 模块二：一级 observable 的机制判别

优先比较以下实验友好 observable：

1. 总超流刚度大小；
2. 刚度张量各向异性 Dxx/Dyy；
3. 掺杂 dependence；
4. 在可行情况下的低温趋势。

### 6.3 模块三：二级解释量分解

在一级 observable 基础上，再分析：

1. Dconv、Dgeom、Dcross；
2. interband pairing 是否优先增强几何项、交叉项或总刚度；
3. 几何分解与 observable signatures 之间的对应关系。

### 6.4 模块四：实验对照与判别图谱

将理论结果整理为 pairing discrimination map，即：

1. 哪些 stiffness patterns 更支持 intraband pairing；
2. 哪些更支持 interband pairing；
3. 哪些结论只应表述为 BM-based low-energy trends，哪些可与实验做较稳健的定性对照。

## 七、研究方法与技术路线

### 7.1 研究方法

本课题采用“解析推导 + 数值模拟 + 文献数据对比”的综合方法：

1. **解析推导**：建立 BdG Hamiltonian、current operator 与 stiffness tensor 的统一表达。
2. **数值模拟**：基于 Python 实现 BM 能带、配对态与线性响应计算。
3. **参数扫描**：在 chemical potential、pairing amplitude、interband pairing strength、anisotropy parameters 等维度上进行系统扫描。
4. **实验对照**：将一级 observable 与公开实验结果做定性或半定量对照。

### 7.2 技术路线

1. 复现 BM continuum band structure 与已知 benchmark。
2. 构造统一 BdG 框架，实现 current operator 在 band basis 中的拆分。
3. 建立数值程序，计算 Dxx、Dyy、Dconv、Dgeom、Dcross。
4. 先比较 intraband s-wave 与 interband s-like pairing，验证主 pipeline。
5. 再加入 nematic d-wave 与 mixed pairing，构建多机制对比图谱。
6. 系统扫描 chemical potential、pairing strength、interband mixing strength，输出主结果图。
7. 先从一级 observable 提炼判据，再用二级解释量解释其来源。

## 八、创新点

本课题的创新点改写为可检验形式如下：

### 8.1 创新点一

提出一个统一的 BM-based band-basis BdG 框架，用于直接比较 intraband 与 interband pairing 对 superfluid stiffness tensor 的影响。

### 8.2 创新点二

不以“几何占比”本身为论文主结论，而是以实验友好 observable 为主结论，以几何分解为机制解释，从而建立 observable-driven discrimination 路线。

### 8.3 创新点三

系统检验 interband pairing 是否产生稳健的 stiffness signatures，例如各向异性、掺杂不对称性或总刚度异常增强。

### 8.4 创新点四

明确区分一级 observable 与二级解释量，构建面向实验的 pairing discrimination map。

## 九、模型边界、适用范围与潜在局限

这是本方案 V2 的另一项关键补充。

### 9.1 模型边界

本课题工作严格限定在 **BM-based low-energy effective framework** 中。研究目标是识别稳健的相对趋势与可观测指纹，而不是给出对真实 MATBG 的模型无关定量结论。

### 9.2 不包含的内容

本课题首阶段不包含：

1. 自洽 Hartree-Fock 重构正常态；
2. UV-complete lattice regularization；
3. 从 microscopic interaction 唯一推出真实 pairing mechanism；
4. 对实验进行高精度定量拟合。

### 9.3 允许的结论类型

本课题优先追求以下结论：

1. 在给定低能理论中，哪些 signatures 对不同 pairing mechanisms 稳健；
2. 哪些趋势在参数变化下稳定存在；
3. 哪些 observable 更适合作为未来实验与理论比较的判据。

### 9.4 需要避免的表述

后续论文与开题报告中应避免：

1. 将 cutoff-sensitive trend 叙述为模型无关定量事实；
2. 将某一 phenomenological interband pairing ansatz 直接等同于真实实验机制；
3. 将定性趋势与严格实验解释混为一谈。

## 十、研究基础与可行性分析

### 10.1 研究基础

前期已积累以下基础：

1. 对 BM continuum model 的基本结构与数值求解已有了解；
2. 已完成 superfluid weight decomposition 的初步实现与结果分析；
3. 已系统分析相关 referee 评论、模型争议与方法学风险；
4. 已形成对 PRB 级文章中方法、边界和论证方式的基本认识。

### 10.2 条件可行性

本课题以理论与数值模拟为主，不依赖实验平台。现有条件包括：

1. 一台 VPS 服务器；
2. Python 常规科学计算环境；
3. 最新大模型辅助文献整理、推导梳理与写作；
4. 可访问公开论文与公开实验数据。

与 Hartree-Fock 全自洽或 atomistic lattice 方案相比，本课题主要涉及 continuum model + BdG diagonalization + response calculation + parameter scans，整体属于单机可执行范围。

### 10.3 风险与应对

1. **问题过宽。**
   应对：固定一个主问题，所有扩展任务后置。

2. **interband pairing 物理动机不足。**
   应对：在开题与论文中明确其作为 candidate mechanism / effective ansatz 的地位，而非已证实事实。

3. **结果只有数值差异，缺乏判据。**
   应对：一级 observable 优先，二级解释量后置。

4. **部分结论受 continuum cutoff 敏感。**
   应对：严格限定结论范围，仅强调稳健相对趋势。

5. **finite-T / BKT 工作量超载。**
   应对：列为扩展任务，不影响主线交付。

## 十一、预期成果

### 11.1 核心成果

1. 一篇以 MATBG 中 interband pairing 与 superfluid stiffness signatures 为主题的 PRB 候选论文；
2. 一套可复用的 Python 理论与数值框架；
3. 一个 pairing discrimination map，服务于后续理论扩展与实验对照。

### 11.2 扩展成果

若核心任务顺利完成，可进一步发展出扩展论文或后续章节，例如：

1. heterostrain 对超流刚度指纹的影响；
2. finite-T / BKT 下的几何增强超导相图；
3. 更复杂 correlated normal state 的后续升级研究。

## 十二、研究计划与时间安排

V2 将计划分成“核心任务”和“扩展任务”。

### 12.1 核心任务

#### 第一阶段：文献收缩与理论框架建立

时间：第 1–2 个月

任务：

1. 梳理 MATBG superfluid stiffness、quantum geometry、interband pairing 核心文献；
2. 明确 pairing 候选集；
3. 完成 BdG + Kubo + decomposition 理论框架整理；
4. 明确一级 observable 与二级解释量的区分。

成果：

1. 文献综述笔记；
2. 理论框架草稿；
3. 开题报告修订稿。

#### 第二阶段：数值平台搭建与 benchmark 验证

时间：第 3–5 个月

任务：

1. 搭建 BM band structure 与 BdG numerical pipeline；
2. 复现 benchmark；
3. 先完成 intraband s-wave 与 interband s-like pairing 对比；
4. 验证 Dxx、Dyy、Dconv、Dgeom、Dcross 的稳定性。

成果：

1. 可运行代码；
2. benchmark 图；
3. 第一批主结果。

#### 第三阶段：主结果生成与判别图谱

时间：第 6–9 个月

任务：

1. 纳入 nematic d-wave 与 mixed pairing；
2. 扫描 chemical potential、gap amplitude、interband mixing strength；
3. 优先输出 total stiffness、anisotropy、doping trend；
4. 再补 Dconv、Dgeom、Dcross 的解释分析；
5. 提炼 pairing discrimination rules。

成果：

1. 主结果图；
2. observable signature map；
3. 论文主结果草稿。

#### 第四阶段：论文写作与投稿准备

时间：第 10–12 个月

任务：

1. 完成 PRB 主论文写作；
2. 整理附录、方法学说明与代码归档；
3. 完成图形规范化和投稿准备。

成果：

1. 论文初稿；
2. 图表与代码归档；
3. 投稿材料。

### 12.2 扩展任务

以下内容列为扩展，不纳入首阶段硬交付：

1. finite-T / BKT 分析；
2. 更大参数空间扫描；
3. heterostrain 扩展；
4. correlated normal state 升级。

## 十三、论文结构设想

若本课题发展为博士论文核心章节或阶段性代表成果，建议结构如下：

1. 绪论：MATBG 超导问题与量子几何理论背景；
2. 理论基础：BM 模型、BdG 方法、超流刚度张量与分解框架；
3. intraband 与 interband pairing 的统一理论描述；
4. 一级 observable 的机制判别结果；
5. 二级解释量分析与实验对照；
6. 结论与展望。

## 十四、参考文献（核心）

1. S. Peotta and P. Törmä, Nat. Commun. **6**, 8944 (2015).
2. X. Hu, T. Hyart, D. I. Pikulin, and E. Rossi, Phys. Rev. Lett. **123**, 237002 (2019).
3. F. Xie, Z. Song, B. Lian, and B. A. Bernevig, Phys. Rev. Lett. **124**, 167002 (2020).
4. P. Törmä, S. Peotta, and B. A. Bernevig, Nat. Rev. Phys. **4**, 528 (2022).
5. H. Tanaka et al., Nature **638**, 99-105 (2025).
6. M. Putzer and M. S. Scheurer, Phys. Rev. B **111**, 144513 (2025).
7. R. Bistritzer and A. H. MacDonald, Proc. Natl. Acad. Sci. U.S.A. **108**, 12233 (2011).
8. M. Koshino et al., Phys. Rev. X **8**, 031087 (2018).

## 十五、结论

V2 版方案在保持原方向不变的前提下，完成了三项关键收紧：

1. 将研究目标压缩为“一个主问题 + 两个次目标”；
2. 明确补充了 interband pairing 的定义、物理动机与本文范围；
3. 明确区分了一级 observable 与二级解释量，并严格限定了 BM-based 低能模型的结论边界。

因此，本方案相较初版更符合严格开题评审的要求：问题更凝练、边界更清楚、风险控制更诚实、可执行性更强。它仍然是一个有前沿价值的 MATBG 理论选题，同时也更适合作为现有资源条件下的真实可落地研究主线。
