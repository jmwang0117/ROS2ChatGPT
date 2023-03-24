import rclpy
from rclpy.node import Node
from chatgpt_interfaces.srv import ChatGPT
import openai

class ChatbotServer(Node):

    def __init__(self):
        super().__init__("chatbot_server")
        self.srv = self.create_service(ChatGPT, "chatbot", self.handle_request)

        # Set up OpenAI API credentials
        openai.api_key = "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"

    def handle_request(self, request, response):
        try:
            # Call the OpenAI chatbot API with the prompt
            prompt = f"Q: {request.question}\nA:"
            response_text = ""
            completions = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices
            for completion in completions:
                # Only use the first response generated
                response_text = completion.text.strip()
                break
            
            # Set the response message
            response.answer = response_text
        except Exception as e:
            self.get_logger().error(f"Error: {e}")
            response.answer = "Sorry, I couldn't understand the question."

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
