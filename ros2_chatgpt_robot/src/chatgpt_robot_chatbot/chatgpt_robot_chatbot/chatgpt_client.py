import rclpy
from rclpy.node import Node

from chatgpt_interfaces.srv import ChatGPT

def main(args=None):
    rclpy.init(args=args)

    node = Node("chatbot_client")

    # Get the service client
    client = node.create_client(ChatGPT, "chatbot")

    while rclpy.ok():
        # Get input from the user
        question = input("Ask me a question: ")

        # Create a request message
        request = ChatGPT.Request()
        request.question = question

        # Call the service and wait for a response
        future = client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            # Display the response
            node.get_logger().info(f"Response: {future.result().answer}")
        else:
            node.get_logger().info("Service call failed")

    # Clean up
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
