import { io } from "socket.io-client";
import "./style.css";

function randomString() {
  return Math.random().toString(36).substring(2, 15);
}

function OutgoingMessage(text) {
  return {
    message_sid: randomString(),
    text,
  };
}

const socket = io(`http://${window.location.hostname}:5000`);
socket.on("connect", () => {
  console.log("connected");
});

socket.on("disconnect", () => {
  console.log("disconnected");
});

socket.on("message", (message) => {
  console.log(message);
});

socket.on("error", (error) => {
  console.error(error);
});

// socket.emit("message", JSON.stringify({ text: "hello world!" }));

const chatHistory = document.getElementById("chat-history");
const chatTextArea = document.getElementById("chat-textarea");
const sendButton = document.getElementById("send-button");

function ChatHistoryMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("chat-history-message");
  messageElement.innerText = message;
  return messageElement;
}
let nextChatMessage = ChatHistoryMessage("Hello!");
// chatHistory.appendChild(nextChatMessage);
socket.on("message", (raw) => {
  console.log("Received message from server:", raw);
  const message = JSON.parse(raw);
  console.log("message", message);

  if (message.isNewMessage) {
    nextChatMessage = ChatHistoryMessage("");
    chatHistory.appendChild(nextChatMessage);
  }

  nextChatMessage.innerText += message.text;
  // We don't scroll to the bottom while the server is sending us messages.
});

function sendChatMessage() {
  const text = chatTextArea.value;
  chatTextArea.value = "";

  chatHistory.appendChild(ChatHistoryMessage(text));

  // Scroll to the bottom of the chatHistory
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Send the message to the server
  socket.send(JSON.stringify(OutgoingMessage(text))); // This will be sent as a JSON string
  console.log("Message sent to server: " + text);
}

let isShiftPressed = false;
chatTextArea.addEventListener("keydown", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = true;
  }
});
chatTextArea.addEventListener("keyup", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = false;
  }
});
chatTextArea.addEventListener("input", (event) => {
  if (event.inputType === "insertLineBreak" && !isShiftPressed) {
    sendChatMessage();
  }
});
sendButton.addEventListener("click", sendChatMessage);
