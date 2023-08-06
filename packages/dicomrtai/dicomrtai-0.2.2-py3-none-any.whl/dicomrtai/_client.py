# Copyright (C) 2021 Simon Biggs

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging

import grpc

from .proto import hello_world_pb2, hello_world_pb2_grpc


def say_hello(stub: hello_world_pb2_grpc.HelloWorldStub):
    message = hello_world_pb2.Greeting(content="Hello DICOM-RT AI API server!")
    reply = stub.talk(message)

    print(reply)


def run():
    with grpc.insecure_channel("api.dicomrt.ai:50051") as channel:
        stub = hello_world_pb2_grpc.HelloWorldStub(channel)
        say_hello(stub)


def main():
    logging.basicConfig(level=logging.DEBUG)
    run()
