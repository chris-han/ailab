conda activate bgmatting
$Env:CUDA_VISIBLE_DEVICES=0
python .\bg_matting.py `
  --name "Speaker" `
  --input "C:\\Users\\chha\\Videos\\Captures\\My Recorded Sessions\\2020-12-6-12-26-15\\" `
  --output_dir "C:\\Users\\chha\\Videos\\Captures\\My Recorded Sessions\\2020-12-6-12-26-15\\output\\" `
  --fixed_threshold "640," `
  --output_types "out,matte,compose" `
  --start 0 `
  --duration -1 `
  --background "C:\\Users\\chha\\Videos\\Microsoft.ZuneVideo_8wekyb3d8bbwe!Microsoft.ZuneVideo"
#conda deactivate