
class MenuSetting:
    file = '파일'
    edit = '편집'
    dummy1 = '더미1'
    lst = [file, edit, dummy1]
    dtlLst = { file : ['dummy1'],
              edit : ['dummy1', 'dummy2'],
              dummy1: ['dummy1', 'dummy2', 'dummy3']}

class BoardSetting:
    name = '보드 설정'
    size = '보드 크기'
    size1 = '8'
    size2 = '12'
    placement = '착수 규칙'
    placement1 = 'cell'
    placement2 = 'cross point'
    background = '배경 이미지'

class ObjectSetting:
    name = '오브젝트 설정'
    count = '오브젝트 개수'
    count1 = '1'
    count2 = '2'
    count3 = '3'
    image = '오브젝트 이미지'
    image1 = '후수'
    image2 = '선수'
    images = '오브젝트 이미지들'

class BoardReset:
    name = '보드 초기화'

class PlacementRule:
    name = '착수 규칙'
    ruleFirst = '1규칙'
    ruleFirst1 = '추가'
    ruleFirst2 = '이동'
    ruleSecond = '2규칙'
    ruleSeconds = ['자유', '+', 'X', '*']
    ruleSecond1 = '자유'
    ruleSecond2 = '+'
    ruleSecond3 = 'X'
    ruleSecond4 = '*'

class PlacementOption:
    name = '착수 옵션'
    row = '행'
    col = '열'
    over = '넘기'
    size = '크기'


class PlacementAfterRule:
    name = '착수 후 규칙'

class ExitRule:
    name = '종료 규칙'


def getSettingList():
    settingClassList = [BoardSetting, ObjectSetting, BoardReset, PlacementRule, PlacementOption, PlacementAfterRule, ExitRule]
    return [settingClass.name for settingClass in settingClassList]
