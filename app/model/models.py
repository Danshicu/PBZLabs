import datetime


class Worker:
    id: str
    fullname: str
    postID: int
    isActive: bool

    def __init__(self, id, fullname, postID, isActive):
        self.id = id
        self.fullname = fullname
        self.postID = postID
        self.isActive = isActive


class Edition:
    subscriptionIndex:str
    editionName:str
    editionType:int
    subscriptionPerCopyCost:float

    def __init__(self, subscriptionIndex, editionName, editionType, subscriptionPerCopyCost):
        self.subscriptionIndex = subscriptionIndex
        self.editionName = editionName
        self.editionType = editionType
        self.subscriptionPerCopyCost = subscriptionPerCopyCost


class ReceivedEdition:
    receiveDate:datetime
    subscriptionIndex:str
    numberOfCopy:int
    workerId:str

    def __init__(self, receiveDate, subscriptionIndex, numberOfCopy, workerId):
        self.receiveDate=receiveDate
        self.subscriptionIndex = subscriptionIndex
        self.numberOfCopy=numberOfCopy
        self.workerId=workerId


class Subscription:
    editionIndex:str
    countOfCopiesPerTime:int
    startDate:datetime
    endDate:datetime
    subscriptionCost:float
    frequencyOfReleaseId:int
    deliveryTypeId:int
    dateOfDelivery:datetime

    def __init__(self, editionIndex, countOfCopiesPerTime, startDate, endDate, subscriptionCost, frequencyOfReleaseId, deliveryTypeId, dateOfDelivery):
        self.editionIndex= editionIndex
        self.countOfCopiesPerTime = countOfCopiesPerTime
        self.startDate = startDate
        self.endDate = endDate
        self.subscriptionCost = subscriptionCost
        self.frequencyOfReleaseId = frequencyOfReleaseId
        self.deliveryTypeId = deliveryTypeId
        self.dateOfDelivery = dateOfDelivery

