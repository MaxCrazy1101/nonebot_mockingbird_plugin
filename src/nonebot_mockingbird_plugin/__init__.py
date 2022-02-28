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
