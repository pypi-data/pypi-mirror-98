# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import BinaryIO, List, Dict


class ClassifyVehicleInsuranceRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class ClassifyVehicleInsuranceAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class ClassifyVehicleInsuranceResponseBodyDataLabels(TeaModel):
    def __init__(
        self,
        score: float = None,
        name: str = None,
    ):
        self.score = score
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.score is not None:
            result['Score'] = self.score
        if self.name is not None:
            result['Name'] = self.name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self


class ClassifyVehicleInsuranceResponseBodyData(TeaModel):
    def __init__(
        self,
        labels: List[ClassifyVehicleInsuranceResponseBodyDataLabels] = None,
        threshold: float = None,
    ):
        self.labels = labels
        self.threshold = threshold

    def validate(self):
        if self.labels:
            for k in self.labels:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Labels'] = []
        if self.labels is not None:
            for k in self.labels:
                result['Labels'].append(k.to_map() if k else None)
        if self.threshold is not None:
            result['Threshold'] = self.threshold
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.labels = []
        if m.get('Labels') is not None:
            for k in m.get('Labels'):
                temp_model = ClassifyVehicleInsuranceResponseBodyDataLabels()
                self.labels.append(temp_model.from_map(k))
        if m.get('Threshold') is not None:
            self.threshold = m.get('Threshold')
        return self


class ClassifyVehicleInsuranceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: ClassifyVehicleInsuranceResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = ClassifyVehicleInsuranceResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class ClassifyVehicleInsuranceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ClassifyVehicleInsuranceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ClassifyVehicleInsuranceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectIPCObjectRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        # 图片URL地址
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectIPCObjectResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        type: str = None,
        score: float = None,
        box: List[int] = None,
        target_rate: float = None,
    ):
        self.type = type
        self.score = score
        self.box = box
        self.target_rate = target_rate

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.score is not None:
            result['Score'] = self.score
        if self.box is not None:
            result['Box'] = self.box
        if self.target_rate is not None:
            result['TargetRate'] = self.target_rate
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('Box') is not None:
            self.box = m.get('Box')
        if m.get('TargetRate') is not None:
            self.target_rate = m.get('TargetRate')
        return self


class DetectIPCObjectResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectIPCObjectResponseBodyDataElements] = None,
        width: int = None,
        height: int = None,
    ):
        self.elements = elements
        self.width = width
        self.height = height

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectIPCObjectResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        return self


class DetectIPCObjectResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectIPCObjectResponseBodyData = None,
    ):
        # Id of the request
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectIPCObjectResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectIPCObjectResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectIPCObjectResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectIPCObjectResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectMainBodyRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectMainBodyAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class DetectMainBodyResponseBodyDataLocation(TeaModel):
    def __init__(
        self,
        width: int = None,
        height: int = None,
        y: int = None,
        x: int = None,
    ):
        self.width = width
        self.height = height
        self.y = y
        self.x = x

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        if self.y is not None:
            result['Y'] = self.y
        if self.x is not None:
            result['X'] = self.x
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        if m.get('X') is not None:
            self.x = m.get('X')
        return self


class DetectMainBodyResponseBodyData(TeaModel):
    def __init__(
        self,
        location: DetectMainBodyResponseBodyDataLocation = None,
    ):
        self.location = location

    def validate(self):
        if self.location:
            self.location.validate()

    def to_map(self):
        result = dict()
        if self.location is not None:
            result['Location'] = self.location.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Location') is not None:
            temp_model = DetectMainBodyResponseBodyDataLocation()
            self.location = temp_model.from_map(m['Location'])
        return self


class DetectMainBodyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectMainBodyResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectMainBodyResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectMainBodyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectMainBodyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectMainBodyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectObjectRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectObjectAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class DetectObjectResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        type: str = None,
        boxes: List[int] = None,
        score: float = None,
    ):
        self.type = type
        self.boxes = boxes
        self.score = score

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class DetectObjectResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectObjectResponseBodyDataElements] = None,
        width: int = None,
        height: int = None,
    ):
        self.elements = elements
        self.width = width
        self.height = height

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectObjectResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        return self


class DetectObjectResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectObjectResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectObjectResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectObjectResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectObjectResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectObjectResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectTransparentImageRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectTransparentImageAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class DetectTransparentImageResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        transparent_image: int = None,
    ):
        self.transparent_image = transparent_image

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.transparent_image is not None:
            result['TransparentImage'] = self.transparent_image
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TransparentImage') is not None:
            self.transparent_image = m.get('TransparentImage')
        return self


class DetectTransparentImageResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectTransparentImageResponseBodyDataElements] = None,
    ):
        self.elements = elements

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectTransparentImageResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        return self


class DetectTransparentImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectTransparentImageResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectTransparentImageResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectTransparentImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectTransparentImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectTransparentImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectVehicleRequest(TeaModel):
    def __init__(
        self,
        image_type: int = None,
        image_url: str = None,
    ):
        self.image_type = image_type
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_type is not None:
            result['ImageType'] = self.image_type
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageType') is not None:
            self.image_type = m.get('ImageType')
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectVehicleAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
        image_type: int = None,
    ):
        self.image_urlobject = image_urlobject
        self.image_type = image_type

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        if self.image_type is not None:
            result['ImageType'] = self.image_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        if m.get('ImageType') is not None:
            self.image_type = m.get('ImageType')
        return self


class DetectVehicleResponseBodyDataDetectObjectInfoList(TeaModel):
    def __init__(
        self,
        type: str = None,
        boxes: List[int] = None,
        score: float = None,
        id: int = None,
    ):
        self.type = type
        self.boxes = boxes
        self.score = score
        self.id = id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.score is not None:
            result['Score'] = self.score
        if self.id is not None:
            result['Id'] = self.id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        return self


class DetectVehicleResponseBodyData(TeaModel):
    def __init__(
        self,
        detect_object_info_list: List[DetectVehicleResponseBodyDataDetectObjectInfoList] = None,
        width: int = None,
        height: int = None,
    ):
        self.detect_object_info_list = detect_object_info_list
        self.width = width
        self.height = height

    def validate(self):
        if self.detect_object_info_list:
            for k in self.detect_object_info_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DetectObjectInfoList'] = []
        if self.detect_object_info_list is not None:
            for k in self.detect_object_info_list:
                result['DetectObjectInfoList'].append(k.to_map() if k else None)
        if self.width is not None:
            result['Width'] = self.width
        if self.height is not None:
            result['Height'] = self.height
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.detect_object_info_list = []
        if m.get('DetectObjectInfoList') is not None:
            for k in m.get('DetectObjectInfoList'):
                temp_model = DetectVehicleResponseBodyDataDetectObjectInfoList()
                self.detect_object_info_list.append(temp_model.from_map(k))
        if m.get('Width') is not None:
            self.width = m.get('Width')
        if m.get('Height') is not None:
            self.height = m.get('Height')
        return self


class DetectVehicleResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectVehicleResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectVehicleResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectVehicleResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectVehicleResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectVehicleResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectVehicleICongestionRequestRoadRegionsRoadRegionPoint(TeaModel):
    def __init__(
        self,
        x: int = None,
        y: int = None,
    ):
        self.x = x
        self.y = y

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        return self


class DetectVehicleICongestionRequestRoadRegionsRoadRegion(TeaModel):
    def __init__(
        self,
        point: DetectVehicleICongestionRequestRoadRegionsRoadRegionPoint = None,
    ):
        self.point = point

    def validate(self):
        if self.point:
            self.point.validate()

    def to_map(self):
        result = dict()
        if self.point is not None:
            result['Point'] = self.point.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Point') is not None:
            temp_model = DetectVehicleICongestionRequestRoadRegionsRoadRegionPoint()
            self.point = temp_model.from_map(m['Point'])
        return self


