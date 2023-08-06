# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from typing import List, Union
import struct
from datetime import datetime

from .com_definition import (
    Probability,
    LabeledProbability,
    CommandCode,
    Judgement,
    ProbabilityType,
)
from .com_base import (
    BaseCommand,
    HEADER_SIZE,
)
from .connection import Connection
from .inspect_image import ImageFormat, InspectImage


class InspectCommand(BaseCommand):

    _CODE = CommandCode.INSPECT
    PROB_SIZE = 13
    LABELED_PROB_SIZE = 14
    PROB_OFFSET = 20 - HEADER_SIZE

    # Requestパラメータ
    _inspect_id = None
    _model_id = None
    _data_format = None
    _image_data = b''
    # Replayパラメータ
    _result = Judgement.FAILED
    _prob_size = 0
    _prob_list: List[Probability] = []

    # ログの詳細出力
    verbose = False

    def __init__(
        self,
        inspect_id: int,
        model_id: int,
        data_format: ImageFormat = None,
        image_data: Union[bytes, InspectImage] = b'',
        connection: Connection = None,
    ):
        """ Inspect コマンド制御

        Args:
            inspect_id (int):           検査番号
            model_id (int):             モデル番号
            data_format:                送信する検査画像フォーマット
                (None, default):        image_data のフォーマット利用
                (ImageFormat):          送信フォーマットを指定
            image_data:
                (InspectImage):         検査画像データ
            connection:
                (None, default)         デフォルトの接続利用
                (Connection, option):   通信対象のTCP接続

        Raises:
            TypeError:      data_format が None で image_data が bytes
            ValueError:     data_format が NDARRAY
        """
        super().__init__(connection)
        # 型チェック
        if (data_format is None) and not issubclass(type(image_data), InspectImage):
            raise TypeError
        # 要求データの設定
        if inspect_id is None:
            self._inspect_id = self.get_datetime_id()
        else:
            self._inspect_id = inspect_id
        self._model_id = model_id
        self._data_format = data_format or image_data.format
        if self._data_format == ImageFormat.NDARRAY:
            raise ValueError
        self._image_data = image_data
        self._extension = self._image_data
        self.encode_data()

        # 応答の変数定義はクラス定義を引き継ぎ
        # self._result = Judgement.FAILED
        # self._prob_size = 0
        # self._prob_list = []

    def encode_data(self):
        """ Inspect コマンドの送信データ生成
        """
        send_params = (
            self._inspect_id,
            self._model_id,
            self._data_format,
        )
        self.data = struct.pack('< Q B B', *send_params)

    def send(self, timeout: float = None):
        """ Inspect コマンドの要求を送信

        Args:
            timeout:
                (None, default):    None はタイムアウト無し
                (float, option):    タイムアウト時間[sec]

        Raises:
            送信タイムアウト（socket.timeout）を含む通信例外を送出
        """
        super().send(extension=self.extension, timeout=timeout)

    def recv(self, timeout: float = None):
        """ Inspect コマンドの応答を受信

        Args:
            timeout:
                (None, default):    None はタイムアウト無し
                (float, option):    タイムアウト時間[sec]

        Raises:
            送信タイムアウト（socket.timeout）を含む通信例外を送出
            RuntimeError    不正な応答受信
        """
        super().recv(timeout=timeout)

    def _decode_reply(self, reply: bytes):
        """ Inspect コマンドの応答内容確認

        Args:
            reply (bytes):      受信応答データ（ヘッダ以外）
        """
        if not reply:
            self._result = Judgement.FAILED
            self._prob_size = 0
            self._prob_list = []
            return

        inspect_id, result, prob_type, prob_size = struct.unpack(
            '< Q B B H',
            reply[:self.PROB_OFFSET]
        )
        prob_data = reply[self.PROB_OFFSET:]

        # 受信データのチェック
        if self._inspect_id != inspect_id:
            raise RuntimeError(
                f'mismatched inspect_id '
                f'recv:{inspect_id}(=0x{inspect_id:#016X}) != '
                f'send:{self._inspect_id}(=0x{self._inspect_id:#016X})')

        # 受信データの格納
        self._result = Judgement(result)
        self._prob_type = prob_type
        self._prob_size = prob_size
        self._prob_list = []
        if prob_type == ProbabilityType.LABELED:
            for offset in range(
                0, prob_size * self.LABELED_PROB_SIZE, self.LABELED_PROB_SIZE
            ):
                x1, y1, x2, y2, typ, label, prob = struct.unpack(
                    '< H H H H B B f',
                    prob_data[offset:offset + self.LABELED_PROB_SIZE]
                )
                prob = LabeledProbability(x1, y1, x2, y2, typ, label, prob)
                self._prob_list .append(prob)
        else:
            for offset in range(0, prob_size * self.PROB_SIZE, self.PROB_SIZE):
                x1, y1, x2, y2, typ, prob = struct.unpack(
                    '< H H H H B f',
                    prob_data[offset:offset + self.PROB_SIZE]
                )
                prob = Probability(x1, y1, x2, y2, typ, prob)
                self._prob_list .append(prob)

    @staticmethod
    def get_datetime_id() -> int:
        """ デフォルトで利用する日時算出の検査ID取得

        Returns:
            int:        日時から算出した検査ID
        """
        dt = datetime.now()
        dtid = int(dt.strftime('%Y%m%d%H%M%S%f')) // 1000
        return dtid

    def __str__(self) -> str:
        image_size = self._extension.get_size(self._data_format)
        string = (
            f'{super().__str__()} '
            f'InspectID: {self._inspect_id}(=0x{self._inspect_id:016X}), '
            f'ModelID: {self._model_id}, '
            f'DataFormat: 0x{self._data_format:02X}, '
            f'ImageData: {image_size:,d} bytes -> '
        )
        if self.is_received_ack:
            string += (
                f'Result: {str(self._result)}, '
                f'ProbabilityType: {self._prob_type}, '
                f'ProbabilitySize: {self._prob_size}, '
                f'ProbabilityList: {self._prob_size} items '
            )
            if self.verbose:
                for prob in self._prob_list:
                    string += '\n    ' + str(prob)
        return string

    # 読み取り専用変数の定義
    @property
    def inspect_id(self) -> int:
        return self._inspect_id

    @property
    def model_id(self) -> int:
        return self._model_id

    @property
    def data_format(self) -> ImageFormat:
        return self._data_format

    @property
    def image_data(self) -> InspectImage:
        return self._image_data

    @property
    def extension(self) -> bytes:
        return self._extension.get_image(self._data_format)

    @property
    def result(self) -> Judgement:
        return self._result

    @property
    def prob_size(self) -> int:
        return self._prob_size

    @property
    def prob_list(self) -> List[Probability]:
        return self._prob_list
