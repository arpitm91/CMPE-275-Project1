# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import raft_pb2 as raft__pb2


class RaftServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RaftHeartbeat = channel.unary_unary(
        '/raft.RaftService/RaftHeartbeat',
        request_serializer=raft__pb2.Table.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )
    self.RequestVote = channel.unary_unary(
        '/raft.RaftService/RequestVote',
        request_serializer=raft__pb2.Candidacy.SerializeToString,
        response_deserializer=raft__pb2.CandidacyResponse.FromString,
        )
    self.AddFileLog = channel.unary_unary(
        '/raft.RaftService/AddFileLog',
        request_serializer=raft__pb2.TableLog.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )
    self.AddDataCenter = channel.unary_unary(
        '/raft.RaftService/AddDataCenter',
        request_serializer=raft__pb2.DataCenterInfo.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )
    self.AddProxy = channel.unary_unary(
        '/raft.RaftService/AddProxy',
        request_serializer=raft__pb2.ProxyInfoRaft.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )
    self.FileUploadCompleted = channel.unary_unary(
        '/raft.RaftService/FileUploadCompleted',
        request_serializer=raft__pb2.UploadCompleteFileInfo.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )
    self.GetChunkLocationInfo = channel.unary_unary(
        '/raft.RaftService/GetChunkLocationInfo',
        request_serializer=raft__pb2.RequestChunkInfo.SerializeToString,
        response_deserializer=raft__pb2.ChunkLocationInfo.FromString,
        )
    self.GetChunkUploadInfo = channel.unary_unary(
        '/raft.RaftService/GetChunkUploadInfo',
        request_serializer=raft__pb2.RequestChunkInfo.SerializeToString,
        response_deserializer=raft__pb2.ChunkLocationInfo.FromString,
        )


class RaftServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RaftHeartbeat(self, request, context):
    """(Raft -> Raft) : Raft heartbeats
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RequestVote(self, request, context):
    """(Raft -> Raft) :Raft voting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddFileLog(self, request, context):
    """(Raft -> Raft) : Raft adding log
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddDataCenter(self, request, context):
    """(Data center -> Raft) : Registers data centers
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddProxy(self, request, context):
    """(Proxy -> Raft) : Registers Proxy
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FileUploadCompleted(self, request, context):
    """(Data center -> Raft) : Signals upload completed to raft
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetChunkLocationInfo(self, request, context):
    """(Proxy -> Raft) : Fetches location of an existing file from raft
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetChunkUploadInfo(self, request, context):
    """(Proxy -> Raft) : Fetches location to upload a file from raft
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RaftServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RaftHeartbeat': grpc.unary_unary_rpc_method_handler(
          servicer.RaftHeartbeat,
          request_deserializer=raft__pb2.Table.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
      'RequestVote': grpc.unary_unary_rpc_method_handler(
          servicer.RequestVote,
          request_deserializer=raft__pb2.Candidacy.FromString,
          response_serializer=raft__pb2.CandidacyResponse.SerializeToString,
      ),
      'AddFileLog': grpc.unary_unary_rpc_method_handler(
          servicer.AddFileLog,
          request_deserializer=raft__pb2.TableLog.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
      'AddDataCenter': grpc.unary_unary_rpc_method_handler(
          servicer.AddDataCenter,
          request_deserializer=raft__pb2.DataCenterInfo.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
      'AddProxy': grpc.unary_unary_rpc_method_handler(
          servicer.AddProxy,
          request_deserializer=raft__pb2.ProxyInfoRaft.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
      'FileUploadCompleted': grpc.unary_unary_rpc_method_handler(
          servicer.FileUploadCompleted,
          request_deserializer=raft__pb2.UploadCompleteFileInfo.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
      'GetChunkLocationInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetChunkLocationInfo,
          request_deserializer=raft__pb2.RequestChunkInfo.FromString,
          response_serializer=raft__pb2.ChunkLocationInfo.SerializeToString,
      ),
      'GetChunkUploadInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetChunkUploadInfo,
          request_deserializer=raft__pb2.RequestChunkInfo.FromString,
          response_serializer=raft__pb2.ChunkLocationInfo.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'raft.RaftService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class ProxyServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ProxyHeartbeat = channel.unary_unary(
        '/raft.ProxyService/ProxyHeartbeat',
        request_serializer=raft__pb2.TableLog.SerializeToString,
        response_deserializer=raft__pb2.Empty.FromString,
        )


class ProxyServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ProxyHeartbeat(self, request, context):
    """(Raft -> Proxy) : Heartbeat for proxy
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProxyServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ProxyHeartbeat': grpc.unary_unary_rpc_method_handler(
          servicer.ProxyHeartbeat,
          request_deserializer=raft__pb2.TableLog.FromString,
          response_serializer=raft__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'raft.ProxyService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class DataCenterServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.DataCenterHeartbeat = channel.unary_unary(
        '/raft.DataCenterService/DataCenterHeartbeat',
        request_serializer=raft__pb2.Empty.SerializeToString,
        response_deserializer=raft__pb2.Empty.FromString,
        )
    self.ReplicationInitiate = channel.unary_unary(
        '/raft.DataCenterService/ReplicationInitiate',
        request_serializer=raft__pb2.ReplicationInfo.SerializeToString,
        response_deserializer=raft__pb2.Ack.FromString,
        )


class DataCenterServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def DataCenterHeartbeat(self, request, context):
    """(Raft -> Data center) : Heartbeat for data center
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReplicationInitiate(self, request, context):
    """(Raft -> Data center) : Start a replication
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DataCenterServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'DataCenterHeartbeat': grpc.unary_unary_rpc_method_handler(
          servicer.DataCenterHeartbeat,
          request_deserializer=raft__pb2.Empty.FromString,
          response_serializer=raft__pb2.Empty.SerializeToString,
      ),
      'ReplicationInitiate': grpc.unary_unary_rpc_method_handler(
          servicer.ReplicationInitiate,
          request_deserializer=raft__pb2.ReplicationInfo.FromString,
          response_serializer=raft__pb2.Ack.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'raft.DataCenterService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