class DetectVehicleICongestionRequestRoadRegions(TeaModel):
    def __init__(
        self,
        road_region: List[DetectVehicleICongestionRequestRoadRegionsRoadRegion] = None,
    ):
        self.road_region = road_region

    def validate(self):
        if self.road_region:
            for k in self.road_region:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RoadRegion'] = []
        if self.road_region is not None:
            for k in self.road_region:
                result['RoadRegion'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.road_region = []
        if m.get('RoadRegion') is not None:
            for k in m.get('RoadRegion'):
                temp_model = DetectVehicleICongestionRequestRoadRegionsRoadRegion()
                self.road_region.append(temp_model.from_map(k))
        return self


class DetectVehicleICongestionRequestPreRegionIntersectFeatures(TeaModel):
    def __init__(
        self,
        features: List[str] = None,
    ):
        self.features = features

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.features is not None:
            result['Features'] = self.features
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Features') is not None:
            self.features = m.get('Features')
        return self


class DetectVehicleICongestionRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        road_regions: List[DetectVehicleICongestionRequestRoadRegions] = None,
        pre_region_intersect_features: List[DetectVehicleICongestionRequestPreRegionIntersectFeatures] = None,
    ):
        # A short description of struct
        self.image_url = image_url
        self.road_regions = road_regions
        self.pre_region_intersect_features = pre_region_intersect_features

    def validate(self):
        if self.road_regions:
            for k in self.road_regions:
                if k:
                    k.validate()
        if self.pre_region_intersect_features:
            for k in self.pre_region_intersect_features:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        result['RoadRegions'] = []
        if self.road_regions is not None:
            for k in self.road_regions:
                result['RoadRegions'].append(k.to_map() if k else None)
        result['PreRegionIntersectFeatures'] = []
        if self.pre_region_intersect_features is not None:
            for k in self.pre_region_intersect_features:
                result['PreRegionIntersectFeatures'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        self.road_regions = []
        if m.get('RoadRegions') is not None:
            for k in m.get('RoadRegions'):
                temp_model = DetectVehicleICongestionRequestRoadRegions()
                self.road_regions.append(temp_model.from_map(k))
        self.pre_region_intersect_features = []
        if m.get('PreRegionIntersectFeatures') is not None:
            for k in m.get('PreRegionIntersectFeatures'):
                temp_model = DetectVehicleICongestionRequestPreRegionIntersectFeatures()
                self.pre_region_intersect_features.append(temp_model.from_map(k))
        return self


class DetectVehicleICongestionShrinkRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        road_regions_shrink: str = None,
        pre_region_intersect_features_shrink: str = None,
    ):
        # A short description of struct
        self.image_url = image_url
        self.road_regions_shrink = road_regions_shrink
        self.pre_region_intersect_features_shrink = pre_region_intersect_features_shrink

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        if self.road_regions_shrink is not None:
            result['RoadRegions'] = self.road_regions_shrink
        if self.pre_region_intersect_features_shrink is not None:
            result['PreRegionIntersectFeatures'] = self.pre_region_intersect_features_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        if m.get('RoadRegions') is not None:
            self.road_regions_shrink = m.get('RoadRegions')
        if m.get('PreRegionIntersectFeatures') is not None:
            self.pre_region_intersect_features_shrink = m.get('PreRegionIntersectFeatures')
        return self


class DetectVehicleICongestionResponseBodyDataElementsBoxes(TeaModel):
    def __init__(
        self,
        left: int = None,
        top: int = None,
        right: int = None,
        bottom: int = None,
    ):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.left is not None:
            result['Left'] = self.left
        if self.top is not None:
            result['Top'] = self.top
        if self.right is not None:
            result['Right'] = self.right
        if self.bottom is not None:
            result['Bottom'] = self.bottom
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Left') is not None:
            self.left = m.get('Left')
        if m.get('Top') is not None:
            self.top = m.get('Top')
        if m.get('Right') is not None:
            self.right = m.get('Right')
        if m.get('Bottom') is not None:
            self.bottom = m.get('Bottom')
        return self


class DetectVehicleICongestionResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        boxes: List[DetectVehicleICongestionResponseBodyDataElementsBoxes] = None,
        score: float = None,
        type_name: str = None,
    ):
        self.boxes = boxes
        self.score = score
        self.type_name = type_name

    def validate(self):
        if self.boxes:
            for k in self.boxes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Boxes'] = []
        if self.boxes is not None:
            for k in self.boxes:
                result['Boxes'].append(k.to_map() if k else None)
        if self.score is not None:
            result['Score'] = self.score
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.boxes = []
        if m.get('Boxes') is not None:
            for k in m.get('Boxes'):
                temp_model = DetectVehicleICongestionResponseBodyDataElementsBoxes()
                self.boxes.append(temp_model.from_map(k))
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        return self


class DetectVehicleICongestionResponseBodyDataRegionIntersectFeatures(TeaModel):
    def __init__(
        self,
        features: List[str] = None,
    ):
        self.features = features

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.features is not None:
            result['Features'] = self.features
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Features') is not None:
            self.features = m.get('Features')
        return self


