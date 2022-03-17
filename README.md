# Nonebot MockingBird Support

> 如果需要直接使用本插件，请将训练好的模型放在机器人根目录下命名为 `mocking_model.pt` , 将音频放置同样的目录下命名 `recoder.wav`

## [Mocking Bird](https://github.com/babysor/MockingBird)
![mockingbird](https://user-images.githubusercontent.com/12797292/131216767-6eb251d6-14fc-4951-8324-2722f0cd4c63.jpg)

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

### [DEMO VIDEO](https://www.bilibili.com/video/BV17Q4y1B7mY/) | [Wiki教程](https://github.com/babysor/MockingBird/wiki/Quick-Start-(Newbie)) ｜ [训练教程](https://vaj2fgg8yn.feishu.cn/docs/doccn7kAbr3SJz0KM0SIDJ0Xnhd)


## 开始
### 1. 安装要求
> 按照原始存储库测试您是否已准备好所有环境。
**Python 3.7 或更高版本** 需要运行工具箱。

* 安装 [PyTorch](https://pytorch.org/get-started/locally/)。
> 如果在用 pip 方式安装的时候出现 `ERROR: Could not find a version that satisfies the requirement torch==1.9.0+cu102 (from versions: 0.1.2, 0.1.2.post1, 0.1.2.post2)` 这个错误可能是 python 版本过低，3.9 可以安装成功
* 安装 [ffmpeg](https://ffmpeg.org/download.html#get-packages)。

### 2. 训练模型
> 此部分请参考原仓库，本仓库精简了部分关于训练模型的代码

#### 2.3使用社区预先训练好的合成器（与2.2二选一）
> 当实在没有设备或者不想慢慢调试，可以使用社区贡献的模型(欢迎持续分享):

| 作者 | 下载链接 | 效果预览 | 信息 |
| --- | ----------- | ----- | ----- |
| 作者 | https://pan.baidu.com/s/1iONvRxmkI-t1nHqxKytY3g  [百度盘链接](https://pan.baidu.com/s/1iONvRxmkI-t1nHqxKytY3g) 4j5d |  | 75k steps 用3个开源数据集混合训练
| 作者 | https://pan.baidu.com/s/1fMh9IlgKJlL2PIiRTYDUvw  [百度盘链接](https://pan.baidu.com/s/1fMh9IlgKJlL2PIiRTYDUvw) 提取码：om7f |  | 25k steps 用3个开源数据集混合训练, 切换到tag v0.0.1使用
|@FawenYo | https://drive.google.com/file/d/1H-YGOUHpmqKxJ9FRc6vAjPuqQki24UbC/view?usp=sharing [百度盘链接](https://pan.baidu.com/s/1vSYXO4wsLyjnF3Unl-Xoxg) 提取码：1024  | [input](https://github.com/babysor/MockingBird/wiki/audio/self_test.mp3) [output](https://github.com/babysor/MockingBird/wiki/audio/export.wav) | 200k steps 台湾口音需切换到tag v0.0.1使用
|@miven| https://pan.baidu.com/s/1PI-hM3sn5wbeChRryX-RCQ 提取码：2021 | https://www.bilibili.com/video/BV1uh411B7AD/ | 150k steps 注意：根据[issue](https://github.com/babysor/MockingBird/issues/37)修复 并切换到tag v0.0.1使用

#### 2.4 训练声码器 (可选)

> 预置默认使用HifiGan

#### 3 使用插件

> 主要是使用`MockingBirdOnlyForUse`库的MockingBird, Params

    ```python
    使用MockingBird时自定义的参数

        Args:
            text (str): 生成语音的目标文字
            recoder_path (Path): 目标录音目录
            synthesizer_path (Path, optional): Synthesizer模型位置. 为None时使用已缓存的模型，如果没有，将会报错。 Defaults to None.
            accuracy (int, optional): Accuracy(精度) 范围3~9. Defaults to 4.
            steps (int, optional): MaxLength(最大句长) 范围1~10. Defaults to 4.
            style_idx (int, optional): Style 范围 -1~9. Defaults to -1.
            save_path (Path, optional): 生成后保存到文件的路径，不填会返回ByteIO类型，填上返回的是Path类型. Defaults to None.
            vocoder (str, optional): 选择Vocoder模型，影响不大，默认使用HifiGan，可选WaveRNN. Defaults to "HifiGan".
            seed (int, optional): 种子，不建议修改. Defaults to None.
            trim_silences (bool): Defaults to False.
    ```
```python
from nonebot_mockingbird_plugin import MockingBird, Params, part

part.keywords["synthesizer_path"] = Path("azusa_200k.pt")
part.keywords["recoder_path"] = Path("temp3.wav")

voice = on_command("讲话", aliases={"语音"}, block=True, rule=to_me(), priority=1)

@voice.handle()
async def _(args: Message = CommandArg()):
    await voice.finish(MessageSegment.record(MockingBird.genrator_voice(part(args))))

```
    
```python
# 样例
import os.path

from MockingBirdOnlyForUse import MockingBird, Params
from MockingBirdOnlyForUse import logger as mocking_logger
from pathlib import Path
from nonebot import export, on_command
from functools import partial

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.log import logger as nonebot_logger


root = os.path.abspath(os.path.join(__file__, "..", "resources"))
mocking_logger.logger = nonebot_logger  # 覆盖使用nonebot的logger

MockingBird.init(
    Path(os.path.join(root, "encoder.pt")),
    Path(os.path.join(root, "g_hifigan.pt")),
    "HifiGan",
)


part = partial(
    Params,
    recoder_path=Path("recoder.wav"),
    synthesizer_path=Path("mocking_model.pt"),
    vocoder="HifiGan",
)

export = export()
export.MockingBird = MockingBird
export.Params = Params
export.part = part

voice = on_command("讲话", aliases={"语音"}, block=True, rule=to_me(), priority=1)


@voice.handle()
async def _(args: Message = CommandArg()):
    params = part(args)
    params.text = args.extract_plain_text()
    await voice.finish(MessageSegment.record(MockingBird.genrator_voice(params)))

```

#### 4. 其他模型
> [电梓播放器](https://www.bilibili.com/video/BV1RF411z7C5)
