# E13 — 分析格点相位与跨尺度依赖

`results.csv` 与 `phase_profiles.csv` 为本轮直接解码七张公开图像后获得的实验结果。原始分析采用 JavaScript 中的 jpeg-js 和 UPNG.js，解码器源码 blob 分别为 a237d4037735de5446e63528ffdec1937ceac09d、d45ca109c8285970a1bc8fbeaa1044ec9441bfd4。图像原始字节通过 GitHub 文件读取接口在独立运行环境中读取；未保存在本实验包。sources.csv 的 blob SHA 由接口返回，尚未独立重新计算。七张图是便利样例，而非独立测试集；两张 SD 图共用输入；仓库 AI/human 标签仅为原作者文件名标签。不可用来估计检测准确率。

Python 复现实现：`pip install numpy pillow`，随后 `python phase_profile.py --download`，或把源图像按 sources.csv 的 local_file 列保存至 images/ 后运行 `python phase_profile.py`。下载功能在当前网络环境未实际完成；代码核查 Git blob SHA，失败会记录而不会使用数据。Pillow 的 JPEG 解码可能与原始 JS 解码有小差异。原始尺寸裁剪到宽高可被4整除；比较同尺寸左上裁块与偏移(1,1)裁块，循环边界仅用于验证平移群性质。非循环裁切的边缘效应与内容变化不会被该性质严格消除。

指标：4×4 窗内计算四个 2×2 Haar 细节能量均值，以及四个子块均值的粗尺度 Haar 细节能量；分别取 log1p，按四档亮度进行组内中心化后合并协方差与方差。16 个采样格点相位的均值、极差分别记录。不是 E12 的秩统计量本身。相位平均和极差在循环整数平移下不变，但不等同于生成特异性。真实原始图也能表现出较强相位波动。跨尺度依赖值不是 AI 概率。

INP-X 示意图审核：original.jpeg 1880×1012, 258803 字节；inpainted.jpeg 1882×1020, 274574 字节。量化表相同；鲁棒低分辨率网格配准后，351个64×64块 RMSE 中位数约14.49/255。未获得原生掩膜与严格配对图，不用于效果评价。

参考：Coifman & Donoho, Translation-Invariant De-Noising (1995); CompVis/stable-diffusion README img2img；INP-X arXiv:2602.00192；UofT-CIFAR/Synthetic-Evidence-Image-Corpus。相位平均等方法属于已有理论。本轮不提出首创性主张。
