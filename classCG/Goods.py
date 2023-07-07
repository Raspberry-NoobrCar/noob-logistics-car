
# 货物类

class Goods:

    def __init__(self, Gno, destination, email, recipientName,receivingMothd):
        self.Gno = Gno
        self.destination = destination
        self.email = email
        self.recipientName = recipientName
        self.receivingMothd = receivingMothd
        self.signed = False

    def getGno(self):
        return self.Gno
    
    def getDestination(self):
        return self.destination
    
    def getEmail(self):
        return self.email
    
    def getRecipientName(self):
        return self.recipientName
    
    def getReceivingMothd(self):
        return self.receivingMothd
    
    def getSigned(self):
        return self.signed

    # 已被签收
    def setSigned(self):
        self.signed = True