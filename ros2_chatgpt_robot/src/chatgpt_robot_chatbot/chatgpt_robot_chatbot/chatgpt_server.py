import rclpy
from rclpy.node import Node
from chatbot_interfaces.srv import Chatbot
import openai

class ChatbotServer(Node):

    def __init__(self):
        super().__init__("chatbot_server")
        self.srv = self.create_service(Chatbot, "chatbot", self.handle_request)

        # Set up OpenAI API credentials
        openai.api_key = "your_openai_api_key_here"

    def handle_request(self, request, response):
        try:
            # Call the OpenAI chatbot API
            prompt = f"Q: {request.question}\nA:"
            response_text = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text.strip()

            # Set the response message
            response.response = response_text
        except Exception as e:
            self.get_logger().error(f"Error: {e}")
            response.response = "Sorry, I couldn't understand the question."

        return response

def main(args=None):
    rclpy.init(args=args)

    server = ChatbotServer()

    # Spin the node so the service can handle requests
    rclpy.spin(server)

    # Clean up
    server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
