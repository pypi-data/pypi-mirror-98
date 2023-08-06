from . import check2_recon_pb2_grpc as importStub

class Check2ReconService(object):

    def __init__(self, router):
        self.connector = router.get_connection(Check2ReconService, importStub.Check2ReconStub)

    def submitGroupBatch(self, request, timeout=None):
        return self.connector.create_request('submitGroupBatch', request, timeout)