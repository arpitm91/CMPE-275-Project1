# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import file_transfer_pb2 as file__transfer__pb2


class DataTransferServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RequestFileInfo = channel.unary_unary(
        '/grpc.DataTransferService/RequestFileInfo',
        request_serializer=file__transfer__pb2.FileInfo.SerializeToString,
        response_deserializer=file__transfer__pb2.FileLocationInfo.FromString,
        )
    self.GetFileLocation = channel.unary_unary(
        '/grpc.DataTransferService/GetFileLocation',
        request_serializer=file__transfer__pb2.FileInfo.SerializeToString,
        response_deserializer=file__transfer__pb2.FileLocationInfo.FromString,
        )
    self.DownloadChunk = channel.unary_stream(
        '/grpc.DataTransferService/DownloadChunk',
        request_serializer=file__transfer__pb2.ChunkInfo.SerializeToString,
        response_deserializer=file__transfer__pb2.FileMetaData.FromString,
        )


class DataTransferServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RequestFileInfo(self, request, context):
    """From team's client to team's own cluster
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetFileLocation(self, request, context):
    """From team-1 cluster to rest of the nodes of other teams
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DownloadChunk(self, request, context):
    """From team's client to the actual data-center node (can be any team's node)
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DataTransferServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RequestFileInfo': grpc.unary_unary_rpc_method_handler(
          servicer.RequestFileInfo,
          request_deserializer=file__transfer__pb2.FileInfo.FromString,
          response_serializer=file__transfer__pb2.FileLocationInfo.SerializeToString,
      ),
      'GetFileLocation': grpc.unary_unary_rpc_method_handler(
          servicer.GetFileLocation,
          request_deserializer=file__transfer__pb2.FileInfo.FromString,
          response_serializer=file__transfer__pb2.FileLocationInfo.SerializeToString,
      ),
      'DownloadChunk': grpc.unary_stream_rpc_method_handler(
          servicer.DownloadChunk,
          request_deserializer=file__transfer__pb2.ChunkInfo.FromString,
          response_serializer=file__transfer__pb2.FileMetaData.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'grpc.DataTransferService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
