# Cross-scale phase dependence / 跨尺度依赖相位

## Method / 方法

For each 4 × 4 window, compute mean fine-scale Haar detail energy over four 2 × 2 subblocks and coarse-scale energy from their means. Apply log1p, center within four luminance bins, and pool covariance and variance to form a correlation. Repeat for all 16 sampling origins. Report the phase mean and range.

对每个 4 × 4 窗计算四个 2 × 2 子块的 Haar 细节能量均值，以及子块均值构成的粗尺度细节能量。取 log1p 后按四档亮度进行组内中心化，合并协方差与方差计算相关系数。遍历 16 个分析起点，记录相位均值与极差。

Circular integer translations permute the phase grid when both dimensions are divisible by four. The mean and range are invariant under this operation; ordinary cropping is not covered by the exact invariance statement.

当宽高均可被四整除时，循环整数平移仅置换相位格点，因此均值与极差不变。普通裁切不满足该严格不变性条件。

## Evidence / 实验记录

- [results.csv](results.csv): seven public examples and shift measurements / 七张公开样例与平移结果。
- [phase_profiles.csv](phase_profiles.csv): sixteen phase values per image / 各图像的十六相位原始统计。
- [sources.csv](sources.csv): source paths and reported Git blob SHA / 来源路径及接口返回的 Git blob SHA。
- [phase_profile.py](phase_profile.py): Python reproduction / Python 复现程序。

The recorded results were computed directly from image bytes using jpeg-js (blob a237d4037735de5446e63528ffdec1937ceac09d) and UPNG.js (blob d45ca109c8285970a1bc8fbeaa1044ec9441bfd4). Original bytes were not retained; source hashes were reported by the retrieval interface and not independently recomputed in that run.

原始统计直接解码图像字节，使用上述 jpeg-js、UPNG.js 源码版本。原图未保存；来源哈希由读取接口返回，原始运行未独立重算。

## Reproduction / 复现

From the repository root / 在仓库根目录执行：

```bash
python -m pip install -r requirements.txt
python experiments/phase-dependence/phase_profile.py --download
```

Or supply images in the experiment's ignored images directory, named according to sources.csv, then omit --download. Review permissions first. Hash mismatches and other failures are recorded in recomputed.json. Network acquisition was not fully validated in the Python environment; Pillow can differ from the original decoder.

也可按 sources.csv 的 local_file 列将原图置于实验目录下的 images 目录，再不带 --download 运行。下载前检查许可。哈希不符及其他失败写入 recomputed.json。Python 环境的网络下载尚未完整验证，Pillow 与原始解码器可能存在细微差异。

## Interpretation / 结果解释

The seven images are convenience examples, not an independent benchmark. Two Stable Diffusion outputs share one sketch; the sketch is not a photographic negative. Two additional repository labels have not been independently verified. Phase statistics are not origin probabilities. Real camera-source images can have strong phase variation.

七张图为便利样例，而非独立测试集。两张 Stable Diffusion 输出共用输入草图，草图不属于摄影阴性样本。另两张仓库标注的来源未经独立验证。相位统计值不是生成概率；真实采集图像也可能具有强相位波动。

A separate INP-X illustration check found differing dimensions (1880 × 1012 versus 1882 × 1020), identical JPEG quantization tables, and a median block RMSE of approximately 14.49 on a 0–255 scale after exploratory registration. These illustrations are not used as native aligned pairs.

INP-X 展示图的尺寸不同（1880 × 1012 与 1882 × 1020），JPEG 量化表相同，探索性配准后的图块 RMSE 中位数约为 14.49（灰度范围 0–255）。不将展示图作为原生配对样本。

References / 参考：Coifman & Donoho, Translation-Invariant De-Noising (1995); [Stable Diffusion](https://github.com/CompVis/stable-diffusion); [INP-X](https://arxiv.org/abs/2602.00192); [CIFAR Synthetic Evidence Image Corpus](https://github.com/UofT-CIFAR/Synthetic-Evidence-Image-Corpus).
