# Reproducibility & Facts — Mobile Vision-Transformer Benchmark for Fine-Grained Medicinal Plant Classification
_generated: 2026-08-28 14:54:53 AEST on carmack.une.edu.au_

## 1. Hardware / OS (training)
```
NVIDIA L40, 46068 MiB, 610.57.04
CPU cores: 32 | RAM: 
OS: Rocky Linux 9.8 (Blue Onyx)
```

## 2. Training venv (phd)
```
Python 3.9.25
numpy==2.0.2
pillow==11.3.0
scikit-learn==1.6.1
scipy==1.13.1
timm==1.0.28
torch==2.6.0+cu124
torchvision==0.21.0+cu124
```

## 3. Conversion venv (aiedge) — pinned set
```
Python 3.11.13
ai-edge-litert==2.1.0
ai-edge-torch==0.7.2
jax==0.10.2
jaxlib==0.10.2
litert-torch==0.8.0
tensorflow==2.19.0
torch==2.6.0+cpu
torchao==0.11.0
torchvision==0.21.0+cpu
```

## 4. Data / split (from results_baseline_s42.json)
```
num_classes = 2721
min_images_per_class = 25
split = {'train': 210327, 'val': 46419, 'test': 46419, 'val_frac': 0.15, 'test_frac': 0.15}
seed = 42
preprocess = baseline
```

## 5. Models (params + benchmark tflite sizes)
```
mobilenetv2_100: params=5,709,473  fp32=22.79MB  fp16=11.42MB
mobilevit_xxs: params=1,824,465  fp32=7.64MB  fp16=2.35MB
efficientformerv2_s0: params=4,209,490  fp32=17.31MB  fp16=8.72MB
```

## 6. ViT-B/16 accuracy ceiling (seed 42)
```
baseline ceiling top1 = 0.8467
clahe ceiling top1 = 0.8404
clahe_sobel ceiling top1 = 0.8372
sobel ceiling top1 = 0.6422
```

## 7. Accuracy results (3-seed mean+/-std)
```
model,preprocess,n_seeds,top1_mean,top1_std,top5_mean,top5_std,top10_mean,top10_std,macro_f1_mean,macro_f1_std,weighted_f1_mean,weighted_f1_std
efficientformerv2_s0,baseline,3,0.6895,0.0023,0.8522,0.0029,0.8913,0.0018,0.6775,0.0023,0.6876,0.0022
efficientformerv2_s0,clahe,3,0.6855,0.0019,0.8481,0.0016,0.8881,0.0019,0.6725,0.0023,0.6835,0.0021
efficientformerv2_s0,sobel,3,0.4796,0.0046,0.6866,0.0031,0.7539,0.0026,0.4664,0.0049,0.4762,0.0045
efficientformerv2_s0,clahe_sobel,3,0.6812,0.0009,0.8452,0.0019,0.8856,0.0007,0.6680,0.0017,0.6791,0.0011
mobilenetv2_100,baseline,3,0.6831,0.0015,0.8433,0.0021,0.8833,0.0018,0.6727,0.0024,0.6812,0.0018
mobilenetv2_100,clahe,3,0.6758,0.0005,0.8389,0.0008,0.8803,0.0013,0.6650,0.0010,0.6740,0.0007
mobilenetv2_100,sobel,3,0.4708,0.0036,0.6734,0.0042,0.7423,0.0023,0.4569,0.0029,0.4665,0.0041
mobilenetv2_100,clahe_sobel,3,0.6747,0.0017,0.8367,0.0016,0.8788,0.0016,0.6638,0.0015,0.6729,0.0016
mobilevit_xxs,baseline,3,0.5765,0.0020,0.7775,0.0010,0.8358,0.0013,0.5610,0.0016,0.5722,0.0023
mobilevit_xxs,clahe,3,0.5692,0.0006,0.7716,0.0015,0.8305,0.0021,0.5533,0.0004,0.5644,0.0007
mobilevit_xxs,sobel,3,0.3532,0.0030,0.5709,0.0030,0.6569,0.0025,0.3335,0.0028,0.3446,0.0032
mobilevit_xxs,clahe_sobel,3,0.5681,0.0008,0.7709,0.0016,0.8309,0.0012,0.5524,0.0006,0.5636,0.0004
```