class DetectVehicleICongestionResponseBodyDataRegionIntersectMatched(TeaModel):
    def __init__(
        self,
        ids: List[int] = None,
    ):
        self.ids = ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ids is not None:
            result['Ids'] = self.ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ids') is not None:
            self.ids = m.get('Ids')
        return self


class DetectVehicleICongestionResponseBodyDataRegionIntersects(TeaModel):
    def __init__(
        self,
        ids: List[int] = None,
    ):
        self.ids = ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ids is not None:
            result['Ids'] = self.ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ids') is not None:
            self.ids = m.get('Ids')
        return self


class DetectVehicleICongestionResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectVehicleICongestionResponseBodyDataElements] = None,
        region_intersect_features: List[DetectVehicleICongestionResponseBodyDataRegionIntersectFeatures] = None,
        region_intersect_matched: List[DetectVehicleICongestionResponseBodyDataRegionIntersectMatched] = None,
        region_intersects: List[DetectVehicleICongestionResponseBodyDataRegionIntersects] = None,
    ):
        self.elements = elements
        self.region_intersect_features = region_intersect_features
        self.region_intersect_matched = region_intersect_matched
        self.region_intersects = region_intersects

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()
        if self.region_intersect_features:
            for k in self.region_intersect_features:
                if k:
                    k.validate()
        if self.region_intersect_matched:
            for k in self.region_intersect_matched:
                if k:
                    k.validate()
        if self.region_intersects:
            for k in self.region_intersects:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        result['RegionIntersectFeatures'] = []
        if self.region_intersect_features is not None:
            for k in self.region_intersect_features:
                result['RegionIntersectFeatures'].append(k.to_map() if k else None)
        result['RegionIntersectMatched'] = []
        if self.region_intersect_matched is not None:
            for k in self.region_intersect_matched:
                result['RegionIntersectMatched'].append(k.to_map() if k else None)
        result['RegionIntersects'] = []
        if self.region_intersects is not None:
            for k in self.region_intersects:
                result['RegionIntersects'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectVehicleICongestionResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        self.region_intersect_features = []
        if m.get('RegionIntersectFeatures') is not None:
            for k in m.get('RegionIntersectFeatures'):
                temp_model = DetectVehicleICongestionResponseBodyDataRegionIntersectFeatures()
                self.region_intersect_features.append(temp_model.from_map(k))
        self.region_intersect_matched = []
        if m.get('RegionIntersectMatched') is not None:
            for k in m.get('RegionIntersectMatched'):
                temp_model = DetectVehicleICongestionResponseBodyDataRegionIntersectMatched()
                self.region_intersect_matched.append(temp_model.from_map(k))
        self.region_intersects = []
        if m.get('RegionIntersects') is not None:
            for k in m.get('RegionIntersects'):
                temp_model = DetectVehicleICongestionResponseBodyDataRegionIntersects()
                self.region_intersects.append(temp_model.from_map(k))
        return self


class DetectVehicleICongestionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectVehicleICongestionResponseBodyData = None,
    ):
        # Id of the request
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectVehicleICongestionResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectVehicleICongestionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectVehicleICongestionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectVehicleICongestionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectVehicleIllegalParkingRequestRoadRegionsRoadRegionPoint(TeaModel):
    def __init__(
        self,
        x: int = None,
        y: int = None,
    ):
        self.x = x
        self.y = y

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.x is not None:
            result['X'] = self.x
        if self.y is not None:
            result['Y'] = self.y
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('X') is not None:
            self.x = m.get('X')
        if m.get('Y') is not None:
            self.y = m.get('Y')
        return self


class DetectVehicleIllegalParkingRequestRoadRegionsRoadRegion(TeaModel):
    def __init__(
        self,
        point: DetectVehicleIllegalParkingRequestRoadRegionsRoadRegionPoint = None,
    ):
        self.point = point

    def validate(self):
        if self.point:
            self.point.validate()

    def to_map(self):
        result = dict()
        if self.point is not None:
            result['Point'] = self.point.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Point') is not None:
            temp_model = DetectVehicleIllegalParkingRequestRoadRegionsRoadRegionPoint()
            self.point = temp_model.from_map(m['Point'])
        return self


