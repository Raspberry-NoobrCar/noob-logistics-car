# -*- coding: utf-8 -*-
import pygame

voiceAssetPath = "voiceModel"

def playAudio(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        continue
    
    # 签收超时
def timeout_voice():
    playAudio(f"{voiceAssetPath}/timeout.wav")
    
    # 已送达及时签收
def delivery_voice():
    playAudio(f"{voiceAssetPath}/depositExpress.wav")
    
    # 正在装货中
def loading_voice():
    playAudio(f"{voiceAssetPath}/loading.wav")

    # 扫码成功
def signIn_voice():
     playAudio(f"{voiceAssetPath}/signIn.wav")
        
    # 请出示二维码
def scanQR_voice():
    playAudio(f"{voiceAssetPath}/scanQR.wav")
        
    # 装配货物
def loadGood_voice():
    playAudio(f"{voiceAssetPath}/loadGood.wav")
        
    # 货物装配成功    
def loadSuccess_voice():
    playAudio(f"{voiceAssetPath}/loadSuccess.wav")
    playAudio(f"{voiceAssetPath}/loadSuccessVideo.wav")

    # 前方障碍物
def tackle_voice():
    playAudio(f"{voiceAssetPath}/tackle.wav")
    
    #前方禁止通行
def forbid_voice():
    playAudio(f"{voiceAssetPath}/forbid.wav")
    
    # 检测到前方人行横道    
def pedestrianCrossing_voice():
    playAudio(f"{voiceAssetPath}/pedestrianCrossing.wav")

    # 送货完毕
def deliveryFinished():
    playAudio(f"{voiceAssetPath}/deliveryFinished.wav")

    # 没有可到达的路径
def noPathFound():
    playAudio(f"{voiceAssetPath}/noPathFound.wav")

    # 重新装货
def loadAgain_voice():
    playAudio(f"{voiceAssetPath}/loadAgain.wav")

    # 装货完毕
def loadFinished_voice():
    playAudio(f"{voiceAssetPath}/loadFinished.wav")

    # 检测到行人离去，重新启动
def rebooting_voice():
    playAudio(f"{voiceAssetPath}/rebooting.wav")
    
    # 检测到二维码不匹配
def notMatch_voice():
    playAudio(f"{voiceAssetPath}/notMatch.wav")
    

    
if __name__ == "__main__":
#     timeout_voice()
    delivery_voice()
#     loading_voice()
#     signIn_voice()
#     scanQR_voice()
#     loadGood_voice()
#     loadSuccess_voice()
#     tackle_voice()
#     deliveryFinished()
#     noPathFound()
#     loadAgain_voice()
#     loadFinished_voice()
#     rebooting_voice()
#     notMatch_voice()
