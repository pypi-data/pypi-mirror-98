from . import act_gui_demo_pb2_grpc as importStub

class HandWinActService(object):

    def __init__(self, router):
        self.connector = router.get_connection(HandWinActService, importStub.HandWinActStub)

    def register(self, request, timeout=None):
        return self.connector.create_request('register', request, timeout)

    def unregister(self, request, timeout=None):
        return self.connector.create_request('unregister', request, timeout)

    def sendNewOrderSingleGui(self, request, timeout=None):
        return self.connector.create_request('sendNewOrderSingleGui', request, timeout)

    def extractSentMessageGui(self, request, timeout=None):
        return self.connector.create_request('extractSentMessageGui', request, timeout)

    def findMessageGui(self, request, timeout=None):
        return self.connector.create_request('findMessageGui', request, timeout)