## 8. Significance (paired t-test / Wilcoxon)
```
model,preprocess_vs_baseline,metric,n_seeds,baseline_mean,variant_mean,mean_delta,paired_t_p,wilcoxon_p
efficientformerv2_s0,clahe,top1,3,0.6895,0.6855,-0.0041,0.2027,0.5
efficientformerv2_s0,clahe,top5,3,0.8522,0.8481,-0.0041,0.03953,0.25
efficientformerv2_s0,clahe,top10,3,0.8913,0.8881,-0.0031,0.005394,0.25
efficientformerv2_s0,clahe,macro_f1,3,0.6775,0.6725,-0.0049,0.148,0.25
efficientformerv2_s0,clahe,weighted_f1,3,0.6876,0.6835,-0.0042,0.2043,0.5
efficientformerv2_s0,sobel,top1,3,0.6895,0.4796,-0.2099,0.000254,0.25
efficientformerv2_s0,sobel,top5,3,0.8522,0.6866,-0.1656,0.0002256,0.25
efficientformerv2_s0,sobel,top10,3,0.8913,0.7539,-0.1374,0.00013,0.25
efficientformerv2_s0,sobel,macro_f1,3,0.6775,0.4664,-0.2111,0.0002233,0.25
efficientformerv2_s0,sobel,weighted_f1,3,0.6876,0.4762,-0.2115,0.0002434,0.25
efficientformerv2_s0,clahe_sobel,top1,3,0.6895,0.6812,-0.0083,0.04752,0.25
efficientformerv2_s0,clahe_sobel,top5,3,0.8522,0.8452,-0.0070,0.04585,0.25
efficientformerv2_s0,clahe_sobel,top10,3,0.8913,0.8856,-0.0057,0.02601,0.25
efficientformerv2_s0,clahe_sobel,macro_f1,3,0.6775,0.6680,-0.0095,0.0535,0.25
efficientformerv2_s0,clahe_sobel,weighted_f1,3,0.6876,0.6791,-0.0085,0.04612,0.25
mobilenetv2_100,clahe,top1,3,0.6831,0.6758,-0.0073,0.007335,0.25
mobilenetv2_100,clahe,top5,3,0.8433,0.8389,-0.0044,0.06608,0.25
mobilenetv2_100,clahe,top10,3,0.8833,0.8803,-0.0030,0.01113,0.25
mobilenetv2_100,clahe,macro_f1,3,0.6727,0.6650,-0.0076,0.0198,0.25
mobilenetv2_100,clahe,weighted_f1,3,0.6812,0.6740,-0.0072,0.007458,0.25
mobilenetv2_100,sobel,top1,3,0.6831,0.4708,-0.2124,4.959e-05,0.25
mobilenetv2_100,sobel,top5,3,0.8433,0.6734,-0.1699,0.0002063,0.25
mobilenetv2_100,sobel,top10,3,0.8833,0.7423,-0.1410,3.406e-05,0.25
mobilenetv2_100,sobel,macro_f1,3,0.6727,0.4569,-0.2157,1.7e-05,0.25
mobilenetv2_100,sobel,weighted_f1,3,0.6812,0.4665,-0.2147,6.476e-05,0.25
mobilenetv2_100,clahe_sobel,top1,3,0.6831,0.6747,-0.0085,0.01058,0.25
mobilenetv2_100,clahe_sobel,top5,3,0.8433,0.8367,-0.0066,0.02902,0.25
mobilenetv2_100,clahe_sobel,top10,3,0.8833,0.8788,-0.0045,0.04756,0.25
mobilenetv2_100,clahe_sobel,macro_f1,3,0.6727,0.6638,-0.0089,0.01045,0.25
mobilenetv2_100,clahe_sobel,weighted_f1,3,0.6812,0.6729,-0.0083,0.009035,0.25
mobilevit_xxs,clahe,top1,3,0.5765,0.5692,-0.0073,0.01406,0.25
mobilevit_xxs,clahe,top5,3,0.7775,0.7716,-0.0059,0.004229,0.25
mobilevit_xxs,clahe,top10,3,0.8358,0.8305,-0.0054,0.007674,0.25
mobilevit_xxs,clahe,macro_f1,3,0.5610,0.5533,-0.0077,0.007783,0.25
mobilevit_xxs,clahe,weighted_f1,3,0.5722,0.5644,-0.0078,0.01787,0.25
mobilevit_xxs,sobel,top1,3,0.5765,0.3532,-0.2233,3.174e-05,0.25
mobilevit_xxs,sobel,top5,3,0.7775,0.5709,-0.2066,3.212e-05,0.25
mobilevit_xxs,sobel,top10,3,0.8358,0.6569,-0.1790,2.281e-05,0.25
mobilevit_xxs,sobel,macro_f1,3,0.5610,0.3335,-0.2275,3.342e-05,0.25
mobilevit_xxs,sobel,weighted_f1,3,0.5722,0.3446,-0.2277,2.877e-05,0.25
mobilevit_xxs,clahe_sobel,top1,3,0.5765,0.5681,-0.0084,0.02253,0.25
mobilevit_xxs,clahe_sobel,top5,3,0.7775,0.7709,-0.0066,0.0131,0.25
mobilevit_xxs,clahe_sobel,top10,3,0.8358,0.8309,-0.0049,0.0001987,0.25
mobilevit_xxs,clahe_sobel,macro_f1,3,0.5610,0.5524,-0.0085,0.01627,0.25
mobilevit_xxs,clahe_sobel,weighted_f1,3,0.5722,0.5636,-0.0087,0.02267,0.25
```

