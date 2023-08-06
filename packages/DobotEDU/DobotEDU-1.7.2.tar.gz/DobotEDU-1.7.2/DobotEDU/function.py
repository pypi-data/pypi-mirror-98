# -*- coding: utf-8 -*-
import requests
import json
import base64
import sounddevice as sd
import cv2
import uuid
from DobotRPC import loggers


class Util(object):
    def get_image(self,
                  timeout: int,
                  port: int,
                  flip=False) -> str:  # timeout为拍照时间,port相机端口，flip是否水平翻转标志
        cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)  # 用摄像头拍照
        t = timeout * 1000
        cnt = timeout + 1
        while True:
            ret, frame = cap.read()  # 读取摄像头拍照的图片
            if flip:
                frame = cv2.flip(frame, 1)  # 左右翻转摄像头获取的照片
            try:
                image_data = frame.copy()
            except AttributeError:
                raise AttributeError(
                    "Please check if there is a problem with the camera")
            dst = cv2.putText(frame, str(cnt), (300, 300),
                              cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4,
                              4)
            cv2.imshow("video", dst)  # 显示照片
            c = cv2.waitKey(1)  # 显示的帧数
            if c == 27:
                break
            if t == 0:
                return image_data
            if t % 1000 == 0:
                cnt = cnt - 1
            t = t - 40

    def record(self, timeout: int) -> str:
        voice_data = sd.rec(int(timeout * 16000), samplerate=16000, channels=1)
        sd.wait()
        return voice_data


class BaseAI(object):
    def __init__(self, token=None):
        self._token = token
        self._url = "https://dobotlab.dobot.cc/api/ai/tencent-transmit"

    @property
    def _headers(self):
        assert self._token is not None
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "ClientType": "DobotEDU"
        }

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url + "/api/ai/tencent-transmit"

    def _format(self, data):
        f_data = None
        try:
            data = data.content.decode(encoding="utf8")
            data = json.loads(data)
            status = data['status']
            if status == 'error':
                err = data['message']
                err = Exception(err)
                raise err
            else:
                f_data = json.loads(data['data'])
        except Exception as e:
            loggers.get('Function').exception(e)
            raise e
        return f_data


class Tiia(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def sort(self, image: str) -> str:
        payload = {"data": "{\"ImageBase64\":\"" + image + "\"}", "type": 1}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data


class Face(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def match(self, image_a: str, image_b: str) -> str:
        payload = {
            "data":
            "{\"ImageA\":\"" + str(image_a, 'utf-8') + "\", \"ImageB\":\"" +
            str(image_b, 'utf-8') + "\"}",
            "type":
            2
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is not None:
            return data["Score"]
        return data

    def detect(self,
               image,
               face_attributes: int = 0,
               quality_detection: int = 0) -> str:
        payload = {
            "data":
            "{\"Image\":\"" + str(image, 'utf-8') +
            "\", \"NeedFaceAttributes\":" + str(face_attributes) +
            ",\"NeedQualityDetection\":" + str(quality_detection) + "}",
            "type":
            3
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data

    def search(self, group_ids: list, image: str) -> str:
        payload = {
            "data":
            "{\"GroupIds\":" + str(group_ids) + ", \"Image\":\"" +
            str(image, 'utf-8') + "\"}",
            "type":
            4
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data

    def create_library(self, group_name: str, group_id: str):
        payload = {
            "data":
            "{\"GroupName\":\"" + group_name + "\", \"GroupId\":\"" +
            group_id + "\"}",
            "type":
            5
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data

    def create_person(self, group_id, person_name, person_id, image):
        payload = {
            "data":
            "{\"GroupId\":\"" + group_id + "\", \"PersonName\":\"" +
            person_name + "\", \"PersonId\":\"" + person_id +
            "\",  \"Image\":\"" + str(image, 'utf-8') + "\"}",
            "type":
            7
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data

    def person_info(self, person_id):
        payload = {"data": "{\"PersonId\":\"" + person_id + "\"}", "type": 14}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data

    def delete_library(self, group_id):
        payload = {"data": "{\"GroupId\":\"" + group_id + "\"}", "type": 6}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data


class Speech(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def asr(self, voice):
        payload = {
            "data":
            "{\"ProjectId\":1,\"SubServiceType\":2,\"EngSerViceType\":\"16k\",\"SourceType\":\
            1,\"VoiceFormat\":\"wav\",\"UsrAudioKey\":\"erwe\",\"Data\": \"" +
            str(voice, "utf-8") + "\",\"DataLen\":1500}",
            "type":
            9
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is not None:
            return data["Result"]
        return data

    def synthesis(self, text, language):
        u = str(uuid.uuid4())
        payload = {
            "data":
            "{\"Text\":" + text + ",\"SessionId\":" + u +
            ",\"ModelType\":2,\"Codec\":" + "mp3" + ",\"PrimaryLanguage\": " +
            str(language) + "}",
            "type":
            10
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is not None:
            data = data['Audio']
            return base64.b64decode(data)
        return data


class Ocr(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def basic_general(self, image):
        payload = {
            "data": "{\"ImageBase64\":\"" + str(image, "utf-8") + "\"}",
            "type": 8
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is None:
            return data

        ocr_data = ""
        for i in range(len(data["TextDetections"])):
            ocr_data = ocr_data + data["TextDetections"][i][
                'DetectedText'] + "\n"
        return ocr_data

    def id_card(self, image, card_side):
        payload = {
            "data":
            "{\"Action\": \"IDCardOCR\", \"Version\":\"2018-11-19\", \"Region\":\"ap-guangzhou\", \"ImageBase64\":\""
            + str(image, "utf-8") + "\", \"CardSide\": " + card_side + "}",
            "type":
            19
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data


class Nlp(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def topic(self, text):
        payload = {
            "data": "{\"Text\":\"" + text + "\",\"Flag\":2}",
            "type": 11
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is not None:
            return data['Classes'][0]['FirstClassName']
        return data


class Tmt(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def translation(self, source_text, source, target):
        payload = {
            "data":
            "{\"SourceText\":\"" + source_text + "\",\"Source\":\"" + source +
            "\", \"Target\":\"" + target + "\",\"ProjectId\":0 }",
            "type":
            12
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        if data is not None:
            return data["TargetText"]
        return data


class Robot(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def conversation(self, query, session_id):
        payload = {
            "data":
            "{\"log_id\":\"7758521\",\"version\":\"2.0\",\"service_id\":\"S48724\",\
            \"session_id\":\"" + session_id + "\",\"request\":{\"query\":\"" +
            query + "\",\"user_id\":\"222333\"},\
            \"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1037318\",\
            \"1044905\",\"1044907\",\"1044908\",\"1044906\"]}}}",
            "type":
            15
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data
