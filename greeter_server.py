#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import socket

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        name = request.name
        msg_body = "["+ hostname + "]" + " Hello," + name + ", from: " + ip
        print("Request from: " + name)
        return helloworld_pb2.HelloReply(message=msg_body)

def serve():
    with open('privatekey.pem','rb') as f:
        private_key = f.read()

    with open('public.crt', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    #server.add_insecure_port('[::]:50051')
    server.add_secure_port('[::]:9090', server_credentials)

    server.start()
    print('Server started...')
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()