class DetectVehicleIllegalParkingRequestRoadRegions(TeaModel):
    def __init__(
        self,
        road_region: List[DetectVehicleIllegalParkingRequestRoadRegionsRoadRegion] = None,
    ):
        self.road_region = road_region

    def validate(self):
        if self.road_region:
            for k in self.road_region:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RoadRegion'] = []
        if self.road_region is not None:
            for k in self.road_region:
                result['RoadRegion'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.road_region = []
        if m.get('RoadRegion') is not None:
            for k in m.get('RoadRegion'):
                temp_model = DetectVehicleIllegalParkingRequestRoadRegionsRoadRegion()
                self.road_region.append(temp_model.from_map(k))
        return self


class DetectVehicleIllegalParkingRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        road_regions: List[DetectVehicleIllegalParkingRequestRoadRegions] = None,
    ):
        # A short description of struct
        self.image_url = image_url
        self.road_regions = road_regions

    def validate(self):
        if self.road_regions:
            for k in self.road_regions:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        result['RoadRegions'] = []
        if self.road_regions is not None:
            for k in self.road_regions:
                result['RoadRegions'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        self.road_regions = []
        if m.get('RoadRegions') is not None:
            for k in m.get('RoadRegions'):
                temp_model = DetectVehicleIllegalParkingRequestRoadRegions()
                self.road_regions.append(temp_model.from_map(k))
        return self


class DetectVehicleIllegalParkingShrinkRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
        road_regions_shrink: str = None,
    ):
        # A short description of struct
        self.image_url = image_url
        self.road_regions_shrink = road_regions_shrink

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        if self.road_regions_shrink is not None:
            result['RoadRegions'] = self.road_regions_shrink
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        if m.get('RoadRegions') is not None:
            self.road_regions_shrink = m.get('RoadRegions')
        return self


class DetectVehicleIllegalParkingResponseBodyDataElementsBoxes(TeaModel):
    def __init__(
        self,
        left: int = None,
        top: int = None,
        right: int = None,
        bottom: int = None,
    ):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.left is not None:
            result['Left'] = self.left
        if self.top is not None:
            result['Top'] = self.top
        if self.right is not None:
            result['Right'] = self.right
        if self.bottom is not None:
            result['Bottom'] = self.bottom
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Left') is not None:
            self.left = m.get('Left')
        if m.get('Top') is not None:
            self.top = m.get('Top')
        if m.get('Right') is not None:
            self.right = m.get('Right')
        if m.get('Bottom') is not None:
            self.bottom = m.get('Bottom')
        return self


class DetectVehicleIllegalParkingResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        boxes: List[DetectVehicleIllegalParkingResponseBodyDataElementsBoxes] = None,
        score: float = None,
        type_name: str = None,
    ):
        self.boxes = boxes
        self.score = score
        self.type_name = type_name

    def validate(self):
        if self.boxes:
            for k in self.boxes:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Boxes'] = []
        if self.boxes is not None:
            for k in self.boxes:
                result['Boxes'].append(k.to_map() if k else None)
        if self.score is not None:
            result['Score'] = self.score
        if self.type_name is not None:
            result['TypeName'] = self.type_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.boxes = []
        if m.get('Boxes') is not None:
            for k in m.get('Boxes'):
                temp_model = DetectVehicleIllegalParkingResponseBodyDataElementsBoxes()
                self.boxes.append(temp_model.from_map(k))
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('TypeName') is not None:
            self.type_name = m.get('TypeName')
        return self


class DetectVehicleIllegalParkingResponseBodyDataRegionIntersects(TeaModel):
    def __init__(
        self,
        ids: List[int] = None,
    ):
        self.ids = ids

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.ids is not None:
            result['Ids'] = self.ids
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ids') is not None:
            self.ids = m.get('Ids')
        return self


class DetectVehicleIllegalParkingResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectVehicleIllegalParkingResponseBodyDataElements] = None,
        region_intersects: List[DetectVehicleIllegalParkingResponseBodyDataRegionIntersects] = None,
    ):
        self.elements = elements
        self.region_intersects = region_intersects

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()
        if self.region_intersects:
            for k in self.region_intersects:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        result['RegionIntersects'] = []
        if self.region_intersects is not None:
            for k in self.region_intersects:
                result['RegionIntersects'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectVehicleIllegalParkingResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        self.region_intersects = []
        if m.get('RegionIntersects') is not None:
            for k in m.get('RegionIntersects'):
                temp_model = DetectVehicleIllegalParkingResponseBodyDataRegionIntersects()
                self.region_intersects.append(temp_model.from_map(k))
        return self


class DetectVehicleIllegalParkingResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectVehicleIllegalParkingResponseBodyData = None,
    ):
        # Id of the request
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectVehicleIllegalParkingResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectVehicleIllegalParkingResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectVehicleIllegalParkingResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectVehicleIllegalParkingResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DetectWhiteBaseImageRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class DetectWhiteBaseImageAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class DetectWhiteBaseImageResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        white_base: int = None,
    ):
        self.white_base = white_base

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.white_base is not None:
            result['WhiteBase'] = self.white_base
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('WhiteBase') is not None:
            self.white_base = m.get('WhiteBase')
        return self


class DetectWhiteBaseImageResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[DetectWhiteBaseImageResponseBodyDataElements] = None,
    ):
        self.elements = elements

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = DetectWhiteBaseImageResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        return self


class DetectWhiteBaseImageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: DetectWhiteBaseImageResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = DetectWhiteBaseImageResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class DetectWhiteBaseImageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DetectWhiteBaseImageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DetectWhiteBaseImageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GenerateVehicleRepairPlanRequestDamageImageList(TeaModel):
    def __init__(
        self,
        create_time_stamp: str = None,
        image_url: str = None,
    ):
        self.create_time_stamp = create_time_stamp
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.create_time_stamp is not None:
            result['CreateTimeStamp'] = self.create_time_stamp
        if self.image_url is not None:
            result['ImageUrl'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTimeStamp') is not None:
            self.create_time_stamp = m.get('CreateTimeStamp')
        if m.get('ImageUrl') is not None:
            self.image_url = m.get('ImageUrl')
        return self


class GenerateVehicleRepairPlanRequest(TeaModel):
    def __init__(
        self,
        damage_image_list: List[GenerateVehicleRepairPlanRequestDamageImageList] = None,
    ):
        self.damage_image_list = damage_image_list

    def validate(self):
        if self.damage_image_list:
            for k in self.damage_image_list:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['DamageImageList'] = []
        if self.damage_image_list is not None:
            for k in self.damage_image_list:
                result['DamageImageList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.damage_image_list = []
        if m.get('DamageImageList') is not None:
            for k in m.get('DamageImageList'):
                temp_model = GenerateVehicleRepairPlanRequestDamageImageList()
                self.damage_image_list.append(temp_model.from_map(k))
        return self


class GenerateVehicleRepairPlanResponseBodyData(TeaModel):
    def __init__(
        self,
        task_id: str = None,
    ):
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class GenerateVehicleRepairPlanResponseBody(TeaModel):
    def __init__(
        self,
        http_code: int = None,
        request_id: str = None,
        data: GenerateVehicleRepairPlanResponseBodyData = None,
        error_message: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.http_code = http_code
        self.request_id = request_id
        self.data = data
        self.error_message = error_message
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.http_code is not None:
            result['HttpCode'] = self.http_code
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HttpCode') is not None:
            self.http_code = m.get('HttpCode')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = GenerateVehicleRepairPlanResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GenerateVehicleRepairPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GenerateVehicleRepairPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GenerateVehicleRepairPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetVehicleRepairPlanRequest(TeaModel):
    def __init__(
        self,
        task_id: str = None,
        car_number_image: str = None,
        vin_code_image: str = None,
    ):
        self.task_id = task_id
        self.car_number_image = car_number_image
        self.vin_code_image = vin_code_image

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        if self.car_number_image is not None:
            result['CarNumberImage'] = self.car_number_image
        if self.vin_code_image is not None:
            result['VinCodeImage'] = self.vin_code_image
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        if m.get('CarNumberImage') is not None:
            self.car_number_image = m.get('CarNumberImage')
        if m.get('VinCodeImage') is not None:
            self.vin_code_image = m.get('VinCodeImage')
        return self


class GetVehicleRepairPlanResponseBodyDataRepairParts(TeaModel):
    def __init__(
        self,
        relation_type: str = None,
        parts_std_code: str = None,
        part_name_match: bool = None,
        repair_fee: str = None,
        out_standard_parts_name: str = None,
        parts_std_name: str = None,
        repair_type_name: str = None,
        repair_type: str = None,
        oe_match: bool = None,
        out_standard_parts_id: str = None,
        garage_type: str = None,
    ):
        self.relation_type = relation_type
        self.parts_std_code = parts_std_code
        self.part_name_match = part_name_match
        self.repair_fee = repair_fee
        self.out_standard_parts_name = out_standard_parts_name
        self.parts_std_name = parts_std_name
        self.repair_type_name = repair_type_name
        self.repair_type = repair_type
        self.oe_match = oe_match
        self.out_standard_parts_id = out_standard_parts_id
        self.garage_type = garage_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.relation_type is not None:
            result['RelationType'] = self.relation_type
        if self.parts_std_code is not None:
            result['PartsStdCode'] = self.parts_std_code
        if self.part_name_match is not None:
            result['PartNameMatch'] = self.part_name_match
        if self.repair_fee is not None:
            result['RepairFee'] = self.repair_fee
        if self.out_standard_parts_name is not None:
            result['OutStandardPartsName'] = self.out_standard_parts_name
        if self.parts_std_name is not None:
            result['PartsStdName'] = self.parts_std_name
        if self.repair_type_name is not None:
            result['RepairTypeName'] = self.repair_type_name
        if self.repair_type is not None:
            result['RepairType'] = self.repair_type
        if self.oe_match is not None:
            result['OeMatch'] = self.oe_match
        if self.out_standard_parts_id is not None:
            result['OutStandardPartsId'] = self.out_standard_parts_id
        if self.garage_type is not None:
            result['GarageType'] = self.garage_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RelationType') is not None:
            self.relation_type = m.get('RelationType')
        if m.get('PartsStdCode') is not None:
            self.parts_std_code = m.get('PartsStdCode')
        if m.get('PartNameMatch') is not None:
            self.part_name_match = m.get('PartNameMatch')
        if m.get('RepairFee') is not None:
            self.repair_fee = m.get('RepairFee')
        if m.get('OutStandardPartsName') is not None:
            self.out_standard_parts_name = m.get('OutStandardPartsName')
        if m.get('PartsStdName') is not None:
            self.parts_std_name = m.get('PartsStdName')
        if m.get('RepairTypeName') is not None:
            self.repair_type_name = m.get('RepairTypeName')
        if m.get('RepairType') is not None:
            self.repair_type = m.get('RepairType')
        if m.get('OeMatch') is not None:
            self.oe_match = m.get('OeMatch')
        if m.get('OutStandardPartsId') is not None:
            self.out_standard_parts_id = m.get('OutStandardPartsId')
        if m.get('GarageType') is not None:
            self.garage_type = m.get('GarageType')
        return self


class GetVehicleRepairPlanResponseBodyData(TeaModel):
    def __init__(
        self,
        repair_parts: List[GetVehicleRepairPlanResponseBodyDataRepairParts] = None,
        frame_no: str = None,
    ):
        self.repair_parts = repair_parts
        self.frame_no = frame_no

    def validate(self):
        if self.repair_parts:
            for k in self.repair_parts:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['RepairParts'] = []
        if self.repair_parts is not None:
            for k in self.repair_parts:
                result['RepairParts'].append(k.to_map() if k else None)
        if self.frame_no is not None:
            result['FrameNo'] = self.frame_no
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.repair_parts = []
        if m.get('RepairParts') is not None:
            for k in m.get('RepairParts'):
                temp_model = GetVehicleRepairPlanResponseBodyDataRepairParts()
                self.repair_parts.append(temp_model.from_map(k))
        if m.get('FrameNo') is not None:
            self.frame_no = m.get('FrameNo')
        return self


class GetVehicleRepairPlanResponseBody(TeaModel):
    def __init__(
        self,
        http_code: int = None,
        request_id: str = None,
        data: GetVehicleRepairPlanResponseBodyData = None,
        error_message: str = None,
        code: str = None,
        success: bool = None,
    ):
        self.http_code = http_code
        self.request_id = request_id
        self.data = data
        self.error_message = error_message
        self.code = code
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.http_code is not None:
            result['HttpCode'] = self.http_code
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.error_message is not None:
            result['ErrorMessage'] = self.error_message
        if self.code is not None:
            result['Code'] = self.code
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HttpCode') is not None:
            self.http_code = m.get('HttpCode')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = GetVehicleRepairPlanResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('ErrorMessage') is not None:
            self.error_message = m.get('ErrorMessage')
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetVehicleRepairPlanResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetVehicleRepairPlanResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetVehicleRepairPlanResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecognizeVehicleDamageRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RecognizeVehicleDamageAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class RecognizeVehicleDamageResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        type: str = None,
        scores: List[float] = None,
        boxes: List[int] = None,
        score: float = None,
    ):
        self.type = type
        self.scores = scores
        self.boxes = boxes
        self.score = score

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.scores is not None:
            result['Scores'] = self.scores
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Scores') is not None:
            self.scores = m.get('Scores')
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class RecognizeVehicleDamageResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[RecognizeVehicleDamageResponseBodyDataElements] = None,
    ):
        self.elements = elements

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = RecognizeVehicleDamageResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        return self


class RecognizeVehicleDamageResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RecognizeVehicleDamageResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RecognizeVehicleDamageResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RecognizeVehicleDamageResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RecognizeVehicleDamageResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RecognizeVehicleDamageResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecognizeVehicleDashboardRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RecognizeVehicleDashboardAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class RecognizeVehicleDashboardResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        boxes: List[float] = None,
        score: float = None,
        label: str = None,
        class_name: str = None,
    ):
        self.boxes = boxes
        self.score = score
        self.label = label
        self.class_name = class_name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.score is not None:
            result['Score'] = self.score
        if self.label is not None:
            result['Label'] = self.label
        if self.class_name is not None:
            result['ClassName'] = self.class_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        if m.get('Label') is not None:
            self.label = m.get('Label')
        if m.get('ClassName') is not None:
            self.class_name = m.get('ClassName')
        return self


class RecognizeVehicleDashboardResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[RecognizeVehicleDashboardResponseBodyDataElements] = None,
    ):
        self.elements = elements

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = RecognizeVehicleDashboardResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        return self


class RecognizeVehicleDashboardResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RecognizeVehicleDashboardResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RecognizeVehicleDashboardResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RecognizeVehicleDashboardResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RecognizeVehicleDashboardResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RecognizeVehicleDashboardResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RecognizeVehiclePartsRequest(TeaModel):
    def __init__(
        self,
        image_url: str = None,
    ):
        self.image_url = image_url

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.image_url is not None:
            result['ImageURL'] = self.image_url
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURL') is not None:
            self.image_url = m.get('ImageURL')
        return self


class RecognizeVehiclePartsAdvanceRequest(TeaModel):
    def __init__(
        self,
        image_urlobject: BinaryIO = None,
    ):
        self.image_urlobject = image_urlobject

    def validate(self):
        self.validate_required(self.image_urlobject, 'image_urlobject')

    def to_map(self):
        result = dict()
        if self.image_urlobject is not None:
            result['ImageURLObject'] = self.image_urlobject
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ImageURLObject') is not None:
            self.image_urlobject = m.get('ImageURLObject')
        return self


class RecognizeVehiclePartsResponseBodyDataElements(TeaModel):
    def __init__(
        self,
        type: str = None,
        boxes: List[int] = None,
        score: float = None,
    ):
        self.type = type
        self.boxes = boxes
        self.score = score

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.type is not None:
            result['Type'] = self.type
        if self.boxes is not None:
            result['Boxes'] = self.boxes
        if self.score is not None:
            result['Score'] = self.score
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Boxes') is not None:
            self.boxes = m.get('Boxes')
        if m.get('Score') is not None:
            self.score = m.get('Score')
        return self


