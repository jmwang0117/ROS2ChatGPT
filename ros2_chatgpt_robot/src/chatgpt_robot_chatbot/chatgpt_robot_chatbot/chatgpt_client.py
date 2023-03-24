import rclpy
from rclpy.node import Node

from chatgpt_interfaces.srv import ChatGPT
import threading

class ChatbotClient(Node):

    def __init__(self):
        super().__init__("chatbot_client")
        self.client = self.create_client(ChatGPT, "chatbot")
        self.semaphore = threading.Semaphore(1)

    def call_service(self, question):
        request = ChatGPT.Request()
        request.question = question

        future = self.client.call_async(request)

        # Wait for the response in a non-blocking way
        while not future.done():
            rclpy.spin_once(self)

        try:
            # Get the response
            response = future.result()
            self.get_logger().info(f"Response: {response.answer}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

        # Release the semaphore
        self.semaphore.release()

    def run(self):
        # Start the client loop
        while rclpy.ok():
            # Get input from the user
            question = input("Ask me a question: ")

            # Acquire the semaphore to prevent multiple threads from running concurrently
            self.semaphore.acquire()

            # Start a new thread to call the service
            thread = threading.Thread(target=self.call_service, args=[question])
            thread.start()

def main(args=None):
    rclpy.init(args=args)

    client = ChatbotClient()

    # Start the client loop
    client.run()

    # Clean up
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
