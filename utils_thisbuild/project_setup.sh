GITHUB="cei_pytorch_wavenet"
#cd ~/cei_pytorch_wavenet/utils_thisbuild
cd ~/$GITHUB/utils_thisbuild

# download necessary model file and map file 
# r9y9 tts prtrain/json
sudo /home/docker/.local/bin/gdown --id "1Z_LsKGIu-xiuFjkCl6SjELzDaVmbxlc0"
sudo /home/docker/.local/bin/gdown --id "1Qoy6o9BoI0oLjD6TTnn7ErBKMuaXDOp5"
# cei tts pretrain
sudo /home/docker/.local/bin/gdown --id "16clV1dTpIBjdZossSDXGnjroe8BjKTzL"
# r9y9 preset
sudo /home/docker/.local/bin/gdown --id "1uFBbk0iqyCDAAnrs8jqNgz3T3I9ewuB5"
sudo chown -R docker:docker ~/$GITHUB/utils_thisbuild
tar -xvf preset.tar.gz

# config git account info for git commit
sh -c 'git config --global user.name alvinyc'
sh -c 'git config --global user.email chen.yongcheng@gmail.com'

# move ljspeech inference model to checkpoints path 
mkdir -p ~/$GITHUB/wavenet_vocoder_2092a64/checkpoints
# necessary nltk data for train/synthesis
python -c "import nltk; nltk.download('cmudict')"
python -c "import nltk; nltk.download('punkt')"

