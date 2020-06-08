conda activate bgmatting
$Env:CUDA_VISIBLE_DEVICES=0
python .\bg_matting.py `
  --name "Speaker" `
  --input C:\Users\chha\Videos\Captures\My Recorded Sessions\2020-08-6-17-29-19\ `
  --output_dir C:\Users\chha\Videos\Captures\My Recorded Sessions\2020-08-6-17-29-19\output\ `
  --fixed_threshold "640," `
  --start 34 `
  --duration 234
conda deactivate