## 9. ML Kit deployment pipeline (the 6 shipped models)
Six deployable models = 3 architectures x {fp16,fp32}, all from baseline_s42 (latency is
architecture/precision-dependent, not seed/preprocess-dependent). Pipeline:

1. labels.txt  (make_labels.py) — class-index order = sorted class-folder names filtered
   to >=25 images; seed/preprocess-independent; one file for all models; verified 2721==output dim.
2. Softmax head  (export_softmax_tflite.py for CNNs; baked into the MobileViT wrapper) —
   ML Kit needs a probability distribution, not logits. Softmax is monotonic => argmax/top-k/
   accuracy unchanged.
3. NHWC input — onnx2tf emits NHWC (CNNs OK). MobileViT (litert-torch) is NCHW [1,3,224,224];
   re-exported via an NHWC wrapper (reexport_mobilevit_nhwc.py) to [1,224,224,3] for ML Kit.
4. Per-model NormalizationOptions metadata  (write_metadata.py):
     mobilenetv2_100, efficientformerv2_s0 : ImageNet  mean=[123.675,116.28,103.53] std=[58.395,57.12,57.375]  (0..255 scale)
     mobilevit_xxs                         : none      mean=[0,0,0] std=[255,255,255]  (plain /255)   <-- DIFFERENT
   Baking ImageNet stats into MobileViT would silently corrupt it.
5. EfficientFormerV2 GELU -> onnx2tf '-rtpo Erf GeLU' (native polynomial approx) to avoid a
   FlexErf op ML Kit cannot run.

TWO FOOTNOTES (both on the latency path, both verified NOT to change predictions):
 (a) MobileViT carries a baked-in NHWC transpose.
 (b) EfficientFormerV2 uses an approximated GELU.
Parity check (parity_check_deployed.py): PyTorch vs deployed fp16/fp32 top-1 == identical for
all 3 models on known test images => the deployed model IS the benchmarked model.

Inference runtime: ML Kit ImageClassifier, default configuration (no thread control exposed),
identical across devices; same as our prior MDPI IoT paper for cross-paper comparability.

## 10. On-device latency — data anomaly to resolve
Latency measured under ML Kit's DEFAULT runtime, which selects its own backend per
device/model. Latency is therefore runtime-dependent, not raw model compute:
 - Same model spans ~188 ms (Oppo) to ~5341 ms (Xiaomi, EfficientFormerV2 fp16) -> ~28x.
 - fp16 ~= fp32 latency on Oppo/Realme (XNNPACK upcasts fp16 on CPU); fp16 uses less RAM.
ACTION: report latency as runtime-dependent; RAM column is clean (~280-343 MB).
