from data.db import *

def clearData():
    BED_LIST = {}

def testAdd():
    clearData()
    print('TESTING addBed')

    print('should throw INVALID_HOSPITAL')
    try:
        addBed(0)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.INVALID_HOSPITAL.value['code'], "Didn't return INVALID_HOSPITAL"
    
    print('should throw INVALID_HOSPITAL')
    try:
        addBed(6)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.INVALID_HOSPITAL.value['code'], "Didn't return INVALID_HOSPITAL"
    
    print('should add a new bed')
    x = addBed(1)
    assert x.state == False, "Didn't add a new unoccupied bed"
    assert x.id in BED_LIST, "Didn't add a new bed"
    print()



def testDelete():
    clearData()
    print('TESTING deleteBed')
    print('should throw INVALID_BED_ID')
    try:
        deleteBed(1)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.INVALID_BED_ID.value['code'], "Didn't return INVALID_BED_ID"
   
    print('should delete the bed')
    x = addBed(1)
    deleteBed(x.id)
    assert not x.id in BED_LIST == None, "Didn't delete the bed"
    print()


def testOccupate():
    clearData()
    print('TESTING occupateBed')
    print('should throw INVALID_BED_ID')
    try:
        occupyBed(1)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.INVALID_BED_ID.value['code'], "Didn't return INVALID_BED_ID"

    print('should throw ALREADY_OCCUPIED_BED_ERROR')
    try:
        x = addBed(1)
        x.state = True
        occupyBed(x.id)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.ALREADY_OCCUPIED_BED_ERROR.value['code'], "Didn't return ALREADY_OCCUPIED_BED_ERROR"
    x.state = False
    print('should occupate the bed')
    occupyBed(x.id)
    assert x.state == True, "Didn't occupate the bed"
    print()

def testUnoccupate():
    clearData()
    print('TESTING unoccupateBed')
    print('should throw INVALID_BED_ID')
    try:
        unoccupyBed(1)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.INVALID_BED_ID.value['code'], "Didn't return INVALID_BED_ID"

    print('should throw ALREADY_UNOCCUPIED_BED_ERROR')
    try:
        x = addBed(1)
        unoccupyBed(x.id)
        raise AssertionError("Didn't throw any error")
    except UTIError as e:
        assert e.code == CodeError.ALREADY_UNOCCUPIED_BED_ERROR.value['code'], "Didn't return ALREADY_UNOCCUPIED_BED_ERROR"
    x.state = True
    print('should unoccupate the bed')
    unoccupyBed(x.id)
    assert x.state == False, "Didn't unoccupate the bed"
    print()

if __name__ == "__main__":
    testAdd()
    testDelete()
    testOccupate()
    testUnoccupate()
    print("Everything passed")