class RecognizeVehiclePartsResponseBodyData(TeaModel):
    def __init__(
        self,
        elements: List[RecognizeVehiclePartsResponseBodyDataElements] = None,
        origin_shapes: List[int] = None,
    ):
        self.elements = elements
        self.origin_shapes = origin_shapes

    def validate(self):
        if self.elements:
            for k in self.elements:
                if k:
                    k.validate()

    def to_map(self):
        result = dict()
        result['Elements'] = []
        if self.elements is not None:
            for k in self.elements:
                result['Elements'].append(k.to_map() if k else None)
        if self.origin_shapes is not None:
            result['OriginShapes'] = self.origin_shapes
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.elements = []
        if m.get('Elements') is not None:
            for k in m.get('Elements'):
                temp_model = RecognizeVehiclePartsResponseBodyDataElements()
                self.elements.append(temp_model.from_map(k))
        if m.get('OriginShapes') is not None:
            self.origin_shapes = m.get('OriginShapes')
        return self


class RecognizeVehiclePartsResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        data: RecognizeVehiclePartsResponseBodyData = None,
    ):
        self.request_id = request_id
        self.data = data

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.data is not None:
            result['Data'] = self.data.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Data') is not None:
            temp_model = RecognizeVehiclePartsResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        return self


class RecognizeVehiclePartsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RecognizeVehiclePartsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RecognizeVehiclePartsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


